from telegram import Update
from telegram.ext import ContextTypes

from database import (
    add_user,
    total_users,
    total_images,
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    add_user(update.effective_user)

    text = (
        "👋 Welcome to MODEX Background Remover!\n\n"
        "Send me a photo or image file.\n\n"
        "I'll remove the background or replace it."
    )

    await update.message.reply_text(text)


async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):

    users = total_users()
    images = total_images()

    text = (
        "📊 MODEX Background Remover\n\n"
        f"👥 Users: {users}\n"
        f"🖼 Images Processed: {images}"
    )

    await update.message.reply_text(text)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = (
        "🆘 Help\n\n"
        "Send any image.\n\n"
        "Available options:\n"
        "🟢 Remove Background\n"
        "⚪ White Background\n"
        "⚫ Black Background\n"
        "🔵 Blue Background\n"
        "🟥 Red Background\n"
        "🖼 Replace Background"
    )

    await update.message.reply_text(text)