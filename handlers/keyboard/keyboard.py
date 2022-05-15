from aiogram import types

from handlers.callback_data.callback import callback_file_answer, callback_years, callback_month

kb_start = types.ReplyKeyboardMarkup([
    [
        types.KeyboardButton('Выбрать производителя'),
        types.KeyboardButton('Выбрать потребителя')
    ],
    [
        types.KeyboardButton('заново')
    ]

], resize_keyboard=True, one_time_keyboard=True)

kb_on_start = types.ReplyKeyboardMarkup([
    [types.KeyboardButton('заново')]
], resize_keyboard=True)

buttons_year = [

    types.InlineKeyboardButton(text='2020', callback_data=callback_years.new(year=2020)),
    types.InlineKeyboardButton(text='2021', callback_data=callback_years.new(year=2021)),
    types.InlineKeyboardButton(text='2022', callback_data=callback_years.new(year=2022)),
    types.InlineKeyboardButton(text='2023', callback_data=callback_years.new(year=2023)),

]

buttons_month = [
    types.InlineKeyboardButton(text="1", callback_data=callback_month.new(month='01')),
    types.InlineKeyboardButton(text="2", callback_data=callback_month.new(month='02')),
    types.InlineKeyboardButton(text="3", callback_data=callback_month.new(month='03')),
    types.InlineKeyboardButton(text="4", callback_data=callback_month.new(month='04')),
    types.InlineKeyboardButton(text="5", callback_data=callback_month.new(month='05')),
    types.InlineKeyboardButton(text="6", callback_data=callback_month.new(month='06')),
    types.InlineKeyboardButton(text="7", callback_data=callback_month.new(month='07')),
    types.InlineKeyboardButton(text="8", callback_data=callback_month.new(month='08')),
    types.InlineKeyboardButton(text="9", callback_data=callback_month.new(month='09')),
    types.InlineKeyboardButton(text="10", callback_data=callback_month.new(month='10')),
    types.InlineKeyboardButton(text="11", callback_data=callback_month.new(month='11')),
    types.InlineKeyboardButton(text="12", callback_data=callback_month.new(month='12')),
]

kb_reports = types.ReplyKeyboardMarkup([
    [
        types.KeyboardButton(text="Отчёт в exele"),
        types.KeyboardButton(text="Отчёт в pdf"),
    ],
    [
        'заново'
    ]
],resize_keyboard=True)

