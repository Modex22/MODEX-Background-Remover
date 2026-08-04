import os
import uuid

from telegram import Update
from telegram.ext import ContextTypes

from keyboards import image_options

TEMP_FOLDER = "temp"


async def receive_image(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # -------------------------
    # Receive replacement background
    # -------------------------

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

        await update.message.reply_text(
            "✅ Background received.\n\n"
            "Now press the Replace Background button again."
        )

        return

    # -------------------------
    # Receive subject image
    # -------------------------

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
        "Choose an option:",
        reply_markup=image_options(),
    )

from database import increment_images
from image_utils import (
    remove_background,
    add_background,
    replace_background,
    load_image,
    save_image,
)


async def process_image(option, update, context):

    image_path = context.user_data.get("image")

    if not image_path:

        await update.effective_message.reply_text(
            "❌ Please send an image first."
        )

        return

    if not os.path.exists(image_path):

        await update.effective_message.reply_text(
            "❌ Image not found."
        )

        return

    subject = remove_background(image_path)

    # -------------------------
    # Transparent
    # -------------------------

    if option == "remove_bg":

        result = subject

    # -------------------------
    # White
    # -------------------------

    elif option == "white_bg":

        result = add_background(
            subject,
            (255, 255, 255, 255)
        )

    # -------------------------
    # Black
    # -------------------------

    elif option == "black_bg":

        result = add_background(
            subject,
            (0, 0, 0, 255)
        )

    # -------------------------
    # Blue
    # -------------------------

    elif option == "blue_bg":

        result = add_background(
            subject,
            (0, 102, 255, 255)
        )

    # -------------------------
    # Red
    # -------------------------

    elif option == "red_bg":

        result = add_background(
            subject,
            (255, 0, 0, 255)
        )

    # -------------------------
    # Replace Background
    # -------------------------

    elif option == "replace_bg":

        background_path = context.user_data.get("background")

        if not background_path:

            context.user_data["waiting_background"] = True

            await update.effective_message.reply_text(
                "🖼 Send me the image you want to use as the NEW background."
            )

            return

        background = load_image(background_path)

        result = replace_background(
            subject,
            background,
        )

    else:

        result = subject

    output_path = os.path.join(
        TEMP_FOLDER,
        f"{uuid.uuid4()}.png"
    )

    save_image(
        result,
        output_path,
    )

    with open(output_path, "rb") as image:

        await update.effective_message.reply_document(
            document=image,
            filename="background_removed.png",
        )

    increment_images()

    # -------------------------
    # Cleanup
    # -------------------------

    for path in (
        image_path,
        context.user_data.get("background"),
        output_path,
    ):

        if path and os.path.exists(path):
            os.remove(path)

    context.user_data.clear()    