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
async def process_start_command(message: Message):
    await message.answer(text=LEXICON_RU[message.text])


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


# react when user sent age
@fill_form_router.message(
    StateFilter(FSMFillForm.fill_age),
    lambda x: x.text.isdigit() and 4 <= int(x.text) <= 120,
)
async def process_sent_age(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU["valid_age"], reply_markup=sex_kb)
    await state.update_data(age=message.text)
    await state.set_state(FSMFillForm.fill_sex)


# react when user sent sex
@fill_form_router.callback_query(
    StateFilter(FSMFillForm.fill_sex), F.data.in_(["male", "female"])
)
async def process_sent_sex(callback: CallbackQuery, state: FSMContext):
    await callback.answer(text=LEXICON_RU[callback.data])
    await callback.message.answer(text=LEXICON_RU["valid_sex"], reply_markup=contact_kb)
    await state.update_data(sex=callback.data)
    await state.set_state(FSMFillForm.send_contact)


# react when user sent contact or refused
@fill_form_router.message(
    StateFilter(FSMFillForm.send_contact),
    F.text.in_(["contact_send", "contact_not_send"]),
)
async def process_sent_contact(message: Message, state: FSMContext, db: dict):
    await message.answer(text=LEXICON_RU["valid_contact"])
    if message.contact is not None:
        await state.update_data(phone_number=message.contact.phone_number)
    db[message.from_user.id] = await state.get_data()
    state.clear()
