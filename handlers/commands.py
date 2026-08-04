from telegram import Update
from telegram.ext import ContextTypes

from database import (
    add_user,
    total_users,
    total_images,
)

from keyboards import main_keyboard


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    add_user(update.effective_user)

    text = (
        "👋 Welcome to MODEX Background Remover!\n\n"
        "Send me any image to begin.\n\n"
        "Then choose what you want to do from the menu below."
    )

    await update.message.reply_text(
        text,
        reply_markup=main_keyboard(),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = (
        "❓ How to use MODEX Background Remover\n\n"

        "1️⃣ Send an image.\n\n"

        "2️⃣ Choose one of the options below:\n"
        "🪄 Remove Background\n"
        "⚪ White Background\n"
        "⚫ Black Background\n"
        "🔵 Blue Background\n"
        "🔴 Red Background\n"
        "🖼 Replace Background\n\n"

        "3️⃣ If you choose Replace Background,\n"
        "the bot will ask you to send the new background image.\n\n"

        "Your final image will be sent as a high-quality PNG."
    )

    await update.message.reply_text(
        text,
        reply_markup=main_keyboard(),
    )


async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):

    users = total_users()
    images = total_images()

    text = (
        "📊 MODEX Background Remover\n\n"
        f"👥 Total Users: {users}\n"
        f"🖼 Images Processed: {images}"
    )

    await update.message.reply_text(
        text,
        reply_markup=main_keyboard(),
    )