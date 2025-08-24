from aiogram import Router
from aiogram.types import Message

from lexicon.lexicon import LEXICON_RU

other_router = Router()


# react to other messages
@other_router.message()
async def process_other_message(message: Message):
    await message.reply(text=LEXICON_RU["other_message"])
