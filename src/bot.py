#!/usr/bin/env python3
import logging
import os

from db.db_handler import db_create
from dotenv import load_dotenv
from handlers import (
    CURRENT,
    HIGH,
    LOW,
    border_high,
    border_low,
    buttons_control,
    current_btc,
    help_output,
    main_menu,
    register,
    reschedule_user_jobs,
    start,
    wrong_conv,
)
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

load_dotenv()

# enable with LOG_LEVEL=INFO or DEBUG; off by default (WARNING)
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "WARNING"),
    format="%(asctime)s %(name)s %(levelname)s %(message)s",
)

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("BOT_TOKEN environment variable not set")


async def post_init(app) -> None:
    # jobs live only in memory; recreate them after every restart
    await reschedule_user_jobs(app)


def main() -> None:
    db_create()

    app = Application.builder().token(TOKEN).post_init(post_init).build()

    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(buttons_control)],
        states={
            LOW: [MessageHandler(filters.Regex(r"^(\d+(\.\d+)?)$"), border_low)],
            HIGH: [MessageHandler(filters.Regex(r"^(\d+(\.\d+)?)$"), border_high)],
            CURRENT: [MessageHandler(filters.Regex(r"^(\d+(\.\d+)?)$"), current_btc)],
        },
        fallbacks=[MessageHandler(filters.TEXT & ~filters.COMMAND, wrong_conv)],
        allow_reentry=True,
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("register", register))
    app.add_handler(CommandHandler("help", help_output))
    app.add_handler(CommandHandler("menu", main_menu))
    app.add_handler(conv_handler)

    print("Starting BTC ticker bot")
    app.run_polling()


if __name__ == "__main__":
    main()
