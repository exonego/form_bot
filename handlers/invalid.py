from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

from keyboards.form_kb import contact_kb
from fsm_classes.fsm_classes import FSMFillForm
from lexicon.lexicon import LEXICON_RU

invalid_router = Router()


# react to command /cancel not in FSMContext
@invalid_router.message(Command("cancel"), StateFilter(default_state))
async def process_invalid_cancel(message: Message):
    await message.answer(text=LEXICON_RU["cancel_not_in_fsm"])


# react to command /showform in FSMContext
@invalid_router.message(Command("showform"), ~StateFilter(default_state))
async def process_invalid_showform(message: Message):
    await message.answer(text=LEXICON_RU["showform_in_fsm"])


# react to incorrect name
@invalid_router.message(StateFilter(FSMFillForm.fill_name))
async def process_invalid_name(message: Message):
    await message.answer(text=LEXICON_RU["invalid_name"])


# react to incorrect age
@invalid_router.message(StateFilter(FSMFillForm.fill_age))
async def process_invalid_age(message: Message):
    await message.answer(text=LEXICON_RU["invalid_age"])


# react to incorrect sex
@invalid_router.message(StateFilter(FSMFillForm.fill_sex))
async def process_invalid_sex(message: Message):
    await message.answer(text=LEXICON_RU["invalid_sex"])


# react to incorrect contact
@invalid_router(StateFilter(FSMFillForm.send_contact))
async def process_invalid_contact(message: Message):
    await message.answer(text=LEXICON_RU["invalid_contact"], reply_markup=contact_kb)
