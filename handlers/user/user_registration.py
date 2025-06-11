# -*- coding: utf-8 -*-
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from loguru import logger

from database import registration_user, AdminBlockUser
from dispatcher import bot, router
from keyboards.keyboards import gender_keyboard, start_keyboard
from messages.messages import messages_start
from states.states import RegisterState


@router.callback_query(F.data == "registration")
async def registration_user_handler(callback_query: CallbackQuery, state: FSMContext):
    """Начало регистрации — запрашиваем имя"""

    id_user = callback_query.from_user.id  # id пользователя
    # Проверяем, заблокирован ли пользователь
    block = AdminBlockUser.select().where(AdminBlockUser.block_id == id_user).first()
    if block:
        logger.warning(f"Заблокированный пользователь {id_user} попытался войти")
        await bot.send_message(
            chat_id=callback_query.from_user.id,
            text="❌ Вам запрещён доступ к этому боту.",
        )
        return  # Прерываем выполнение функции

    await bot.send_message(
        chat_id=callback_query.from_user.id, text="Для регистрации введите свое имя"
    )
    await state.set_state(RegisterState.name)


@router.message(RegisterState.name)
async def handle_registration_name(message: Message, state: FSMContext):
    """Получаем имя, запрашиваем фамилию"""
    user_name = message.text
    await state.update_data(user_name=user_name)
    await bot.send_message(chat_id=message.from_user.id, text="Введите свою фамилию")
    await state.set_state(RegisterState.surname)


@router.message(RegisterState.surname)
async def handle_registration_surname(message: Message, state: FSMContext):
    """Получаем фамилию, запрашиваем телефон"""
    user_surname = message.text
    await state.update_data(user_surname=user_surname)
    await bot.send_message(
        chat_id=message.from_user.id, text="Введите свой номер телефона"
    )
    await state.set_state(RegisterState.phone)


@router.message(RegisterState.phone)
async def handle_registration_phone(message: Message, state: FSMContext):
    """Получаем телефон, запрашиваем пол"""
    await state.update_data(user_phone=message.text)
    await bot.send_message(
        chat_id=message.from_user.id,
        text="Выберите свой пол:",
        reply_markup=gender_keyboard(),
    )
    await state.set_state(RegisterState.gender)


@router.callback_query(RegisterState.gender)
async def handle_registration_gender(callback: CallbackQuery, state: FSMContext):
    """Обрабатываем выбор пола"""
    try:
        gender = "мужской" if callback.data == "gender_male" else "женский"
        logger.info(f"Gender: {gender}")
        await state.update_data(user_gender=gender)

        data = await state.get_data()
        user_name = data.get("user_name")
        user_surname = data.get("user_surname")
        user_phone = data.get("user_phone")

        logger.info(f"User: {user_name}, {user_surname}, {user_phone}, {gender}")

        # Сохраняем пользователя в БД
        registration_user(
            callback=callback,
            name=user_name,
            surname=user_surname,
            phone=user_phone,
            gender=gender,
        )

        await state.clear()

        await bot.send_message(
            chat_id=callback.message.chat.id,
            text=messages_start,
            reply_markup=start_keyboard(),
        )
    except Exception as e:
        logger.exception(e)


def registration_handler_register_user():
    """Регистрация Handler"""
    router.callback_query.register(registration_user_handler)
    router.callback_query.register(handle_registration_name)
    router.callback_query.register(handle_registration_surname)
    router.callback_query.register(handle_registration_phone)
    router.callback_query.register(handle_registration_gender)
