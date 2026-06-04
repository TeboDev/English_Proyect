"""
handlers/general.py — /start, /help, and fallback unknown-command handler.
"""

import logging
from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, ContextTypes, filters

import messages as msg

logger = logging.getLogger(__name__)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(msg.WELCOME, parse_mode="Markdown")
    logger.info("New user: chat_id=%s", update.effective_chat.id)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(msg.HELP, parse_mode="Markdown")


async def unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(msg.UNKNOWN_COMMAND)


def build_general_handlers() -> list:
    return [
        CommandHandler("start", start_command),
        CommandHandler("help", help_command),
        MessageHandler(filters.COMMAND, unknown_command),
    ]
