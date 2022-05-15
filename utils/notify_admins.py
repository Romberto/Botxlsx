import logging
from aiogram import Dispatcher

from data.config import admins_id


async def on_startup_notyfy(dp: Dispatcher):
    for admin in admins_id:
        try:
            await dp.bot.send_message(chat_id=admin, text="Бот запущен")
        except Exception as err:
            logging.exception(err)
