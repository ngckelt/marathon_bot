from aiogram.dispatcher.filters.state import StatesGroup, State


class UpdateMarathonMember(StatesGroup):
    update_wakeup_time = State()


