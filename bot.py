import os

from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
)

from config import BOT_TOKEN
from database import create_tables

from handlers.commands import (
    start,
    help_command,
    stats,
)

from handlers.images import (
    receive_image,
    handle_menu,
)

TEMP_FOLDER = "temp"


def main():

    # Create temp folder
    os.makedirs(TEMP_FOLDER, exist_ok=True)

    # Create database
    create_tables()

    # Create Telegram app
    app = Application.builder().token(BOT_TOKEN).build()

    # ------------------------
    # Commands
    # ------------------------

    app.add_handler(
        CommandHandler(
            "start",
            start,
        )
    )

    app.add_handler(
        CommandHandler(
            "help",
            help_command,
        )
    )

    app.add_handler(
        CommandHandler(
            "stats",
            stats,
        )
    )

    # ------------------------
    # Receive Images
    # ------------------------

    app.add_handler(
        MessageHandler(
            filters.PHOTO | filters.Document.IMAGE,
            receive_image,
        )
    )

    # ------------------------
    # Reply Keyboard Menu
    # ------------------------

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_menu,
        )
    )

    print("🤖 MODEX Background Remover is running...")

    app.run_polling()


if __name__ == "__main__":
    main()