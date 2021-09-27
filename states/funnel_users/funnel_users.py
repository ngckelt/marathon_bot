from aiogram.dispatcher.filters.state import StatesGroup, State


class FunnelUsers(StatesGroup):
    try_wakeup = State()
    are_they_right = State()
    has_idea = State()
    lets_try = State()
    is_interested = State()
    about_author = State()
    instruction = State()

    



