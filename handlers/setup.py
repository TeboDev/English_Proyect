"""
handlers/setup.py — /setup command: collect bedtime & wake time from the user.

Conversation states:
  SETUP_BEDTIME  → user sends their bedtime
  SETUP_WAKETIME → user sends their wake-up time
"""

import re
import logging
from telegram import Update
from telegram.ext import (
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

import database as db
import messages as msg

logger = logging.getLogger(__name__)

SETUP_BEDTIME, SETUP_WAKETIME = range(2)

_TIME_RE = re.compile(r"^([01]?\d|2[0-3]):([0-5]\d)$")


def _valid_time(text: str) -> bool:
    return bool(_TIME_RE.match(text.strip()))


async def setup_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(msg.SETUP_ASK_BEDTIME, parse_mode="Markdown")
    return SETUP_BEDTIME


async def setup_bedtime(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text.strip()
    if not _valid_time(text):
        await update.message.reply_text(msg.SETUP_INVALID_TIME, parse_mode="Markdown")
        return SETUP_BEDTIME

    match = _TIME_RE.match(text)
    normalized = f"{int(match.group(1)):02d}:{int(match.group(2)):02d}"
    context.user_data["bedtime"] = normalized
    await update.message.reply_text(msg.SETUP_ASK_WAKETIME, parse_mode="Markdown")
    return SETUP_WAKETIME


async def setup_waketime(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text.strip()
    if not _valid_time(text):
        await update.message.reply_text(msg.SETUP_INVALID_TIME, parse_mode="Markdown")
        return SETUP_WAKETIME

    match = _TIME_RE.match(text)
    waketime = f"{int(match.group(1)):02d}:{int(match.group(2)):02d}"
    bedtime = context.user_data.get("bedtime", "22:00")
    chat_id = update.effective_chat.id

    db.upsert_user(chat_id, bedtime, waketime)
    logger.info("User %s configured: bed=%s, wake=%s", chat_id, bedtime, waketime)

    await update.message.reply_text(
        msg.SETUP_COMPLETE.format(bedtime=bedtime, waketime=waketime),
        parse_mode="Markdown",
    )
    return ConversationHandler.END


async def setup_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("⚠️ Setup cancelled. Run /setup any time to try again.")
    return ConversationHandler.END


def build_setup_handler() -> ConversationHandler:
    return ConversationHandler(
        entry_points=[CommandHandler("setup", setup_start)],
        states={
            SETUP_BEDTIME: [MessageHandler(filters.TEXT & ~filters.COMMAND, setup_bedtime)],
            SETUP_WAKETIME: [MessageHandler(filters.TEXT & ~filters.COMMAND, setup_waketime)],
        },
        fallbacks=[CommandHandler("cancel", setup_cancel)],
        name="setup_conversation",
        persistent=False,
    )
