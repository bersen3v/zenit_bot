from aiogram import types, Router
from aiogram.filters import Command
from aiogram.types import FSInputFile
from aiogram import F
from aiogram.fsm.context import FSMContext

from keyboards.menu import menu
from database.admins_database import admins
from database.users_database import users

router = Router()
photo_01 = FSInputFile("static/main_menu.png")


@router.message(Command("start"))
async def cmd_start(message: types.Message, state=FSMContext) -> None:
    await state.clear()

    id = message.from_user.id
    if not await users.check_user_exist(id):
        await users.add_new_user(id)

    if await admins.check_admin_exist(id):
        menu.admin_menu()

    else:
        menu.main_menu()
    await message.answer_photo(photo_01, "Выберите опцию:",
                               reply_markup=menu.keyboard)


@router.callback_query(F.data == "menu")
async def return_main_menu(callback: types.CallbackQuery, state=FSMContext) -> None:
    await state.clear()

    if await admins.check_admin_exist(callback.from_user.id):
        menu.admin_menu()

    else:
        menu.main_menu()
    await callback.message.answer_photo(photo_01, "Выберите опцию:",
                                        reply_markup=menu.keyboard)
