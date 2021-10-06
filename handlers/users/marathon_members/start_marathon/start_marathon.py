from aiogram import types
from loader import dp
from keyboards.default.marathon_members.main_markup import main_markup
from utils.db_api.db import MarathonMembersModel


@dp.message_handler(text="Начать марафон")
async def start_marathon(message: types.Message):
    marathon_member = await MarathonMembersModel.get_marathon_member(message.from_user.id)
    if marathon_member is None:
        await MarathonMembersModel.update_marathon_member(message.from_user.id, on_marathon=True)
        await message.answer(
            text="Марафон начался. С завтрашнего дня тебе нужно будет присылать отчеты",
            reply_markup=main_markup
        )
    else:
        await message.answer("Вы уже участвуете в марафоне")





