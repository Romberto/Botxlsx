import os
from data.config import  FILE_PATH_XLSX, DATABASE
from aiogram import types
from aiogram.dispatcher import FSMContext
from manager.make_database import get_data, update_data
from handlers.callback_data.callback import callback_file_answer
from handlers.keyboard.keyboard import kb_start
from handlers.states.state import LoadState
from loader import dp


@dp.callback_query_handler(callback_file_answer.filter(action=['yes', 'no']))
async def callback_new_file(call: types.CallbackQuery, callback_data: dict):
    action = callback_data['action']
    if action == 'yes':
        await LoadState.step_load.set()
        await call.message.answer('загрузите фалл в xls формате', reply_markup=kb_start)
    elif action == 'no':
        await call.message.answer('Отлично!!! \n'
                                  'Продолжаем с ранее загруженной таблицей', reply_markup=kb_start)


@dp.message_handler(content_types=types.ContentType.DOCUMENT, state=LoadState.step_load)
async def load_file(message:types.Message, state: FSMContext):
    if os.path.exists(FILE_PATH_XLSX):
        os.remove(FILE_PATH_XLSX)
    file_name = message.document.file_name.split('.')[-1]

    if file_name != 'xlsx':
        print('не тот формат')
        await message.answer('формат таблицы должен быть .xlsx\n'
                             'бот ждёт файл с таблицей')
        return

    else:
        file_id = message.document.file_id
        file_table = await message.bot.get_file(file_id)
        file_path = file_table.file_path
        # ПУТЬ К ГЛАВНОМУ ФАЙЛУ
        await message.bot.download_file(file_path, FILE_PATH_XLSX)

        await message.answer('Таблица загружена идёт преобразование таблицы в базу данных. \n Ждём 9 сек. ')
        photo = open("data/1uJP.gif", 'rb')
        await message.bot.send_animation(message.chat.id, photo)
        photo.close()
        await get_data(FILE_PATH_XLSX)

        await message.answer('Преобразование завершено, база готова!!!', reply_markup=kb_start)

        await state.finish()

@dp.message_handler(content_types=types.ContentType.DOCUMENT, state=LoadState.step_update)
async def load_update(message:types.Message, state=FSMContext):
    file_name = message.document.file_name.split('.')[-1]

    if file_name != 'xlsx':
        print('не тот формат')
        await message.answer('формат таблицы должен быть .xlsx\n'
                             'бот ждёт файл с таблицей')
        return

    else:
        file_id = message.document.file_id
        file_table = await message.bot.get_file(file_id)
        file_path = file_table.file_path
        # ПУТЬ К ГЛАВНОМУ ФАЙЛУ
        await message.bot.download_file(file_path, FILE_PATH_XLSX)

        await message.answer('Таблица загружена идёт преобразование таблицы в базу данных. \n Ждём 9 сек. ')
        photo = open("data/1uJP.gif", 'rb')
        await message.bot.send_animation(message.chat.id, photo)
        photo.close()
        print('dsds')
        await update_data(FILE_PATH_XLSX)

        await message.answer('Преобразование завершено, база готова!!!', reply_markup=kb_start)

        await state.finish()