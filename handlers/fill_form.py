from copy import deepcopy

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

from fsm_classes.fsm_classes import FSMFillForm
from keyboards.form_kb import sex_kb, contact_kb
from lexicon.lexicon import LEXICON_RU


fill_form_router = Router()


# react to command /start
@fill_form_router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message, db: dict):
    await message.answer(text=LEXICON_RU[message.text])
    if message.from_user.id not in db["users"]:
        db["users"][message.from_user.id] = deepcopy(db.get("user_template"))


# react to command /help
@fill_form_router.message(Command(commands="help"))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_RU[message.text])


# react to command /cancel in FSMContext
@fill_form_router.message(Command(commands="cancel"), ~StateFilter(default_state))
async def process_cancel_command(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU[message.text])
    await state.clear()


# react to command /fillform
@fill_form_router.message(Command(commands="fillform"), StateFilter(default_state))
async def process_fillform_command(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU[message.text])
    await state.set_state(FSMFillForm.fill_name)


# react when user sent name
@fill_form_router.message(StateFilter(FSMFillForm.fill_name), F.text.isalpha())
async def process_sent_name(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU["valid_name"])
    await state.update_data(name=message.text)
    await state.set_state(FSMFillForm.fill_age)
