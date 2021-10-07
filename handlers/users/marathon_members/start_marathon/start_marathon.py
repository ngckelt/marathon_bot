from aiogram import types
from loader import dp
from keyboards.default.marathon_members.main_markup import main_markup
from utils.db_api.db import MarathonMembersModel


@dp.message_handler(text="Начать челлендж")
async def start_marathon(message: types.Message):
    marathon_member = await MarathonMembersModel.get_marathon_member(message.from_user.id)
    if marathon_member is not None:
        if not marathon_member.on_marathon:
            await MarathonMembersModel.update_marathon_member(message.from_user.id, on_marathon=True)
            await message.answer(
                text="Челлендж начался. С завтрашнего дня тебе нужно будет присылать отчеты",
                reply_markup=main_markup
            )
        else:
            await message.answer("Вы уже участвуете в челлендже")
    else:
        await message.answer("Для начала зарегистрируйтесь в боте")





