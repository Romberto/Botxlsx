from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import admins_id
from handlers.keyboard.keyboard import kb_start
from handlers.states.state import LookState
from loader import dp


#    просмотр кто и когда формировал отчеты
from manager.manager import remove_json, looking_report



@dp.callback_query_handler(state=LookState.sp_look)
async def cb_look(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'r1':
        await looking_report(1)
        doc = open('data/report.pdf', mode='rb')
        await state.finish()
        await call.message.answer_document(document=doc, reply_markup=kb_start)
        await remove_json('data')
    elif call.data == 'r3':
        await looking_report(3)
        doc = open('data/report.pdf', mode='rb')
        await state.finish()
        await call.message.answer_document(document=doc, reply_markup=kb_start)
        await remove_json('data')
    elif call.data == 'r7':
        await looking_report(7)
        doc = open('data/report.pdf', mode='rb')
        await state.finish()
        await call.message.answer_document(document=doc, reply_markup=kb_start)
        await remove_json('data')
    elif call.data == 'end':
        await remove_json("data")
        await state.finish()
        await call.message.answer(f'Привет, я бот который формирует отчёт по отгрузке '
                             f'щебня по производителям и потребителям за период', reply_markup=kb_start)

