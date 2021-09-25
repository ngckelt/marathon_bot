from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

try_wakeup_markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=f"Да, было дело"),
            KeyboardButton(text=f"НЕТ, но хочу попробовать"),
        ],
        [
            KeyboardButton(text=f"Пробовал(а), но не получается"),
            KeyboardButton(text=f"Я не сумасшедший"),
        ],
    ],
    resize_keyboard=True
)

are_they_right_markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=f"В этом что-то есть"),
            KeyboardButton(text=f"Безумцы )"),
        ],
    ],
    resize_keyboard=True
)

yes_and_no_markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=f"ДА"),
            KeyboardButton(text=f"НЕТ"),
        ],
    ],
    resize_keyboard=True
)

lets_try_markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=f"Согласен"),
            KeyboardButton(text=f"Давай попробуем"),
        ],
    ],
    resize_keyboard=True
)

interested_markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=f"ДА, расскажи"),
            KeyboardButton(text=f"Хочу узнать как это работает"),
        ],
    ],
    resize_keyboard=True
)

how_challenge_works_markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=f"Узнать как работает Челлендж"),
        ],
    ],
    resize_keyboard=True
)

are_you_ready_markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=f"Попробовать 3 дня челленджа"),
            KeyboardButton(text=f"Посмотреть Отзывы"),
        ],
    ],
    resize_keyboard=True
)

are_you_ready_with_author_markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=f"Попробовать 3 дня челленджа"),
            KeyboardButton(text=f"Посмотреть Отзывы"),
        ],
        [
            KeyboardButton(text=f"Узнать о создателе челлендажа"),
        ],
    ],
    resize_keyboard=True
)



