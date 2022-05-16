import os
import types

from data.config import FILE_PATH_XLSX, admins_id
from handlers.keyboard.keyboard import *
from handlers.states.state import LoadState, LookState
from loader import dp



@dp.message_handler(text="/look")
async def look(message: types.Message):
    if message.chat.id in admins_id:
        kb_look_menu = types.InlineKeyboardMarkup(row_width=1)
        buttons = [
            types.InlineKeyboardButton(text="Отчёты за сегодня", callback_data="r1"),
            types.InlineKeyboardButton(text="Отчёты за последние 3 дня", callback_data="r3"),
            types.InlineKeyboardButton(text="Отчёты за последние 7 дней", callback_data="r7"),
            types.InlineKeyboardButton(text="выйти", callback_data="end")
        ]
        kb_look_menu.add(*buttons)
        await LookState.sp_look.set()
        await message.answer("Укажите за какой период, просмотреть информацию о отчётах", reply_markup=kb_look_menu)
    else:
        try:
            await message.answer(
                f'извените {message.from_user.first_name} у вас нет прав для этой команды, обратитесь к администратору',
                reply_markup=kb_start)
        except Exception as er:

            await message.answer(
                'извените у вас нет прав для этой команды, обратитесь к администратору',
                reply_markup=kb_start)

@dp.message_handler(commands="load")
async def load_xlsx(message: types.Message):

    if message.chat.id in admins_id:
        kb_load = types.ReplyKeyboardMarkup([
            [types.KeyboardButton('загрузить'), types.KeyboardButton('обновить')]
        ],resize_keyboard=True)
        await message.answer('вы можете загрузить абсолютно новую таблицу или обновить(добавить данные) к имеющейся', reply_markup=kb_load)
    else:
        await message.answer(
            f'{message.from_user.first_name} у вас нет прав для загрузки файлов, свяжитесь с администратором', reply_markup=kb_on_start)

@dp.message_handler(content_types=types.ContentType.TEXT, text='загрузить')
async def load_table(message:types.Message):
    file_path = FILE_PATH_XLSX
    if not os.path.exists(file_path):
        await LoadState.step_load.set()
        await message.answer("отправьте мне файл в формате xlsx \n или нажмите назад", reply_markup=kb_on_start)
    else:
        kb_new_file = types.InlineKeyboardMarkup()
        button1 = [types.InlineKeyboardButton(text="да загрузить новую таблицу",
                                              callback_data=callback_file_answer.new(action='yes')),
                   types.InlineKeyboardButton(text='нет, продолжить с имеющейся',
                                              callback_data=callback_file_answer.new(action='no'))]
        kb_new_file.add(*button1)

        await message.answer('я обнаружил ранее загруженную таблицу\n'
                             'Хотите загрузить новую ?', reply_markup=kb_new_file)
@dp.message_handler(content_types=types.ContentType.TEXT, text="обновить")
async def update_table(message: types.Message):
    await LoadState.step_update.set()
    await message.answer("отправьте мне файл в формате xlsx \n или нажмите назад", reply_markup=kb_on_start)