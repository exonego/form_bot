from aiogram.fsm.state import State, StatesGroup


class FSMFillForm(StatesGroup):
    fill_name = State()
    fill_age = State()
    fill_sex = State()