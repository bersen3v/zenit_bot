from aiogram import types
from aiogram.types import FSInputFile

from keyboards.menu import menu
from core.constants import question, questions

photo_05 = FSInputFile("static/questions_menu.png")


def add_button(text):
    button_number = len(menu.question_buttons) - 1
    button_callback = "new_button" + str(button_number)
    menu.new_button(text, button_callback)


async def ask_question(message: types.Message):
    menu.question()
    await message.answer_photo(photo_05, question,
                                        parse_mode='Markdown',
                                        reply_markup=menu.builder.as_markup(resize_keyboard=True))


async def ask_question_1(callback: types.CallbackQuery):
    menu.back_to_menu_1()
    await callback.message.answer_photo(photo_05, questions[list(questions)[0]],
                                        parse_mode='Markdown',
                                        reply_markup=menu.builder.as_markup(resize_keyboard=True))


async def ask_question_2(callback: types.CallbackQuery):
    menu.back_to_menu_1()
    await callback.message.answer_photo(photo_05, questions[list(questions)[1]],
                                        parse_mode='Markdown',
                                        reply_markup=menu.builder.as_markup(resize_keyboard=True))


async def ask_question_3(callback: types.CallbackQuery):
    menu.back_to_menu_1()
    await callback.message.answer_photo(photo_05, questions[list(questions)[2]],
                                        parse_mode='Markdown',
                                        reply_markup=menu.builder.as_markup(resize_keyboard=True))


async def ask_question_4(callback: types.CallbackQuery):
    menu.back_to_menu_1()
    await callback.message.answer_photo(photo_05, questions[list(questions)[3]],
                                        parse_mode='Markdown',
                                        reply_markup=menu.builder.as_markup(resize_keyboard=True))
