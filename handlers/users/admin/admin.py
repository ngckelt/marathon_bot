from aiogram import types
from loader import dp

from utils.doc.get_doc import create_document

from filters.admin_chat import AdminOnly


@dp.message_handler(AdminOnly(), commands=['doc'])
async def send_doc(message: types.Message):
    document = await create_document()
    await message.answer("Готовлю документ")
    await message.answer_document(open(document, 'rb'))


@dp.message_handler(AdminOnly(), content_types=types.ContentType.DOCUMENT)
async def get_document_id(message: types.Message):
    document_id = message.document.file_id
    await message.reply(text=f'Вот id этого документа:\n{document_id}')


@dp.message_handler(AdminOnly(), content_types=types.ContentType.PHOTO)
async def get_photo_id(message: types.Message):
    photo_id = message.photo[-1].file_id
    await message.reply(text=f'ID фотографии: \n{photo_id}')


@dp.message_handler(AdminOnly(), content_types=types.ContentType.VIDEO)
async def get_video_id(message: types.Message):
    video_id = message.video.file_id
    await message.reply(text=f'ID видеоролика: \n{video_id}')

