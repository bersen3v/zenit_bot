from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder


class Admin:
    def __init__(self) -> None:
        self.builder = InlineKeyboardBuilder()

        self.button_1 = types.InlineKeyboardButton(
            text="Главное меню",
            callback_data="menu"
        )

        self.button_2 = types.InlineKeyboardButton(
            text="Обновить базу",
            callback_data="database_update"
        )

        self.button_3 = types.InlineKeyboardButton(
            text="Рассылки",
            callback_data="mailing"
        )

        self.button_4 = types.InlineKeyboardButton(
            text="Рассылка по именинникам",
            callback_data="send_birth_mailing"
        )

        self.button_5 = types.InlineKeyboardButton(
            text="Рассылка всем",
            callback_data="all_mailing"
        )

        self.button_6 = types.InlineKeyboardButton(
            text="Рассылка по номеру игрока",
            callback_data="number_mailing"
        )

        self.button_7 = types.InlineKeyboardButton(
            text="Отмена",
            callback_data="admin"
        )

        self.button_8 = types.InlineKeyboardButton(
            text="Без фото",
            callback_data="without_photo"
        )

        self.button_9 = types.InlineKeyboardButton(
            text="Разослать сообщение указанным пользователям",
            callback_data="send_post"
        )

        self.button_10 = types.InlineKeyboardButton(
            text="Добавить нового администратора",
            callback_data="add_new_admin"
        )

    def build_admin(self) -> None:
        self.builder = InlineKeyboardBuilder()
        self.builder.row(self.button_2)
        self.builder.row(self.button_3)
        self.builder.row(self.button_10)
        self.builder.row(self.button_1)

    def cancel(self) -> None:
        self.builder = InlineKeyboardBuilder()
        self.builder.row(self.button_7)

    def back_to_menu(self) -> None:
        self.builder = InlineKeyboardBuilder()
        self.builder.row(self.button_1)

    def mailing(self):
        self.builder = InlineKeyboardBuilder()
        self.builder.row(self.button_5)
        self.builder.row(self.button_4)
        self.builder.row(self.button_6)
        self.builder.row(self.button_7)

    def mailing_photo(self):
        self.builder = InlineKeyboardBuilder()
        self.builder.row(self.button_8)
        self.builder.row(self.button_7)

    def sending_mailing_menu(self):
        self.builder = InlineKeyboardBuilder()
        self.builder.row(self.button_9)
        self.builder.row(self.button_7)


admin = Admin()
