from aiogram import types
from aiogram.dispatcher import FSMContext
from handlers.keyboard.keyboard import *
from loader import dp
from manager.manager import remove_json

from manager.models import Users


@dp.message_handler(text="/start", state='*')
async def command_start(message: types.Message, state: FSMContext):
    us = Users()
    us.create_table(safe=True)
    chat_id = message.chat.id
    if message.from_user.first_name:
        first_name = message.from_user.first_name
    else:
        first_name = None
    if message.from_user.last_name:
        last_name = message.from_user.last_name
    else:
        last_name = None
    chat = Users.select().where(Users.chat_id == chat_id)
    if not chat:
        Users.create(chat_id=chat_id, first_name=first_name,last_name=last_name)
    await state.finish()
    await message.answer(f'Привет, {first_name}, я бот который формирует отчёт по отгрузке '
                         f'щебня по производителям и потребителям за период', reply_markup=kb_start)

@dp.message_handler(state='*', text='заново')
async def on_start(message:types.Message, state: FSMContext):
    await remove_json("data")
    await state.finish()
    await message.answer(f'Привет, {message.from_user.first_name}, я бот который формирует отчёт по отгрузке '
                         f'щебня по производителям и потребителям за период', reply_markup=kb_start)
