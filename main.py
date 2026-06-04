"""
main.py — ZenEnglish Bot entry point.

Usage:
    python main.py

Environment variables (via .env):
    BOT_TOKEN — Telegram Bot API token from @BotFather
"""

import asyncio
import logging
import os

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, Application

import database as db
from scheduler import create_scheduler
from handlers.general import build_general_handlers
from handlers.setup import build_setup_handler
from handlers.pomodoro import build_pomodoro_handler
from handlers.checkin import build_checkin_handler
from handlers.report import build_report_handler

# ──────────────────────────────────────────────────
#  Logging
# ──────────────────────────────────────────────────
logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ──────────────────────────────────────────────────
#  Load environment
# ──────────────────────────────────────────────────
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise RuntimeError(
        "BOT_TOKEN is not set. "
        "Create a .env file with BOT_TOKEN=<your_token> and try again."
    )


# ──────────────────────────────────────────────────
#  Scheduler lifecycle hooks
#  (must run inside the event loop — use post_init / post_shutdown)
# ──────────────────────────────────────────────────
async def post_init(application: Application) -> None:
    """Called by PTB after the event loop is running."""
    # 1. Start APScheduler
    scheduler = create_scheduler(application.bot)
    scheduler.start()
    application.bot_data["scheduler"] = scheduler
    logger.info("Scheduler started.")

    # 2. Start a dummy web server for Render (Free Tier)
    # Render Web Services require the app to bind to $PORT within 60 seconds
    port = int(os.environ.get("PORT", 8080))
    
    async def dummy_handler(reader, writer):
        writer.write(b"HTTP/1.1 200 OK\r\n\r\nBot is running!")
        await writer.drain()
        writer.close()

    server = await asyncio.start_server(dummy_handler, '0.0.0.0', port)
    application.bot_data["dummy_server"] = server
    asyncio.create_task(server.serve_forever())
    logger.info(f"Dummy web server listening on port {port} for Render health checks.")


async def post_shutdown(application: Application) -> None:
    """Cleanly stop the scheduler and web server when the bot shuts down."""
    scheduler = application.bot_data.get("scheduler")
    if scheduler and scheduler.running:
        scheduler.shutdown(wait=False)
        logger.info("Scheduler stopped.")
        
    server = application.bot_data.get("dummy_server")
    if server:
        server.close()
        await server.wait_closed()
        logger.info("Dummy web server stopped.")


# ──────────────────────────────────────────────────
#  Application factory
# ──────────────────────────────────────────────────
def build_app() -> Application:
    app = (
        ApplicationBuilder()
        .token(BOT_TOKEN)
        .post_init(post_init)
        .post_shutdown(post_shutdown)
        .build()
    )

    # Conversation handlers (must be added before general command handlers)
    app.add_handler(build_setup_handler())
    app.add_handler(build_checkin_handler())

    # Simple command handlers
    app.add_handler(build_pomodoro_handler())
    app.add_handler(build_report_handler())

    # General handlers (start, help, unknown)
    for handler in build_general_handlers():
        app.add_handler(handler)

    return app


# ──────────────────────────────────────────────────
#  Entry point
# ──────────────────────────────────────────────────
def main() -> None:
    # 1. Initialise database
    db.init_db()
    logger.info("Database initialised.")

    # 2. Python 3.12+ no longer auto-creates an event loop via get_event_loop().
    #    PTB 22.x still relies on this internally, so we create one explicitly.
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # 3. Build app (post_init starts the scheduler once the loop is live)
    app = build_app()
    logger.info("ZenEnglish Bot is starting… 🌿")

    # 4. run_polling is a blocking call that drives the event loop
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
