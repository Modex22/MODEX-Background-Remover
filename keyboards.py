from telegram import ReplyKeyboardMarkup


def main_keyboard():
    keyboard = [
        ["🪄 Remove Background", "🖼 Replace Background"],
        ["⚪ White Background", "⚫ Black Background"],
        ["🔵 Blue Background", "🔴 Red Background"],
        ["📊 Stats", "❓ Help"],
    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        one_time_keyboard=False,
        input_field_placeholder="Choose an option...",
    )