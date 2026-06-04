"""
handlers/report.py — /report command: show the user's weekly sleep history.
"""

import logging
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

import database as db
import messages as msg

logger = logging.getLogger(__name__)


async def report_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    logs = db.get_weekly_logs(chat_id, weeks=1)

    if not logs:
        await update.message.reply_text(msg.REPORT_EMPTY, parse_mode="Markdown")
        return

    lines = [msg.REPORT_HEADER]
    total_hours = 0.0
    count = 0

    for row in logs:
        mood_key = row["mood"] or "default"
        emoji, label = msg.MOOD_MAP.get(mood_key, ("🌿", mood_key.capitalize()))
        hours = row["hours_slept"] if row["hours_slept"] is not None else 0
        total_hours += hours
        count += 1
        lines.append(
            msg.REPORT_ROW.format(
                date=row["log_date"],
                hours=hours,
                mood_emoji=emoji,
                mood_label=label,
            )
        )

    if count:
        lines.append(msg.REPORT_AVERAGE.format(avg=total_hours / count))

    lines.append(msg.REPORT_FOOTER)
    await update.message.reply_text("".join(lines), parse_mode="Markdown")
    logger.info("Report sent → chat_id=%s (%d records)", chat_id, count)


def build_report_handler() -> CommandHandler:
    return CommandHandler("report", report_command)
