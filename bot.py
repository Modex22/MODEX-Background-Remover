import os

from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)

from config import BOT_TOKEN
from database import create_tables

from handlers.commands import (
    start,
    stats,
    help_command,
)

from handlers.images import (
    receive_image,
)

from handlers.callbacks import (
    button,
)

TEMP_FOLDER = "temp"


def main():

    os.makedirs(TEMP_FOLDER, exist_ok=True)

    create_tables()

    app = Application.builder().token(BOT_TOKEN).build()

    # -----------------------
    # Commands
    # -----------------------

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("stats", stats))

    # -----------------------
    # Images
    # -----------------------

    app.add_handler(
        MessageHandler(
            filters.PHOTO | filters.Document.IMAGE,
            receive_image,
        )
    )

    # -----------------------
    # Inline Buttons
    # -----------------------

    app.add_handler(
        CallbackQueryHandler(button)
    )

    print("🤖 MODEX Background Remover is running...")

    app.run_polling()


if __name__ == "__main__":
    main()