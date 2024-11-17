import io

from aiogram.fsm.context import FSMContext
from aiogram import types, Router, F, Bot

from core.config import TOKEN
from keyboards.admin import admin
from fsm.states import Admin
from database.clients_database import clients
from database.clients_telegram_database import clients_telegram
from database.users_database import users

router = Router()
bot = Bot(token=TOKEN)


@router.callback_query(F.data == "mailing")
async def mailing_menu(callback: types.CallbackQuery) -> None:
    admin.mailing()
    await callback.message.answer(
        text="виды рассылок",
        reply_markup=admin.builder.as_markup(resize_keyboard=True)
    )


@router.callback_query(F.data == "send_birth_mailing")
async def send_birth_mailing_text(callback: types.CallbackQuery, state: FSMContext):
    admin.back_to_menu()
    id_list = await clients.get_clients_number_with_birthday()
    await state.update_data(id_list=id_list)
    await callback.message.answer(
        text="Введи сообщение, которое хочешь отправить всем именинникам",
        reply_markup=admin.builder.as_markup(resize_keyboard=True)
    )
    await state.set_state(Admin.mailing_text)


@router.callback_query(F.data == "all_mailing")
async def send_birth_mailing_text(callback: types.CallbackQuery, state: FSMContext):
    if await users.get_all_users_id() is None:
        admin.back_to_menu()
        await state.clear()
        await callback.message.answer(
            text=f"На данный момент нет авторизованных пользователей",
            reply_markup=admin.builder.as_markup(resize_keyboard=True)
        )
    else:
        admin.back_to_menu()
        id_list = await users.get_all_users_id()
        await state.update_data(id_list=id_list)
        await callback.message.answer(
            text=f"Всего авторизованных пользователей: {len(id_list)}\n"
                 f"\nВведи сообщение, которое будет отправлено всем пользователям",
            reply_markup=admin.builder.as_markup(resize_keyboard=True)
        )
        await state.set_state(Admin.mailing_text)


@router.callback_query(F.data == "number_mailing")
async def send_birth_mailing_text(callback: types.CallbackQuery, state: FSMContext):
    admin.cancel()
    await callback.message.answer(
        text=f"Отправь txt файл со всеми номерами игроков, которым нужно отправить сообщение",
        reply_markup=admin.builder.as_markup(resize_keyboard=True)
    )
    await state.set_state(Admin.mailing_file)


@router.message(Admin.mailing_file)
async def get_mailing_file(message: types.Message, state: FSMContext):
    if message.document and message.document.mime_type == 'text/plain':
        try:
            file = await bot.get_file(message.document.file_id)
            file_bytes = await bot.download_file(file.file_path)
            txt_file = io.BytesIO(file_bytes.getvalue())
            content = txt_file.getvalue().decode('utf-8')
            number_list = list(map(int, content.split()))
            id_list = [
                await clients_telegram.get_id_by_number(number)
                for number in number_list
                if await clients_telegram.check_client_exist_by_number(number)
            ]
            if not len(id_list) == 0:
                await state.update_data(id_list=id_list)
                admin.back_to_menu()
                await message.answer(
                    text="Файл принят"
                         f"\n {len(id_list)} из {len(number_list)} номеров авторизованы в боте\n"
                         f"\n Теперь введи сообщение",
                    reply_markup=admin.builder.as_markup(resize_keyboard=True)
                )
                await state.set_state(Admin.mailing_text)

            else:
                admin.cancel()
                await message.answer(
                    text="В данном файле нет ни одного авторизованного пользователя"
                         "\n Попробуй ещё раз",
                    reply_markup=admin.builder.as_markup(resize_keyboard=True)
                )
                await state.set_state(Admin.mailing_file)

        except Exception:
            admin.back_to_menu()
            await state.clear()
            await message.answer(
                text="Произошла ошибка при обработке текстового файла",
                reply_markup=admin.builder.as_markup(resize_keyboard=True)
            )
    else:
        admin.cancel()
        await message.answer(
            text="Неверный формат файла"
                 "\nПопробуй ещё раз",
            reply_markup=admin.builder.as_markup(resize_keyboard=True)
        )
        await state.set_state(Admin.mailing_file)


@router.message(Admin.mailing_text)
async def get_mailing_text(message: types.Message, state: FSMContext):
    text = message.text
    admin.mailing_photo()
    await message.answer(
        text="Отправь фото, которое прикрепишь к посту",
        reply_markup=admin.builder.as_markup(resize_keyboard=True)
    )
    await state.set_state(Admin.mailing_photo)
    await state.update_data(text=text)


@router.message(Admin.mailing_photo)
async def get_birth_mailing_photo(message: types.Message, state: FSMContext):
    # Получаем последнее фото из сообщения
    photo = message.photo[-1]  # Берем самое высокое разрешение # Загружаем фото
    await state.update_data(photo=photo.file_id)
    # Извлекаем текст из состояния
    data = await state.get_data()
    text = data.get("text", "")  # Получаем текст, если он есть

    admin.sending_mailing_menu()
    await message.answer_photo(
        photo=photo.file_id,
        caption=text,
        reply_markup=admin.builder.as_markup(resize_keyboard=True)
    )


@router.callback_query(F.data == "without_photo")
async def mailing_without_photo(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    t = data.get("text", "")  # Получаем текст, если он есть

    admin.sending_mailing_menu()
    await callback.message.answer(
        text=t,
        reply_markup=admin.builder.as_markup(resize_keyboard=True)
    )


@router.callback_query(F.data == "send_post")
async def mailing_message(callback: types.CallbackQuery, state: FSMContext):
    try:
        data = await state.get_data()
        photo = data.get("photo", "")
        t = data.get("text", "")  # Получаем текст, если он есть
        id_list = data.get("id_list")
        if photo:
            for id in id_list:
                await bot.send_photo(photo=photo, chat_id=id, caption=t)
        else:
            for id in id_list:
                await bot.send_message(chat_id=id, text=t)
        admin.back_to_menu()
        await state.clear()
        await callback.message.answer(
            text=f"Рассылка произведена для {len(id_list)} пользователей",
            reply_markup=admin.builder.as_markup(resize_keyboard=True)
        )
    except Exception:
        admin.back_to_menu()
        await state.clear()
        await callback.message.answer(
            text="Произошла ошибка при рассылке (скорее всего некорректный ввод"
                 "отправляемого текста)",
            reply_markup=admin.builder.as_markup(resize_keyboard=True)
        )
