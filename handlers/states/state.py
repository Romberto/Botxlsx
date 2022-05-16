from aiogram.dispatcher.filters.state import StatesGroup, State


class MainState(StatesGroup):
    article = State()  # запоминаем Производителя или Потребителя , а так же имя компании
    start_date_step = State()  # запоминаем интерисующий период начало
    end_date_step = State()  # запоминаем интерисующий период конец
    report_filter = State()  # выбор отчёт в xlsx или pdf


class LoadState(StatesGroup):
    step_load = State()
    step_update = State()


class LookState(StatesGroup):
    sp_command = State()
    sp_look = State()
