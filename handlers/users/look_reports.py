from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import admins_id
from handlers.keyboard.keyboard import kb_start
from handlers.states.state import LookState
from loader import dp



from manager.manager import remove_json, looking_report

#    просмотр кто и когда формировал отчеты

@dp.callback_query_handler(state=LookState.sp_look)
async def cb_look(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'r1':
        await looking_report(0)
        doc = open('data/report.pdf', mode='rb')
        await call.message.delete_reply_markup()
        await call.message.answer_document(document=doc, reply_markup=kb_start)
        await remove_json('data')
        await state.finish()
    elif call.data == 'r3':
        await looking_report(2)
        doc = open('data/report.pdf', mode='rb')
        await call.message.delete_reply_markup()
        await call.message.answer_document(document=doc, reply_markup=kb_start)
        await remove_json('data')
        await state.finish()
    elif call.data == 'r7':
        await looking_report(6)
        doc = open('data/report.pdf', mode='rb')
        await call.message.delete_reply_markup()
        await call.message.answer_document(document=doc, reply_markup=kb_start)
        await remove_json('data')
        await state.finish()
    elif call.data == 'end':
        await remove_json("data")
        await state.finish()
        await call.message.answer(f'Привет, я бот который формирует отчёт по отгрузке '
                             f'щебня по производителям и потребителям за период', reply_markup=kb_start)

