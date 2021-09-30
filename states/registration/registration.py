from aiogram.dispatcher.filters.state import StatesGroup, State


class RegisterMarathonMember(StatesGroup):
    get_full_name = State()
    get_phone = State()
    is_msk = State()
    get_msk_timedelta = State()
    get_wakeup_time = State()


