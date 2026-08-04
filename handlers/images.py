import os
import uuid

from telegram import Update
from telegram.ext import ContextTypes

from image_utils import (
    remove_background,
    add_background,
    replace_background,
    load_image,
    save_image,
)

from database import increment_images

TEMP_FOLDER = "temp"


async def receive_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Receives either:
    - The main image
    - A replacement background image
    """

    # ------------------------------------
    # Waiting for replacement background
    # ------------------------------------

    if context.user_data.get("waiting_background"):

        if update.message.photo:

            telegram_file = await update.message.photo[-1].get_file()
            extension = ".jpg"

        elif (
            update.message.document
            and update.message.document.mime_type
            and update.message.document.mime_type.startswith("image/")
        ):

            telegram_file = await update.message.document.get_file()

            filename = update.message.document.file_name or ""
            extension = os.path.splitext(filename)[1] or ".png"

        else:

            await update.message.reply_text(
                "❌ Please send an image."
            )

            return

        background_path = os.path.join(
            TEMP_FOLDER,
            f"{uuid.uuid4()}{extension}"
        )

        await telegram_file.download_to_drive(background_path)

        context.user_data["background"] = background_path
        context.user_data["waiting_background"] = False

        await update.message.reply_text(
            "✅ Background received.\n\n⏳ Processing..."
        )

        await process_image(
            "replace_bg",
            update,
            context,
        )

        return

    # ------------------------------------
    # Receive main image
    # ------------------------------------

    if update.message.photo:

        telegram_file = await update.message.photo[-1].get_file()
        extension = ".jpg"

    elif (
        update.message.document
        and update.message.document.mime_type
        and update.message.document.mime_type.startswith("image/")
    ):

        telegram_file = await update.message.document.get_file()

        filename = update.message.document.file_name or ""
        extension = os.path.splitext(filename)[1] or ".png"

    else:

        await update.message.reply_text(
            "❌ Please send an image."
        )

        return

    image_path = os.path.join(
        TEMP_FOLDER,
        f"{uuid.uuid4()}{extension}"
    )

    await telegram_file.download_to_drive(image_path)

    context.user_data["image"] = image_path

    await update.message.reply_text(
        "✅ Image received!\n\nChoose an option from the menu below."
    )


async def handle_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text

    mapping = {
        "🪄 Remove Background": "remove_bg",
        "⚪ White Background": "white_bg",
        "⚫ Black Background": "black_bg",
        "🔵 Blue Background": "blue_bg",
        "🔴 Red Background": "red_bg",
        "🖼 Replace Background": "replace_bg",
    }

    if text == "📊 Stats":
        from handlers.commands import stats
        await stats(update, context)
        return

    if text == "❓ Help":
        from handlers.commands import help_command
        await help_command(update, context)
        return

    option = mapping.get(text)

    if option is None:
        return

    await process_image(
        option,
        update,
        context,
    )

async def process_image(
    option: str,
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    image_path = context.user_data.get("image")

    if not image_path:

        await update.message.reply_text(
            "❌ Please send an image first."
        )

        return

    if not os.path.exists(image_path):

        await update.message.reply_text(
            "❌ Image not found."
        )

        return

    # -----------------------------
    # Remove background
    # -----------------------------

    try:

        subject = remove_background(image_path)

    except Exception as e:

        await update.message.reply_text(
            f"❌ Error:\n{e}"
        )

        return

    # -----------------------------
    # Choose output
    # -----------------------------

    if option == "remove_bg":

        result = subject

    elif option == "white_bg":

        result = add_background(
            subject,
            (255, 255, 255, 255),
        )

    elif option == "black_bg":

        result = add_background(
            subject,
            (0, 0, 0, 255),
        )

    elif option == "blue_bg":

        result = add_background(
            subject,
            (0, 102, 255, 255),
        )

    elif option == "red_bg":

        result = add_background(
            subject,
            (255, 0, 0, 255),
        )

    elif option == "replace_bg":

        background_path = context.user_data.get("background")

        if background_path is None:

            context.user_data["waiting_background"] = True

            await update.message.reply_text(
                "🖼 Send me the background image."
            )

            return

        if not os.path.exists(background_path):

            await update.message.reply_text(
                "❌ Background image not found."
            )

            context.user_data.clear()

            return

        background = load_image(background_path)

        result = replace_background(
            subject,
            background,
        )

    else:

        result = subject

    # -----------------------------
    # Save
    # -----------------------------

    output_path = os.path.join(
        TEMP_FOLDER,
        f"{uuid.uuid4()}.png",
    )

    save_image(
        result,
        output_path,
    )

    # -----------------------------
    # Send
    # -----------------------------

    with open(output_path, "rb") as photo:

        await update.message.reply_document(
            document=photo,
            filename="MODEX_Background_Remover.png",
            caption="✅ Finished!",
        )

    increment_images()

    # -----------------------------
    # Cleanup
    # -----------------------------

    files = [
        image_path,
        context.user_data.get("background"),
        output_path,
    ]

    for file in files:

        if file and os.path.exists(file):

            try:
                os.remove(file)
            except Exception:
                pass

    context.user_data.clear()

    await update.message.reply_text(
        "✨ Done!\n\n"
        "Send another image whenever you're ready."
    )