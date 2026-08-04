from io import BytesIO

from PIL import Image
from rembg import remove


def remove_background(input_path):
    """
    Remove the background from an image.
    Returns a transparent RGBA PIL Image.
    """

    with open(input_path, "rb") as file:
        input_bytes = file.read()

    output_bytes = remove(input_bytes)

    subject = Image.open(
        BytesIO(output_bytes)
    ).convert("RGBA")

    return subject


def add_background(subject, color):
    """
    Place the subject on a solid color background.
    """

    background = Image.new(
        "RGBA",
        subject.size,
        color
    )

    background.paste(
        subject,
        (0, 0),
        subject,
    )

    return background


def replace_background(subject, background):
    """
    Replace the background with another image.
    """

    background = background.convert("RGBA")

    background = background.resize(
        subject.size,
        Image.Resampling.LANCZOS
    )

    background.paste(
        subject,
        (0, 0),
        subject,
    )

    return background


def resize_image(image, size):
    """
    Resize an image while maintaining quality.
    """

    return image.resize(
        size,
        Image.Resampling.LANCZOS
    )


def crop_center(image, size):
    """
    Crop an image from the center.
    """

    width, height = image.size
    target_width, target_height = size

    left = (width - target_width) // 2
    top = (height - target_height) // 2

    right = left + target_width
    bottom = top + target_height

    return image.crop(
        (
            left,
            top,
            right,
            bottom,
        )
    )


def save_image(image, output_path):
    """
    Save image as PNG.
    """

    image.save(
        output_path,
        format="PNG",
    )


def load_image(path):
    """
    Open image as RGBA.
    """

    return Image.open(path).convert("RGBA")