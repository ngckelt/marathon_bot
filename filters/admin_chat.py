from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from utils.db_api.db import ModeratorsModel


class AdminOnly(BoundFilter):

    async def check(self, message: types.Message) -> bool:
        moderator = await ModeratorsModel.get_moderator()
        return str(message.from_user.id) == moderator.telegram_id



