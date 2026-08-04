from telegram import Update
from telegram.ext import ContextTypes

from handlers.images import process_image


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    option = query.data

    await query.edit_message_text(
        "⏳ Processing..."
    )

    await process_image(
        option,
        update,
        context,
    )