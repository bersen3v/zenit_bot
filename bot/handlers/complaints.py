from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile
from aiogram import types, Router, F, Bot

from core.constants import complaints
from keyboards.menu import menu
from fsm.states import Complaint_menu
from core import config
from database.admins_database import admins

TOKEN = config.TOKEN
bot = Bot(token=TOKEN)

router = Router()


@router.message(F.text == "✉️ Жалобы")
async def complaint_menu_1(message: types.Message):
    menu.complaint_1()
    # Отправим меню menu.complaine_1()
    photo_08 = FSInputFile("static/complaint_menu.png")
    await message.answer_photo(photo_08, complaints[0],
                                        parse_mode='Markdown',
                                        reply_markup=menu.builder.as_markup(resize_keyboard=True))


@router.callback_query(F.data == "complaint_2")
async def complaint_menu_2(callback: types.CallbackQuery, state=FSMContext):
    menu.complaint_2()
    photo_08 = FSInputFile("static/complaint_menu.png")
    await callback.message.answer_photo(photo_08, complaints[1],
                                        parse_mode='Markdown',
                                        reply_markup=menu.builder.as_markup(resize_keyboard=True))
    await state.set_state(Complaint_menu.complaint)


@router.message(Complaint_menu.complaint)
async def send_complaint_to_admin(message: types.Message, state=FSMContext):
    try:
        photo_08 = FSInputFile("static/complaint_menu.png")
        mes = "Жалоба: " + message.text
        for admin_id in await admins.get_all_admins_id():
            await bot.send_message(admin_id, mes)
        await state.clear()
        menu.back_to_menu()
        await message.answer_photo(
            photo=photo_08,
            caption="Жалоба была отправлена!",
            reply_markup=menu.builder.as_markup(resize_keyboard=True))

    except Exception:
        menu.back_to_menu()
        await message.answer(
            "Произошла ошибка (скорее всего id одного из админов недействителен)",
            reply_markup=menu.builder.as_markup(resize_keyboard=True)
        )
