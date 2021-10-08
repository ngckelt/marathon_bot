from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from loader import dp

from states.registration.registration import RegisterMarathonMember
from keyboards.inline.wakeup_time_markup import wakeup_time_markup, wakeup_time_callback
from keyboards.inline.yes_or_no_markup import yes_or_no_markup, yes_or_no_callback
from keyboards.default.marathon_members.start_marathon import start_marathon_markup
from keyboards.default.marathon_members.registration_markups import request_contact_markup

from utils.db_api.db import MarathonMembersModel, FunnelUsersModel
from .utils import correct_msk_timedelta, only_cyrillic, notify_moderator_about_new_marathon_member

from keyboards.default.funnel_users.funnel_users_markups import restart_registration_markup
from utils.chat_link.chat_link import get_chat_link


@dp.message_handler(text="Начать регистрацию сначала 🔄", state=RegisterMarathonMember)
async def restart_registration(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(
        text="Напиши свое Имя и Фамилию",
        reply_markup=restart_registration_markup
    )
    await RegisterMarathonMember.get_full_name.set()


@dp.message_handler(text="Попробовать 3 дня челленджа")
async def start_registration(message: types.Message):
    marathon_member = await MarathonMembersModel.get_marathon_member(message.from_user.id)
    if marathon_member is None:
        await FunnelUsersModel.update_funnel_user(
            telegram_id=message.from_user.id,
            last_message="Попробовать 3 дня челленджа",
            on_marathon_registration=True
        )
        await message.answer(
            text="Отлично! Ты сделал правильный выбор! "
                 "А теперь, давай познакомимся. Как тебя зовут? "
                 "Напиши свое Имя и Фамилию",
            reply_markup=restart_registration_markup
        )
        await RegisterMarathonMember.get_full_name.set()
    else:
        await message.answer("Ты уже использовал эту команду")


@dp.message_handler(state=RegisterMarathonMember.get_full_name)
async def get_full_name(message: types.Message, state: FSMContext):
    try:
        first_name, last_name = message.text.split()
        if only_cyrillic(first_name) and only_cyrillic(last_name):
            await state.update_data(first_name=first_name, last_name=last_name)
            await message.answer(
                text="Пришли свой номер телефона, используя кнопку ниже. "
                     "Он нужен, чтобы с тобой мог связаться ментор челленджа",
                reply_markup=request_contact_markup
            )
            await RegisterMarathonMember.get_phone.set()
        else:
            await message.answer("Имя и фамилия могут содержать только кириллицу")
    except ValueError:
        await message.answer("Неверный формат входных данных")


@dp.message_handler(content_types=types.ContentTypes.CONTACT, state=RegisterMarathonMember.get_phone)
async def get_phone(message: types.Message, state: FSMContext):
    phone = message.contact.phone_number
    if message.contact.user_id == message.from_user.id:
        if phone[0] != '+':
            phone = '+' + phone

        await message.answer(
            text="Отлично",
            reply_markup=restart_registration_markup
        )
        await state.update_data(phone=phone)
        await message.answer(
            text="Выбери желаемое время подъема",
            reply_markup=wakeup_time_markup()
        )

        await RegisterMarathonMember.get_wakeup_time.set()
    else:
        await message.answer("Ай-ай-ай! Как нехорошо использовать чужой номер телефона! 😡")


@dp.callback_query_handler(wakeup_time_callback.filter(), state=RegisterMarathonMember.get_wakeup_time)
async def get_wakeup_time(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    wakeup_time = callback_data.get('wakeup_time')
    await state.update_data(wakeup_time=wakeup_time)

    await callback.message.answer(
        text="Твой часовой пояс совпадает с московским?",
        reply_markup=yes_or_no_markup('is_msk')
    )
    await RegisterMarathonMember.is_msk.set()


async def finish_registration(user_id, username, state):
    state_data = await state.get_data()
    await MarathonMembersModel.add_marathon_member(
        telegram_id=user_id,
        username=username,
        first_name=state_data.get('first_name').capitalize(),
        last_name=state_data.get('last_name').capitalize(),
        phone=state_data.get('phone'),
        msk_timedelta=state_data.get('msk_timedelta'),
        wakeup_time=state_data.get('wakeup_time')
    )
    await FunnelUsersModel.update_funnel_user(
        telegram_id=user_id,
        started_marathon=True,
        on_marathon_registration=False
    )
    await notify_moderator_about_new_marathon_member(
        first_name=state_data.get('first_name').capitalize(),
        last_name=state_data.get('last_name').capitalize(),
        username=username if username is not None else "Отсутствует",
        phone=state_data.get('phone')
    )


@dp.callback_query_handler(yes_or_no_callback.filter(action='is_msk'), state=RegisterMarathonMember.is_msk)
async def is_msk(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    choice = callback_data.get('choice')
    if choice == 'yes':
        await state.update_data(msk_timedelta='0')
        await finish_registration(callback.from_user.id, callback.from_user.username, state)
        await callback.message.answer(
            text="В ближайшие несколько часов с тобой свяжется ментор челленджа и подробнее расскажет как у нас всё "
                 "устроено. А пока лови ссылку на чат https://t.me/joinchat/Bb21nyN9t9wzYzFi. \nПрисоединяйся ❤️",
            reply_markup=start_marathon_markup
        )

        await callback.message.answer("Как будешь готов начать челлендж вернись сюда и нажми кнопку \"начать челлендж\","
                                      " утром следующего дня бот будет ждать первый отчет в чате по ссылке выше")
        await state.finish()
    else:
        await callback.message.answer(
            "Укажи разницу во врмени с Москвой, например:\n\n"
            "- если твое время <b>опережает</b> московское на <b>2 часа</b>, укажи <b>2</b>\n\n"
            "- если твое время <b>отстает</b> от Московского на <b>3 часа</b>, укажи <b>-3</b>\n\n"
        )
        await RegisterMarathonMember.get_msk_timedelta.set()


# https://t.me/joinchat/Bb21nyN9t9wzYzFi
@dp.message_handler(state=RegisterMarathonMember.get_msk_timedelta)
async def get_msk_timedelta(message: types.Message, state: FSMContext):
    msk_timedelta = message.text
    if correct_msk_timedelta(msk_timedelta):
        await state.update_data(msk_timedelta=msk_timedelta)
        await finish_registration(message.from_user.id, message.from_user.username, state)
        await message.answer(
            text="В ближайшие несколько часов с тобой свяжется ментор челленджа и подробнее расскажет как у нас всё "
                 f"устроено. А пока лови ссылку на чат {get_chat_link()}. \nПрисоединяйся ❤️",
            reply_markup=start_marathon_markup
        )
        await message.answer("Как будешь готов начать челлендж вернись сюда и нажми кнопку \"начать челлендж\","
                             " утром следующего дня бот будет ждать первый отчет в чате по ссылке выше")
        await state.finish()
    else:
        await message.answer("Недопустимый диапазон разницы во времени")


@dp.message_handler(state=RegisterMarathonMember.get_phone)
async def get_phone_error(message: types.Message, ):
    await message.answer("Пожалуйста, воспользуйся кнопкой ниже, чтобы отправить свой номер телефона")


@dp.message_handler(state=[
    RegisterMarathonMember.get_wakeup_time,
    RegisterMarathonMember.is_msk,
]
)
async def error(message: types.Message):
    await message.answer("Пожалуйста, выбери один из вариентов ответа")
