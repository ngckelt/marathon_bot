import json
import time
from datetime import datetime

from aiogram import types
from loader import dp, bot

from filters.group_chat import GroupOnly
from filters.admin_chat import AdminOnly


@dp.message_handler(AdminOnly(), GroupOnly(), text="!update_group_id")
async def update_group_id(message: types.Message):
    with open('utils/group_id.json', 'w') as f:
        data = {'group_id': message.chat.id}
        f.write(json.dumps(data))


