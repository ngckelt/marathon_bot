from loader import bot
from re import findall

from utils.db_api.db import ModeratorsModel


def only_cyrillic(string: str) -> bool:
    cyrillic_count = findall(string=string, pattern="[а-яА-Я]")
    return len(cyrillic_count) == len(string)


def correct_msk_timedelta(msk_timedelta: str) -> bool:
    try:
        msk_timedelta = int(msk_timedelta)
        if msk_timedelta in range(-24, 24):
            return True
        return False
    except:
        return False


async def notify_moderator_about_new_marathon_member(first_name, last_name, username, phone):
    moderator = await ModeratorsModel.get_moderator()
    message = f"{first_name} {last_name} зарегистрировался на марафон\n" \
              f"Контактная информация:\n" \
              f"Юзернейм: {username}\n" \
              f"Телефон: {phone}"
    try:
        await bot.send_message(
            chat_id=moderator.telegram_id,
            text=message
        )
    except:
        ...


