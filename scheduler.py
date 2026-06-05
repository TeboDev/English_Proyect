"""
scheduler.py — APScheduler jobs for ZenEnglish Bot.

Jobs:
  • check_blackout   — runs every minute; sends Digital Blackout 1h before bedtime
  • check_morning    — runs every minute; sends morning check-in at wake time
  • reset_flags      — runs daily at midnight; resets the blackout_sent flag
"""

import logging
from datetime import datetime, timedelta, timezone

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from telegram import Bot

import database as db
import messages as msg

logger = logging.getLogger(__name__)


def _now_hhmm() -> str:
    """Return current UTC time as HH:MM string."""
    return datetime.now(timezone.utc).strftime("%H:%M")


def _subtract_hour(hhmm: str) -> str:
    """Return the HH:MM that is 60 minutes before the given HH:MM."""
    dt = datetime.strptime(hhmm, "%H:%M")
    earlier = (dt - timedelta(hours=1)).strftime("%H:%M")
    return earlier


async def _check_blackout(bot: Bot) -> None:
    """Send Digital Blackout notification 1 hour before each user's bedtime."""
    now = _now_hhmm()
    for user in db.get_all_users():
        trigger_time = _subtract_hour(user["bedtime"])
        if now == trigger_time and not user["blackout_sent"]:
            try:
                await bot.send_message(
                    chat_id=user["chat_id"],
                    text=msg.DIGITAL_BLACKOUT,
                    parse_mode="Markdown",
                )
                db.mark_blackout_sent(user["chat_id"])
                logger.info("Digital Blackout sent → chat_id=%s", user["chat_id"])
            except Exception as exc:
                logger.error(
                    "Failed to send blackout to %s: %s", user["chat_id"], exc
                )


async def _check_morning(bot: Bot) -> None:
    """Send morning check-in at each user's configured wake time."""
    now = _now_hhmm()
    for user in db.get_all_users():
        if now == user["waketime"]:
            # Avoid re-sending if already done today
            if db.get_today_log(user["chat_id"]):
                continue
            try:
                await bot.send_message(
                    chat_id=user["chat_id"],
                    text=msg.MORNING_CHECKIN_INTRO,
                    parse_mode="Markdown",
                )
                logger.info("Morning check-in sent → chat_id=%s", user["chat_id"])
            except Exception as exc:
                logger.error(
                    "Failed to send morning check-in to %s: %s", user["chat_id"], exc
                )


def _reset_flags() -> None:
    db.reset_daily_flags()
    logger.info("Daily flags reset at midnight.")


def create_scheduler(bot: Bot) -> AsyncIOScheduler:
    """Build and return a configured AsyncIOScheduler."""
    scheduler = AsyncIOScheduler()

    # Every minute: check blackout triggers
    scheduler.add_job(
        _check_blackout,
        trigger="cron",
        minute="*",
        id="check_blackout",
        kwargs={"bot": bot},
    )

    # Every minute: check morning wake triggers
    scheduler.add_job(
        _check_morning,
        trigger="cron",
        minute="*",
        id="check_morning",
        kwargs={"bot": bot},
    )

    # Daily at midnight UTC: reset flags
    scheduler.add_job(
        _reset_flags,
        trigger="cron",
        hour=0,
        minute=0,
        id="reset_flags",
    )

    return scheduler
