from aiogram import Dispatcher

from loader import dp
from .group_chat import GroupOnly

from loader import dp


def setup(dp: Dispatcher):
    dp.filters_factory.bind(GroupOnly)


# if __name__ == "filters":
#     dp.filters_factory.bind(IsGroup)
    # dp.filters_factory.bind(is_admin)
    # dp.filters_factory.bind(IsPrivate)
