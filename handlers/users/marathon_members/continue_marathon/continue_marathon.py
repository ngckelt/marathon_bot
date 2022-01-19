from aiogram import types
from loader import dp
from utils.db_api.db import MarathonMembersModel
from keyboards.inline.yes_or_no_markup import yes_or_no_callback
from utils.timestamps_manage.timestamps_manage import ask_to_continue_marathon, update_marathon_member
from utils.db_api.db import MarathonMembersModel


@dp.message_handler(commands=['ask'])
async def ask_test(message: types.Message):
    marathon_member = await MarathonMembersModel.get_marathon_member(message.from_user.id)
    await ask_to_continue_marathon(marathon_member)


@dp.callback_query_handler(yes_or_no_callback.filter(action='ask_to_continue_marathon'))
async def get_continue_marathon_answer(callback: types.CallbackQuery, callback_data: dict):
    await callback.answer()
    choice = callback_data.get('choice')
    if choice == 'yes':
        marathon_member = await MarathonMembersModel.get_marathon_member(callback.from_user.id)
        await update_marathon_member(marathon_member, on_marathon=True)
        await callback.message.answer("Челлендж продолжен")
    else:
        await callback.message.answer("Челлендж завершен")








