from aiogram import types
from aiogram.types import FSInputFile

from core.constants import contact
from keyboards.menu import menu


async def contacts(message: types.Message):
    menu.back_to_menu()
    photo_07 = FSInputFile("static/contact_menu.png")
    await message.answer_photo(photo_07, contact,
                               parse_mode='Markdown', reply_markup=menu.builder.as_markup(resize_keyboard=True)
                               )
