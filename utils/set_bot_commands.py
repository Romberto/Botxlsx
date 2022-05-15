from aiogram import types, Dispatcher


async def set_default_commands(dp: Dispatcher):
    await dp.bot.set_my_commands([
        types.BotCommand('/start', 'Старт'),
        types.BotCommand('/help', 'Помощь'),
        types.BotCommand('/load', 'Загрузить таблицу')

    ])
