from aiogram.dispatcher.filters.state import StatesGroup, State


class AdminState(StatesGroup):
    get_chat_link = State()


