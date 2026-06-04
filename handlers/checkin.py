"""
handlers/checkin.py — Morning check-in conversation.

Triggered automatically by the scheduler OR manually by the user.

States:
  CHECKIN_MOOD  → inline keyboard with mood options
  CHECKIN_SLEEP → user types hours slept
"""

import logging
from datetime import date

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

import database as db
import messages as msg

logger = logging.getLogger(__name__)

CHECKIN_MOOD, CHECKIN_SLEEP = range(10, 12)

# Mood keyboard
_MOOD_KEYBOARD = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("😄 Great", callback_data="mood:great"),
            InlineKeyboardButton("🙂 Good", callback_data="mood:good"),
        ],
        [
            InlineKeyboardButton("😐 Okay", callback_data="mood:okay"),
            InlineKeyboardButton("😴 Tired", callback_data="mood:tired"),
        ],
        [
            InlineKeyboardButton("😰 Stressed", callback_data="mood:stressed"),
        ],
    ]
)


async def checkin_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Entry point — send mood question with inline keyboard."""
    await update.message.reply_text(
        f"{msg.MORNING_CHECKIN_INTRO}\n\n_{msg.MORNING_MOOD_QUESTION}_",
        reply_markup=_MOOD_KEYBOARD,
        parse_mode="Markdown",
    )
    return CHECKIN_MOOD


async def checkin_mood_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()

    mood_key = query.data.split(":")[1]
    context.user_data["mood"] = mood_key

    await query.edit_message_text(
        f"✅ Mood noted: {msg.MOOD_MAP[mood_key][0]} {msg.MOOD_MAP[mood_key][1]}\n\n"
        f"_{msg.MORNING_SLEEP_QUESTION}_",
        parse_mode="Markdown",
    )
    return CHECKIN_SLEEP


async def checkin_sleep_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text.strip().replace(",", ".")
    try:
        hours = float(text)
        if not (1 <= hours <= 24):
            raise ValueError
    except ValueError:
        await update.message.reply_text(msg.MORNING_SLEEP_INVALID, parse_mode="Markdown")
        return CHECKIN_SLEEP

    mood_key = context.user_data.get("mood", "default")
    chat_id = update.effective_chat.id
    today = date.today().isoformat()

    db.upsert_sleep_log(chat_id, today, hours, mood_key)
    logger.info("Check-in saved: chat=%s, date=%s, hours=%s, mood=%s", chat_id, today, hours, mood_key)

    emoji, label = msg.MOOD_MAP.get(mood_key, ("🌿", mood_key.capitalize()))
    motivational = msg.get_motivational(mood_key)

    await update.message.reply_text(
        msg.MORNING_CHECKIN_DONE.format(
            mood_emoji=emoji,
            mood_label=label,
            hours=hours,
            motivational_message=motivational,
        ),
        parse_mode="Markdown",
    )
    return ConversationHandler.END


async def checkin_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("⚠️ Check-in cancelled. You can do it anytime with /checkin.")
    return ConversationHandler.END


def build_checkin_handler() -> ConversationHandler:
    return ConversationHandler(
        entry_points=[CommandHandler("checkin", checkin_start)],
        states={
            CHECKIN_MOOD: [CallbackQueryHandler(checkin_mood_callback, pattern="^mood:")],
            CHECKIN_SLEEP: [MessageHandler(filters.TEXT & ~filters.COMMAND, checkin_sleep_input)],
        },
        fallbacks=[CommandHandler("cancel", checkin_cancel)],
        name="checkin_conversation",
        per_message=False,   # one active check-in per user (chat), not per message
        persistent=False,
    )
