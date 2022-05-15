"""ПРИНИМАЕМ НАЧАЛО ПЕРИОДА ГОД """
from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers.callback_data.callback import callback_years, callback_month
from handlers.keyboard.keyboard import buttons_month, buttons_year, kb_start, kb_on_start, kb_reports
from handlers.states.state import MainState
from loader import dp


@dp.callback_query_handler(callback_years.filter(year=['2019', '2020', '2021', '2022', 'month']),
                           state=MainState.start_date_step)
async def end_date(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    year = callback_data['year']
    if year == 'month':
        data = await state.get_data()
        year = str(datetime.today().year)
        month = str(datetime.today().month)
        if len(month) != 2:
            month = "0" + month
        await call.message.answer('фильтрую базу...\n'
                                  'за текущий месяц'
                                  f'{data["article"]} {data["chosen_name_company"]}\n'
                                  )
        await state.update_data(start_year=year, end_year=year, start_month=month, end_month=month)

        await call.message.answer('отчёт готов ...', reply_markup=kb_reports)
        await MainState.report_filter.set()



    else:
        kb_mounth = types.InlineKeyboardMarkup(row_width=4)
        kb_mounth.add(*buttons_month)

        await state.update_data(start_year=year)
        await call.message.answer('НАЧАЛО периода\n'
                                  'выберите месяц', reply_markup=kb_mounth)


@dp.callback_query_handler(
    callback_month.filter(month=['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']),
    state=MainState.start_date_step)
async def get_mouth(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    date_mounth = callback_data['month']

    await state.update_data(start_month=date_mounth)
    data_step = await state.get_data()
    kb_years = types.InlineKeyboardMarkup(row_width=2)

    kb_years.add(*buttons_year)
    await call.message.answer(f'начало периода {data_step["start_year"]}_{data_step["start_month"]}\n'
                              f'теперь КОНЕЦ периода\n'
                              f'выберите год',
                              reply_markup=kb_years
                              )
    await MainState.next()


@dp.callback_query_handler(callback_years.filter(year=['2019', '2020', '2021', '2022']),
                           state=MainState.end_date_step)
async def end_year_callback(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    data = await state.get_data()
    year = callback_data['year']
    if int(year) < int(data['start_year']):
        kb_years = types.InlineKeyboardMarkup(row_width=2)
        kb_years.add(*buttons_year)
        await call.message.answer(f"конец периода должен быть в будущем,"
                                  f"выбраная дата НАЧАЛО: {data['start_year']}_{data['start_month']}"
                                  f"выберите КОНЕЦ периода 'год' после НАЧАЛО",
                                  reply_markup=kb_years)
        return
    kb_mounth = types.InlineKeyboardMarkup(row_width=4)
    kb_mounth.add(*buttons_month)
    await state.update_data(end_year=year)
    await call.message.answer('теперь выберем интересующий интервал\n'
                              'КОНЕЦ периода\n'
                              'выберите месяц', reply_markup=kb_mounth)


@dp.callback_query_handler(
    callback_month.filter(month=['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']),
    state=MainState.end_date_step)
async def get_mouth(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    data = await state.get_data()
    date_mounth = callback_data['month']

    if int(f"{data['start_year']}{data['start_month']}") > int(f"{data['end_year']}{date_mounth}"):
        kb_mounth = types.InlineKeyboardMarkup(row_width=4)
        kb_mounth.add(*buttons_month)
        await call.message.answer(f"конец периода должен быть в будущем,"
                                  f"выбраная дата НАЧАЛО: {data['start_year']}_{data['start_month']}"
                                  f"выберите КОНЕЦ периода {data['end_year']} 'месяц' после НАЧАЛО",
                                  reply_markup=kb_mounth)
        return
    await state.update_data(end_month=date_mounth)
    await call.message.answer('фильтрую базу...\n'
                              f'{data["article"]} {data["chosen_name_company"]}\n'
                              f'период с {data["start_year"]}_{data["start_month"]} по'
                              f' {data["end_year"]}_{date_mounth}\n\n'

                              )

    await MainState.report_filter.set()
    await call.message.answer('отчёт готов ...', reply_markup=kb_reports)
