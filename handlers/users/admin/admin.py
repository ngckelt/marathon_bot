from aiogram import types
from loader import dp

from utils.doc.get_doc import create_document

from environs import Env
env = Env()
env.read_env()


@dp.message_handler(commands=['doc'])
async def send_doc(message: types.Message):
    document = await create_document()
    await message.answer("Готовлю документ")
    await message.answer_document(open(document, 'rb'))


@dp.message_handler(content_types=types.ContentType.DOCUMENT)
async def get_document_id(message: types.Message):
    if str(message.from_user.id) in env.str("ADMINS").split():
        document_id = message.document.file_id
        await message.reply(text=f'Вот id этого документа:\n{document_id}')
    else:
        await message.answer("Неизвестный запрос")


@dp.message_handler(content_types=types.ContentType.PHOTO)
async def get_photo_id(message: types.Message):
    if str(message.from_user.id) in env.str("ADMINS").split():
        photo_id = message.photo[-1].file_id
        await message.reply(text=f'ID фотографии: \n{photo_id}')
        with open('photo_id.txt', 'w') as f:
            f.write(photo_id)
    else:
        await message.answer("Неизвестный запрос")


@dp.message_handler(content_types=types.ContentType.VIDEO)
async def get_video_id(message: types.Message):
    if str(message.from_user.id) in env.str("ADMINS").split():
        video_id = message.video.file_id
        await message.reply(text=f'ID видеоролика: \n{video_id}')
    else:
        await message.answer("Неизвестный запрос")

