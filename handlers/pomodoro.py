"""
handlers/pomodoro.py — /pomodoro command.

Starts a 25-minute Pomodoro timer using asyncio. The job is stored in
context.bot_data so it can be cancelled if the same user calls /pomodoro
while one is already running.
"""

import asyncio
import logging
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

import messages as msg

logger = logging.getLogger(__name__)

POMODORO_MINUTES = 2
BREAK_MINUTES = 1

# Key for storing active pomodoro tasks per chat
_ACTIVE_KEY = "pomodoro_tasks"


async def _run_pomodoro(chat_id: int, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Async task: sleep 25 min, then send break notification."""
    try:
        await asyncio.sleep(POMODORO_MINUTES * 60)
        await context.bot.send_message(
            chat_id=chat_id,
            text=msg.POMODORO_BREAK,
            parse_mode="Markdown",
        )
        logger.info("Pomodoro break notification sent → chat_id=%s", chat_id)
    except asyncio.CancelledError:
        logger.info("Pomodoro task cancelled for chat_id=%s", chat_id)
    finally:
        # Clean up task reference
        tasks: dict = context.bot_data.setdefault(_ACTIVE_KEY, {})
        tasks.pop(chat_id, None)


async def pomodoro_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    tasks: dict = context.bot_data.setdefault(_ACTIVE_KEY, {})

    if chat_id in tasks and not tasks[chat_id].done():
        await update.message.reply_text(
            msg.POMODORO_ALREADY_RUNNING, parse_mode="Markdown"
        )
        return

    await update.message.reply_text(msg.POMODORO_START, parse_mode="Markdown")

    # Schedule the async task
    loop = asyncio.get_event_loop()
    task = loop.create_task(_run_pomodoro(chat_id, context))
    tasks[chat_id] = task
    logger.info("Pomodoro started for chat_id=%s", chat_id)


def build_pomodoro_handler() -> CommandHandler:
    return CommandHandler("pomodoro", pomodoro_command)
