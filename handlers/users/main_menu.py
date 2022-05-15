import os

from aiogram import types

from data.config import FILE_PATH_XLSX, DATABASE
from handlers.callback_data.callback import callback_file_answer
from handlers.keyboard.keyboard import kb_on_start, kb_start
from loader import dp
from handlers.states.state import LoadState, MainState
from aiogram.dispatcher import FSMContext


@dp.message_handler(content_types=types.ContentType.TEXT)
async def main_menu(message: types.Message, state: FSMContext):
    if message.text == 'Выбрать производителя':
        if os.path.exists(DATABASE):
            switch_keyboard = types.InlineKeyboardMarkup()
            switch_keyboard.add(types.InlineKeyboardButton(
                text="Выбрать производителя",
                switch_inline_query_current_chat="",
            ))
            await MainState.article.set()
            await state.update_data(article='Производитель')
            await message.answer(
                "Нажмите на кнопку 'Выбрать производителя', и начните вводить название компании",
                reply_markup=switch_keyboard)


        else:
            await message.answer("загрузите таблицу в формате xlsx с которой будем работать\n "
                                 "*** нажмите заново ***", reply_markup=kb_on_start)

    elif message.text == 'Выбрать потребителя':
        if os.path.exists(DATABASE):
            switch_keyboard = types.InlineKeyboardMarkup()
            switch_keyboard.add(types.InlineKeyboardButton(
                text="Выбрать потребителя",
                switch_inline_query_current_chat="",
            ))
            await MainState.article.set()
            await state.update_data(article='Потребитель')
            await message.answer(
                "Нажмите на кнопку 'Выбрать потребителя', и начните вводить название компании",
                reply_markup=switch_keyboard)
        else:
            await message.answer("загрузите таблицу в формате xlsx с которой будем работать\n "
                                 "*** нажмите заново ***", reply_markup=kb_on_start)

