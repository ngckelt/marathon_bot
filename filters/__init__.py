from aiogram import Dispatcher

from loader import dp
from .group_chat import GroupOnly
from .admin_chat import AdminOnly

from loader import dp


def setup(dp: Dispatcher):
    dp.filters_factory.bind(GroupOnly)
    dp.filters_factory.bind(AdminOnly)

# if __name__ == "filters":
#     dp.filters_factory.bind(IsGroup)
    # dp.filters_factory.bind(is_admin)
    # dp.filters_factory.bind(IsPrivate)
