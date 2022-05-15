from aiogram.dispatcher import FSMContext

from handlers.keyboard.keyboard import *
from handlers.states.state import MainState
from loader import dp
from aiogram import types
from manager.seatcher import Searcher


@dp.inline_handler(state=MainState.article)
async def inline_handler_manufacturer(query: types.InlineQuery, state : FSMContext):
    state_data = await state.get_data()
    article = state_data["article"]
    search = Searcher(article)
    text = query.query or 'echo'
    result = []
    names = search.pars_query(text)
    if names:
        for i, name in enumerate(names):
            if len(result) < 10:
                result.append(
                    types.InlineQueryResultArticle(
                        id=str(i + 1),
                        title=name,
                        input_message_content=types.InputTextMessageContent(
                            message_text=name
                        )
                    )
                )
            else:
                break
        await query.answer(result, cache_time=10 )

    else:
        result.append(
            types.InlineQueryResultArticle(
                id='90000',
                title="ни чего не нашлось, отмена",
                input_message_content=types.InputTextMessageContent(message_text='отмена')
            )
        )
        await query.answer(result, cache_time=10)





@dp.message_handler(content_types=types.ContentType.TEXT, state=MainState.article)
async def gfgt(message: types.Message, state : FSMContext):
    if message.text == 'заново' or message.text == 'отмена':
        await state.finish()
        await message.answer(f'Привет, имя, я бот который формирует отчёт по отгрузке '
                             f'щебня по производителям и потребителям за период', reply_markup=kb_start)
    else:
        await state.update_data(chosen_name_company=message.text.strip())
        await MainState.start_date_step.set()
        kb_years = types.InlineKeyboardMarkup(row_width=2)

        kb_years.add(*buttons_year)
        kb_years.add(types.InlineKeyboardButton(text='текущий месяц', callback_data=callback_years.new(year='month')))

        await message.answer('теперь выберем интересующий интервал\n'
                             'НАЧАЛО периода\n'
                             'выберите год', reply_markup=kb_years)
