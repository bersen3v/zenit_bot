from aiogram import types
from aiogram.types import FSInputFile
from core.constants import adress
from keyboards.menu import menu


async def adresses(message: types.Message):
    menu.back_to_menu()
    photo_03 = FSInputFile("static/adress_menu.png")

    await message.answer_photo(photo_03, adress,
                                        parse_mode='Markdown',
                                        reply_markup=menu.builder.as_markup(resize_keyboard=True))
