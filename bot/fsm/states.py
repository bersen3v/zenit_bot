from aiogram.fsm.state import State, StatesGroup


class Account(StatesGroup):
    registration = State()


class Admin(StatesGroup):
    updating_database = State()
    successful_update = State()
    mailing_text = State()
    mailing_photo = State()
    sending_mailing_with_photo = State()
    adding_administrator = State()
    mailing_file = State()


class Complaint_menu(StatesGroup):
    complaint = State()
