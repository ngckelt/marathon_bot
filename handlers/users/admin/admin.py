from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp

from utils.doc.get_doc import create_document

from filters.admin_chat import AdminOnly
from states.admin.admin_state import AdminState
from utils.chat_link.chat_link import update_chat_link


@dp.message_handler(AdminOnly(), commands=['doc'])
async def send_doc(message: types.Message):
    if message.chat.type == types.ChatType.PRIVATE:
        document = await create_document()
        await message.answer("Готовлю документ")
        await message.answer_document(open(document, 'rb'))


@dp.message_handler(AdminOnly(), content_types=types.ContentType.DOCUMENT)
async def get_document_id(message: types.Message):
    if message.chat.type == types.ChatType.PRIVATE:
        document_id = message.document.file_id
        await message.reply(text=f'Вот id этого документа:\n{document_id}')


@dp.message_handler(AdminOnly(), content_types=types.ContentType.PHOTO)
async def get_photo_id(message: types.Message):
    if message.chat.type == types.ChatType.PRIVATE:
        photo_id = message.photo[-1].file_id
        await message.reply(text=f'ID фотографии: \n{photo_id}')


@dp.message_handler(AdminOnly(), content_types=types.ContentType.VIDEO)
async def get_video_id(message: types.Message):
    if message.chat.type == types.ChatType.PRIVATE:
        video_id = message.video.file_id
        await message.reply(text=f'ID видеоролика: \n{video_id}')


@dp.message_handler(AdminOnly(), commands=['update_chat_link'])
async def get_chat_link(message: types.Message):
    if message.chat.type == types.ChatType.PRIVATE:
        await message.answer("Пришли новую ссылку на групповой чат")
        await AdminState.get_chat_link.set()


@dp.message_handler(AdminOnly(), state=AdminState.get_chat_link)
async def get_chat_link(message: types.Message, state: FSMContext):
    if message.chat.type == types.ChatType.PRIVATE:
        chat_link = message.text
        update_chat_link(chat_link)
        await message.answer("Ссылка на чат успешно обновлена")
        await state.finish()