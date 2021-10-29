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

            text = "Челлендж начался. С завтрашнего дня тебе нужно будет присылать отчеты.\n\n" \
                   "Как учитывает бот. Время подъёма можно выбрать 5:00, 5:30, 6:00. Начиная с 4 утра и до +10 минут " \
                   "от выбранного вами времени подъёма надо прислать видео-сообщение в ЧАТ. Сказать что угодно " \
                   "(Доброе утро, к примеру) в более/менее светлом месте, не лёжа ) Спустя 1,5 часа от выбранного " \
                   "времени надо прислать второй отчёт в виде текста. Текст любой. Желательно список того, " \
                   "что полезного сделали с утра. \n\n" \
                   "После первого видео-сообщения бот ответит, какой день челленджа и напомнит о необходимости " \
                   "прислать второй отчёт. После второго отчёта - бот зачтёт день. В личные сообщения бот присылает " \
                   "мотивационные/поддерживающие сообщения после каждого засчитанного дня. \n\n" \
                   "За всё время челленджа (63 дня) допускается 3 дня пропуска. Если готовы участвовать в челлендже " \
                   "до конца - то есть разные тарифы участия, с которыми вы сможете ознакомиться после прохождения " \
                   "5 пробных дней"
            await message.answer(
                text=text,
                reply_markup=main_markup
            )
        else:
            await message.answer(
                text="Вы уже участвуете в челлендже",
                reply_markup=main_markup
            )
    else:
        await message.answer("Для начала зарегистрируйтесь в боте")





