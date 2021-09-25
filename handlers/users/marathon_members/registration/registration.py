from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from loader import dp

from states.registration.registration import RegisterMarathonMember
from keyboards.inline.wakeup_time_markup import wakeup_time_markup, wakeup_time_callback

from utils.db_api.db import MarathonMembersModel
from handlers.users.utils.registration_utils import correct_msk_timedelta, only_cyrillic


# @dp.message_handler(CommandStart())
# async def start_registration(message: types.Message):
#     await message.answer("Приветствуем 👋\nКак Вас зовут?")
#     await RegisterMarathonMember.get_name.set()


@dp.message_handler(state=RegisterMarathonMember.get_name)
async def get_name(message: types.Message, state: FSMContext):
    name = message.text
    if only_cyrillic(name):
        await state.update_data(name=name)
        await message.answer(
            text="Выберите желаемое время подъема",
            reply_markup=wakeup_time_markup()
        )
        await RegisterMarathonMember.get_wakeup_time.set()
    else:
        await message.answer("Имя может содержать только кириллицу")


@dp.callback_query_handler(wakeup_time_callback.filter(), state=RegisterMarathonMember.get_wakeup_time)
async def get_wakeup_time(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    wakeup_time = callback_data.get('wakeup_time')
    await state.update_data(wakeup_time=wakeup_time)
    await callback.message.answer(
        "Укажите разницу во врмени с москвой:\n\n"
        "- если Ваше время <b>опережает</b> московское на <b>2 часа</b>, укажите <b>2</b>\n\n"
        "- если Ваше время <b>отстает</b> от Московского на <b>3 часа</b>, "
        "укажите <b>-3</b>\n\n"
        "- если Ваше время <b>равно</b> московскому, укажите <b>0</b>"
    )
    await RegisterMarathonMember.get_msk_timedelta.set()


@dp.message_handler(state=RegisterMarathonMember.get_msk_timedelta)
async def get_msk_timedelta(message: types.Message, state: FSMContext):
    msk_timedelta = message.text
    if correct_msk_timedelta(msk_timedelta):
        state_data = await state.get_data()
        await MarathonMembersModel.add_marathon_member(
            telegram_id=message.from_user.id,
            username=message.from_user.username,
            msk_timedelta=msk_timedelta,
            name=state_data.get('name').capitalize(),
            wakeup_time=state_data.get('wakeup_time')
        )

        await message.answer("Регистрация успешно завершена! С завтрашнего дня Вам необходимо будет присылать отчеты")
        await state.finish()
    else:
        await message.answer("Недопустимый диапазон разницы во времени")



