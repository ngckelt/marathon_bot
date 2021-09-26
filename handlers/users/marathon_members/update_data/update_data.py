from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp

from keyboards.inline.wakeup_time_markup import wakeup_time_markup, wakeup_time_callback
from states.registration.update_data import UpdateMarathonMember
from utils.db_api.db import MarathonMembersModel


@dp.message_handler(text="Изменить время подъема 🕣")
async def start_update_wakeup_time(message: types.Message):
    await message.answer(
        text="Выберите новое время подъема",
        reply_markup=wakeup_time_markup()
    )
    await UpdateMarathonMember.update_wakeup_time.set()


@dp.callback_query_handler(wakeup_time_callback.filter(), state=UpdateMarathonMember.update_wakeup_time)
async def update_wakeup_time(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    wakeup_time = callback_data.get('wakeup_time')
    await MarathonMembersModel.update_marathon_member(
        telegram_id=callback.from_user.id,
        wakeup_time=wakeup_time
    )
    await callback.message.answer("Время подъема успешно изменено!")
    await state.finish()



