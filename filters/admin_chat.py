from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from environs import Env

env = Env()
env.read_env()


class AdminOnly(BoundFilter):

    async def check(self, message: types.Message) -> bool:
        return str(message.from_user.id) in env.str("ADMINS").split()



