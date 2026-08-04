from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def image_options():
    keyboard = [
        [
            InlineKeyboardButton(
                "🟢 Remove Background",
                callback_data="remove_bg",
            )
        ],
        [
            InlineKeyboardButton(
                "⚪ White Background",
                callback_data="white_bg",
            ),
            InlineKeyboardButton(
                "⚫ Black Background",
                callback_data="black_bg",
            ),
        ],
        [
            InlineKeyboardButton(
                "🔵 Blue Background",
                callback_data="blue_bg",
            ),
            InlineKeyboardButton(
                "🟥 Red Background",
                callback_data="red_bg",
            ),
        ],
        [
            InlineKeyboardButton(
                "🖼 Replace Background",
                callback_data="replace_bg",
            )
        ],
    ]

    return InlineKeyboardMarkup(keyboard)