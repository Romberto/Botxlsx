from pprint import pprint

from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers.keyboard.keyboard import kb_reports
from handlers.states.state import MainState
from loader import dp

from manager.EXELEmaker import EXELEmaker
from manager.PDFmaker import PDFmaker


@dp.message_handler(state=MainState.report_filter, text='Отчёт в exele')
async def exele(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    data = await state.get_data()
    name_company = data['chosen_name_company'].replace(' ', "_")

    filter_dict = {
        'chosen_name_company': data["chosen_name_company"],
        'start_year': data["start_year"],
        'start_month': data["start_month"],
        'end_year': data['end_year'],
        'end_month': data['end_month'],
        'article': data['article']
    }

    pdf = PDFmaker(filter_dict, chat_id)
    datas = pdf.filter_database()
    await EXELEmaker(datas, f'data/file{message.chat.id}.xlsx', data["article"])
    doc = open(f'data/file{message.chat.id}.xlsx', 'rb')
    await message.answer_document(document=doc, reply_markup=kb_reports)
    doc.close()
    return


@dp.message_handler(state=MainState.report_filter, text='Отчёт в pdf')
async def pdf(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    data = await state.get_data()
    name_company = data['chosen_name_company'].replace(' ', "_")

    filter_dict = {
        'chosen_name_company': data["chosen_name_company"],
        'start_year': data["start_year"],
        'start_month': data["start_month"],
        'end_year': data['end_year'],
        'end_month': data['end_month'],
        'article': data['article']
    }

    pdf = PDFmaker(filter_dict, chat_id)
    if pdf.filter_database():
        pdf.pdf_maker(f'data/DATA_{chat_id}_name_company_{name_company}.pdf')

        doc = open(f'data/DATA_{chat_id}_name_company_{name_company}.pdf', mode='rb')
        await message.answer_document(doc, reply_markup=kb_reports)
        doc.close()
        return
    else:
        await message.answer(f'{data["article"]} в этом периоде не найден')
        return
