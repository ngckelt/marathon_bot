from aiogram import types
from loader import dp

from utils.doc.get_doc import create_document


@dp.message_handler(commands=['doc'])
async def send_doc(message: types.Message):
    document = await create_document()
    await message.answer("Готовлю документ")
    await message.answer_document(open(document, 'rb'))



