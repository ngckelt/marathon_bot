from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp


@dp.message_handler(state="*", commands=['cancel'])
async def cancel_state(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Действие отменено")


