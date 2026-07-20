from aiogram.fsm.state import State, StatesGroup


class DepositState(StatesGroup):
    amount = State()
    pending = State()
    confirming = State()


class InvoiceState(StatesGroup):
    search = State()