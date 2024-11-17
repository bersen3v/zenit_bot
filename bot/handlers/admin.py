import io
from aiogram import types, Router, F, Bot
from aiogram.fsm.context import FSMContext

from core.config import TOKEN
from fsm.states import Admin
from database.clients_database import clients
from keyboards.admin import admin
from database.admins_database import admins

router = Router()
bot = Bot(token=TOKEN)


@router.message(F.text == '{ АДМИНКА }')
async def admin_menu(message: types.Message) -> None:
    admin.build_admin()
    await message.answer(
        "Админка",
        reply_markup=admin.builder.as_markup(resize_keyboard=True)
    )

@router.callback_query(F.data == 'admin')
async def admin_menu(callback: types.CallbackQuery) -> None:
    admin.build_admin()
    await callback.message.answer(
        "Админка",
        reply_markup=admin.builder.as_markup(resize_keyboard=True)
    )

@router.callback_query(F.data == "database_update")
async def update_database(callback: types.CallbackQuery, state: FSMContext) -> None:
    admin.cancel()
    await callback.message.answer(
        "Чтобы обновить базу, скинь файл в формате .csv",
        reply_markup=admin.builder.as_markup(resize_keyboard=True)
    )
    await state.set_state(Admin.updating_database)


@router.message(Admin.updating_database)
async def load_database(message: types.Message, state: FSMContext) -> None:
    if message.document and message.document.mime_type == 'text/csv':

        try:
            file = await bot.get_file(message.document.file_id)
            file_bytes = await bot.download_file(file.file_path)
            csvfile = io.BytesIO(file_bytes.getvalue())
            await clients.update_table(csvfile)
            await state.set_state(Admin.successful_update)
            await finish_updating(message, state)

        except Exception:
            admin.back_to_menu()
            await message.answer(
                "Возникла ошибка при обработке файла",
                reply_markup=admin.builder.as_markup(resize_keyboard=True)
            )
            await state.set_state(Admin.updating_database)

    else:
        admin.back_to_menu()
        await message.answer(
            "Неверный формат файла.\nПопробуй ещё раз",
            reply_markup=admin.builder.as_markup(resize_keyboard=True)
        )
        await state.set_state(Admin.updating_database)


@router.message(Admin.successful_update)
async def finish_updating(message: types.Message, state: FSMContext) -> None:
    admin.back_to_menu()
    await state.clear()
    await message.answer(
        "База обновлена",
        reply_markup=admin.builder.as_markup(resize_keyboard=True)
    )


@router.callback_query(F.data == "add_new_admin")
async def update_database(callback: types.CallbackQuery, state: FSMContext) -> None:
    admin.cancel()
    await callback.message.answer(
        "Чтобы добавить нового администратора, отправь его Telegram id",
        reply_markup=admin.builder.as_markup(resize_keyboard=True)
    )
    await state.set_state(Admin.adding_administrator)


@router.message(Admin.adding_administrator)
async def registrate_account(message: types.Message, state: FSMContext) -> None:
    id_administrator = message.text

    if not id_administrator.isdigit():
        admin.cancel()
        await message.answer(
            "Вы ввели не Telegram id",
            reply_markup=admin.builder.as_markup(resize_keyboard=True)
        )
        await state.set_state(Admin.adding_administrator)

    elif await admins.check_admin_exist(int(id_administrator)):
        await state.clear()
        admin.back_to_menu()
        await message.answer(
            "Этот Telegram id уже указан как администратор",
            reply_markup=admin.builder.as_markup(resize_keyboard=True)
        )

    else:
        await state.clear()
        await admins.add_new_admin(int(id_administrator))
        admin.back_to_menu()
        await message.answer(
            "Новый администратор успешно добавлен",
            reply_markup=admin.builder.as_markup(resize_keyboard=True)
        )
