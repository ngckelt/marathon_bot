import time
from pprint import pprint

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp

from keyboards.default.funnel_users import funnel_users_markups
from keyboards.default.funnel_users.funnel_users_markups import create_markup
from keyboards.inline.funnel_users import funnel_users_markups as inline_funnel_users_markups
from keyboards.inline.paginator import Paginator, pagination_callback

from utils.db_api.db import FunnelUsersModel, ReviewsModel, MarathonMembersModel

from states.funnel_users.funnel_users import FunnelUsers


async def update_funnel_user(message):
    await FunnelUsersModel.update_funnel_user(
        telegram_id=message.from_user.id,
        last_message=message.text,
        last_update_time=time.time()
    )


async def has_idea(message: types.Message, state: FSMContext):
    await message.answer(
        "Наверняка ты слышал(а) про людей, которые просыпаются в 5 утра, и это помогает им достигать более высоких "
        "результатов во всех сферах жизни.\n"
        "✨ Продуктивнее работать и больше успевать\n"
        "✨ Чувствовать себя лучше и здоровее\n"
        "✨ Стать человеком с прокаченной силой воли\n"
        "✨ Стать психологически более устойчивым"
    )

    await message.answer(
        "Признавайся, есть ли у тебя идея внедрить привычку ежедневно просыпаться в 5-6 утра? 😉",
        reply_markup=create_markup(2, 'ДА', 'НЕТ')
    )
    await FunnelUsers.is_interested.set()


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message, state: FSMContext):
    marathon_member = await MarathonMembersModel.get_marathon_member(message.from_user.id)
    if marathon_member is None:
        await state.finish()
        await FunnelUsersModel.add_funnel_user(
            telegram_id=message.from_user.id,
            username=message.from_user.username,
            last_message='/start',
            last_update_time=time.time()
        )
        await message.answer(
            f"Привет, {message.from_user.first_name} 👋\n"
            f"Раз ты перешел(а) по этой ссылке - значит тебе интересны ранние подъёмы."
            f"Что-то тебя в них привлекает. Ты хочешь испытать это чувство, когда ты встал, а весь мир ещё спит. "
            f"Или ты просто любопытничаешь, приоткрываешь дверку, чтобы посмотреть: “А смогу ли я? Получится? "
            f"Надо ли мне?” Одно знаю точно: ничего не бывает просто так. И если ты здесь, то в твоём пространстве "
            f"вариантов точно есть ТЫ"
            f"который(ая) встает в 5 утра и кайфует от этого",
            reply_markup=create_markup(
                2, 'Да, было дело', 'НЕТ, но хочу попробовать', 'Пробовал(а), но не получается',
                'Я не сумасшедший',
            )
        )

        await FunnelUsers.try_wakeup.set()
    else:
        await message.answer("Ты уже использовал данную команду")


@dp.message_handler(state=FunnelUsers.try_wakeup)
async def try_wakeup(message: types.Message, state: FSMContext):
    await update_funnel_user(message)
    text = message.text
    if text == "Да, было дело":
        await message.answer('Ты молодец! Значит точно сможешь внедрить ранние подъёмы в свою жизнь на постоянной '
                             'основе. Как гласит известная фраза: “Не бойся, что не получается с первого раза. '
                             'Бойся, что не пробуешь”')
        await has_idea(message, state)
    elif text == "НЕТ, но хочу попробовать":
        await message.answer('Ура! Значит в тебе есть огромный потенциал внедрить эту уникальную привычку в свою жизнь.')
        await has_idea(message, state)
    elif text == "Пробовал(а), но не получается":
        await message.answer('Ты молодец! Значит точно сможешь внедрить ранние подъёмы в свою жизнь на постоянной '
                             'основе. Как гласит известная фраза: “Не бойся, что не получается с первого раза. '
                             'Бойся, что не пробуешь”')
        await has_idea(message, state)
    elif text == "Я не сумасшедший":
        await message.answer('Да, ты прав(а) 😁 Про сумасшедших')
        await message.answer('Как говорила Алиса, та самая из страны чудес: '
                             '“Так и есть — с ума сошла, спятила, чокнулась!.. Открою тебе секрет: безумцы всех '
                             'умней.”')
        await message.answer('А Вильям Шекспир считал, что “У всякого безумия есть своя логика”. Как думаешь, '
                             'они правы?',
                             reply_markup=create_markup(2, 'В этом что-то есть', 'Безумцы)')
                             )
        await FunnelUsers.are_they_right.set()
        return
    else:
        await message.answer('Пожалуйста, выбери один из вариантов ответа')
        return

    await FunnelUsers.has_idea.set()


@dp.message_handler(state=FunnelUsers.are_they_right)
async def are_they_right(message: types.Message, state: FSMContext):
    if message.text == 'В этом что-то есть' or message.text == 'Безумцы)':
        await update_funnel_user(message)
        await has_idea(message, state)
        await FunnelUsers.has_idea.set()
    else:
        await message.answer("Пожалуйста, выбери один из вариантов ответа")


async def is_interested(message: types.Message, state: FSMContext):
    await message.answer(
        "Ранние подъёмы - это привычка, которую внедрить в одиночку невероятно сложная задача. "
        "Кто пробовал - тот знает."
    )
    await message.answer("Бросаю тебе вызов и приглашаю в онлайн-челлендж по внедрению ранних подъемов 🕔✨")
    await message.answer(
        "С челленджем у тебя:\n\n"
        "🔥 Однозначно будет больше энергии\n"
        "🧠 Поменяются нейронные связи и дороги\n"
        "🚀 Увеличатся скорости и будешь больше успевать\n"
        "😍 Подтянется фигура\n"
        "🕔 Появится режим\n"
        "⚔️ Избавишься от прокрастинации\n"
        "📚 Начнёшь читать книги\n"
        "👥 Получишь мощную поддержку единомышленников\n"
        "✨Найдешь время для медитаций, тишины и инсайтов\n"
        "💪 Прокачаешь силу воли\n"
        "💪 Победишь лень и вечные отмазками.\n\n"
        "Ну как тебе предложение?\n\n"
        "Рассказать тебе побольше о нас?",
        reply_markup=create_markup(2, 'ДА, расскажи', 'Хочу узнать как это работает')
    )
    await FunnelUsers.about_author.set()


@dp.message_handler(state=FunnelUsers.has_idea)
async def has_idea_get_answer(message: types.Message, state: FSMContext):
    await update_funnel_user(message)
    text = message.text
    if text == 'ДА':
        await message.answer("Ура! Поздравляю с отличным решением, которое изменит твою жизнь к лучшему.")
        await is_interested(message, state)
    elif text == "НЕТ":
        await message.answer("Ты наверно думаешь это непосильная задача. Позволь, ещё немного порассуждаем. "
                             "Возможно ты передумаешь.",
                             reply_markup=create_markup(2, 'Согласен', 'Давай попробуем')
                             )
        await FunnelUsers.lets_try.set()
    else:
        await message.answer("Пожалуйста, выбери один из вариантов ответа")


@dp.message_handler(state=FunnelUsers.lets_try)
async def lets_try(message: types.Message, state: FSMContext):
    if message.text == 'Согласен' or message.text == 'Давай попробуем':
        await update_funnel_user(message)
        await is_interested(message, state)
    else:
        await message.answer("Пожалуйста, выбери один из вариантов ответа")


async def instruction(message: types.Message, state: FSMContext, author=False):
    markup = create_markup(2, 'Попробовать 3 дня челленджа', 'Посмотреть отзывы')
    if author:
        markup = create_markup(2, 'Попробовать 3 дня челленджа', 'Посмотреть отзывы', 'Узнать о создателе челлендажа')
    await message.answer(
        "КАК ВНЕДРЯЕТСЯ ПРИВЫЧКА\n"
        "Исследования гласят, что на внедрение привычки необходимо от 5 до 254 дней. Да 😳 Представляете какой разбег!\n"
        "Долгое время популярна была концепция 21 дня. Именно такое количество дней считалось необходимым для "
        "внедрения "
        "нового постоянного действия в жизнь.\n"
        "Я же последнее время считаю, что большинству людей недостаточно 21 дня. Мой опыт ведения клуба ранних "
        "подъёмов позволяет сделать такие выводы\n."
        "✔️ Первый цикл из 21 дня разрушается старая привычка поздних укладываний и привыкание психики к новому "
        "режиму\n "
        "✔️ Второй цикл из 21 дня формируется привычка.\n"
        "✔️ И в третий цикл 21 дня привычка закрепляется и и интегрируется в жизнь.\n"
        "Итого 63 дня!\n А в идеале, если следовать сакральному числу 108 и выдержать челлендж 108 дней, то вы уже "
        "никогда не сойдете с устойчивой нейронной связи 🔥"
    )

    await message.answer(
        "КАК ВСЁ УСТРОЕНО В ЧЕЛЛЕНДЖЕ\n"
        "Каждое (!) утро в 5:00 в общий чат участники отчитываются о пробуждении.\n"
        "Время может варьироваться от 4:00 до 5:10.\n\n"
        "Я рекомендую начинать свой первый час дня со следующих действий:\n\n"
        "🏃🏃‍♀️10-20 мин - спорт / физические упражнения или прогулка на улице\n"
        "🧘‍♀️💆‍♀️ 10-20 мин - медитация/аффирмации или другие ментальные/духовные практики\n"
        "📚 20 мин - чтение/саморазвитие.\n"
        "Умный бот учитывает ваши подъёмы и не даёт расслабиться и проспать. Ведь если проспишь и не отчитаешься - то "
        "это минус “одна жизнь”. А жизней в челлендже всего 3! 😳😁\n"
        "Здорово ведь в формате игры внедрять привычку в свою жизнь!"
    )

    await message.answer(
        "А ещё у тебя будет мощная поддержка ментора, единомышленников и доступ к огромной базе знаний, "
        "где ты сможешь изучить лекции про:\n"
        "📌 Биоритмы\n"
        "📌 Секреты эффективного сна\n"
        "📌 Фишки как рассчитать свой цикл сна\n"
        "📌 Связь питания и сна\n"
        "📌 Секреты фен-шуя спальни\n"
        "📌 Аффирмации\n"
        "📌 Введение в визуализацию\n"
        "📌 Как научиться самостоятельно медитировать\n"
        "А ещё получишь доступ:\n"
        "📌 Более 10 энергетическим и ментальным практикам\n"
        "📌 Подборка медитаций\n"
        "📌 Электронные книги по ранним подъёмам\n\n"
        "На самом деле это не все правила. Подробнее обо всём ты можешь узнать на пробных 3х днях челленджа.\n"
        "Ну что? Ты готов(а)?",
        reply_markup=markup
    )

    await state.finish()


async def author_description(message, state, challenge_markup=False):
    markup = create_markup(2, 'Попробовать 3 дня челленджа', 'Посмотреть отзывы')
    if challenge_markup:
        markup = create_markup(1, 'Как работает Челлендж')
    await message.answer_photo("https://scontent-hel3-1.cdninstagram.com/v/t51.2885-15/e35/242610079_223786276467332_8893897483567551067_n.jpg?_nc_ht=scontent-hel3-1.cdninstagram.com&_nc_cat=108&_nc_ohc=ZqfmVba4MwgAX8krTGT&edm=AABBvjUBAAAA&ccb=7-4&oh=9cb83421c74be6ceb854e4843063f675&oe=6158807C&_nc_sid=83d603")
    await message.answer(
        "Меня зовут Любовь Скабелина. Я встаю в 5 утра уже более 10 лет. "
        "Начала практиковать ранние подъёмы ещё когда Хэл Элрод про них не задумывался. Да, это автор "
        "бестселлера “Магия утра”. И Робин Шарма тоже ещё не написал свою знаменитую книгу “Клуб 5 утра”. Так что "
        "перед вами уникальный 😁  экземпляр человека, который по собственной воле и желанию решил вставать в 5 "
        "утра. Да ещё полюбил это дело и внедрил в свою жизнь на постоянной основе. "
        "Как я к этому пришла - это длинная история. Но ты можешь её прочитать в моём блоге",
        reply_markup=inline_funnel_users_markups.instagram_link_markup()
    )
    await message.answer(
        "В двух словах обо мне. Мне 33 года. Я практикующий коуч и без пяти минут психолог. "
        "Получаю сейчас третье высшее образование. Когда-то я мечтала стать переводчиком и первые 2 мои "
        "образования - это учитель истории и английского языка, а также англо-русский переводчик. Но жизнь так "
        "сложилась, что с 20 лет я предприниматель. В течение 9 лет у меня был успешный мини-маркет хозтоваров, "
        "который я продала полгода назад. Ибо готовлюсь к переезду в тёплый регион. А ещё было швейное "
        "производство и онлайн-магазин. Так что перед вами не просто блуждающий блогер 😄 А ещё я мать 4 детей 😳 "
        "Да, сама в шоке ))\n"
        "Присаживайся, проходи. Давай дружить ❤️",
        reply_markup=markup
    )
    await FunnelUsers.instruction.set()


@dp.message_handler(state=FunnelUsers.about_author)
async def about_author(message: types.Message, state: FSMContext):
    await update_funnel_user(message)
    text = message.text
    if text == "ДА, расскажи":
        await author_description(message, state, True)
    elif text == "Хочу узнать как это работает":
        await instruction(message, state, author=True)
        await state.finish()
    else:
        await message.answer("Пожалуйста, выбери один из вариантов ответа")


@dp.message_handler(state=FunnelUsers.instruction)
async def send_instruction(message: types.Message, state: FSMContext):
    if message.text == 'Как работает Челлендж':
        await update_funnel_user(message)
        await instruction(message, state)
        await state.finish()
    else:
        await message.answer("Пожалуйста, выбери один из вариантов ответа")


@dp.message_handler(text="Узнать о создателе челлендажа")
async def about_author_message(message: types.Message, state: FSMContext):
    await update_funnel_user(message)
    await author_description(message, state,)
    await state.finish()


@dp.message_handler(text="Посмотреть отзывы")
async def about_author_message(message: types.Message, state: FSMContext):
    await update_funnel_user(message)
    reviews = await ReviewsModel.get_reviews()

    album = types.MediaGroup()
    for review in reviews:
        if review.photo_id:
            album.attach_photo(review.photo_id)
        elif review.video_id:
            album.attach_video(review.video_id)

    await message.answer_media_group(
        media=album,
    )

    markup = Paginator('paginator', 'reviews').create_markup(
        max_items=len(reviews),
    )
    review = reviews[0]
    if review.photo_id:
        await message.answer_photo(
            photo=review.photo_id,
            reply_markup=markup
        )
    elif review.video_id:
        await message.answer_video(
            video=review.video_id,
            reply_markup=markup
        )

    await state.finish()


@dp.callback_query_handler(pagination_callback.filter(key='reviews', page='curr_page'))
async def curr_page(callback: types.CallbackQuery):
    await callback.answer(cache_time=60)


@dp.callback_query_handler(pagination_callback.filter(key='reviews'))
async def show_chosen_article(callback: types.CallbackQuery, callback_data: dict):
    await callback.answer()
    current_page = int(callback_data.get('page'))
    reviews = await ReviewsModel.get_reviews()
    review = reviews[current_page-1]

    markup = Paginator('paginator', 'reviews').create_markup(
        max_items=len(reviews),
        curr_page=current_page,
    )

    if review.photo_id:
        await callback.message.answer_photo(
            photo=review.photo_id,
            reply_markup=markup,
        )
    elif review.video_id:
        await callback.message.answer_video(
            video=review.video_id,
            reply_markup=markup,
        )

    await callback.message.delete()



