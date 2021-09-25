from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp

from keyboards.default.funnel_users import funnel_users_markups
from keyboards.inline.funnel_users import funnel_users_markups as inline_funnel_users_markups

from states.funnel_users.funnel_users import FunnelUsers


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
        reply_markup=funnel_users_markups.yes_and_no_markup
    )
    await FunnelUsers.is_interested.set()


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(
        f"Привет, {message.from_user.first_name} 👋\n"
        f"Раз ты перешел(а) по этой ссылке - значит тебе интересны ранние подъёмы."
        f"Что-то тебя в них привлекает. Ты хочешь испытать это чувство, когда ты встал, а весь мир ещё спит. "
        f"Или ты просто любопытничаешь, приоткрываешь дверку, чтобы посмотреть: “А смогу ли я? Получится? "
        f"Надо ли мне?” Одно знаю точно: ничего не бывает просто так. И если ты здесь, то в твоём пространстве "
        f"вариантов точно есть ТЫ"
        f"который(ая) встает в 5 утра и кайфует от этого",
        reply_markup=funnel_users_markups.try_wakeup_markup
    )

    await FunnelUsers.try_wakeup.set()


@dp.message_handler(state=FunnelUsers.try_wakeup)
async def try_wakeup(message: types.Message, state: FSMContext):
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
                             reply_markup=funnel_users_markups.are_they_right_markup
                             )
        await FunnelUsers.are_they_right.set()
        return
    else:
        await message.answer('Пожалуйста, выбери один из вариантов ответа')

    await FunnelUsers.has_idea.set()


@dp.message_handler(state=FunnelUsers.are_they_right)
async def are_they_right(message: types.Message, state: FSMContext):
    await has_idea(message, state)
    await FunnelUsers.has_idea.set()


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
        reply_markup=funnel_users_markups.interested_markup
    )
    await FunnelUsers.about_author.set()


@dp.message_handler(state=FunnelUsers.has_idea)
async def has_idea_get_answer(message: types.Message, state: FSMContext):
    text = message.text
    if text == 'ДА':
        await message.answer("Ура! Поздравляю с отличным решением, которое изменит твою жизнь к лучшему.")
        await is_interested(message, state)
    elif text == "НЕТ":
        await message.answer("Ты наверно думаешь это непосильная задача. Позволь, ещё немного порассуждаем. "
                             "Возможно ты передумаешь.",
                             reply_markup=funnel_users_markups.lets_try_markup
                             )
        await FunnelUsers.lets_try.set()


@dp.message_handler(state=FunnelUsers.lets_try)
async def lets_try(message: types.Message, state: FSMContext):
    await is_interested(message, state)


async def instruction(message: types.Message, state: FSMContext, author=False):

    markup = funnel_users_markups.are_you_ready_markup
    if author:
        markup = funnel_users_markups.are_you_ready_with_author_markup
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
    markup = funnel_users_markups.are_you_ready_markup
    if challenge_markup:
        markup = funnel_users_markups.how_challenge_works_markup
    # send photo
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
    text = message.text
    if text == "ДА, расскажи":
        await author_description(message, state, True)
    elif text == "Хочу узнать как это работает":
        await instruction(message, state, author=True)
        await state.finish()


@dp.message_handler(state=FunnelUsers.instruction)
async def send_instruction(message: types.Message, state: FSMContext):
    await instruction(message, state)
    await state.finish()


@dp.message_handler(text="Узнать о создателе челлендажа")
async def about_author_message(message: types.Message, state: FSMContext):
    await author_description(message, state,)



