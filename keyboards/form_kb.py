from aiogram.types import (
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    KeyboardButton,
)

from lexicon.lexicon import LEXICON_RU


sex_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=LEXICON_RU["male"], callback_data="male"),
            InlineKeyboardButton(text=LEXICON_RU["female"], callback_data="female"),
        ]
    ]
)

contact_kb = ReplyKeyboardMarkup(
    keyboard=[
        KeyboardButton(text=LEXICON_RU["send_contact"], request_contact=True),
        KeyboardButton(text=LEXICON_RU["not_send_contact"]),
    ],
    resize_keyboard=True,
    input_field_placeholder=LEXICON_RU["just_click"],
)
