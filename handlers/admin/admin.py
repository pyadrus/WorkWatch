# -*- coding: utf-8 -*-
from datetime import date, datetime
from io import BytesIO

from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import BufferedInputFile, CallbackQuery, Message
from loguru import logger
from openpyxl import Workbook

from database import AdminBot, RecordDataWorkingStart, RegisterUserBot, db
from dispatcher import bot, router
from keyboards.admin import admin_keyboard
from keyboards.keyboards import start_menu_keyboard
from states.states import AdminState


@router.callback_query(F.data == "grant_administrator_rights")
async def grant_administrator_rights(callback_query: CallbackQuery, state: FSMContext):
    """✅ Выдача администраторских прав"""
    await state.clear()
    message_text = "🔑 Выдача администраторских прав\n\nВведите id пользователя, которому хотите выдать права администратора:"
    await bot.send_message(
        chat_id=callback_query.from_user.id,
        text=message_text,
    )
    await state.set_state(AdminState.admin_id)


@router.message(AdminState.admin_id)
async def handle_admin_id(message: Message, state: FSMContext):
    """✅ Обработка id администратора"""
    admin_id = message.text.strip()

    db.create_tables([AdminBot])
    # Проверяем, что это число
    if not admin_id.isdigit():
        await bot.send_message(
            chat_id=message.from_user.id,
            text="⚠️ ID должен быть числом. Попробуйте ещё раз.",
        )
        return

    admin_id = int(admin_id)

    # Сохраняем в базу данных
    try:
        AdminBot.create(id_admin=admin_id)
        await bot.send_message(
            chat_id=message.from_user.id,
            text=f"✅ Пользователю с ID {admin_id} успешно выданы администраторские права.",
            reply_markup=start_menu_keyboard(),
        )
    except Exception as e:
        logger.exception(e)
        await bot.send_message(
            chat_id=message.from_user.id,
            text="❌ Произошла ошибка при сохранении данных.",
            reply_markup=start_menu_keyboard(),
        )

    await state.clear()


@router.callback_query(F.data == "get_register_users")
async def get_register_users(callback_query: CallbackQuery, state: FSMContext):
    """✅ Получение списка зарегистрированных пользователей"""
    await state.clear()
    # Получаем всех пользователей из базы данных
    users = list(RegisterUserBot.select().dicts())
    if not users:
        await callback_query.message.answer("⚠️ Нет зарегистрированных пользователей.")
        return
    # Создаём Excel-файл с помощью openpyxl
    wb = Workbook()
    ws = wb.active
    ws.title = "Пользователи"
    # Добавляем заголовки
    ws.append(
        [
            "ID пользователя",
            "Имя Telegram",
            "Фамилия Telegram",
            "Username",
            "Имя сотрудника",
            "Фамилия сотрудника",
            "Телефон",
            "Пол",
            "Дата регистрации",
        ]
    )
    # Добавляем данные
    for user in users:
        ws.append(
            [
                user["id_user"],
                user["name_telegram"],
                user["surname_telegram"],
                user["username"],
                user["name"],
                user["surname"],
                user["phone"],
                user["gender"],
                user["registration_date"],
            ]
        )
    # Сохраняем в буфер
    file_stream = BytesIO()
    wb.save(file_stream)
    file_stream.seek(0)
    filename = f"registered_users_{datetime.now().strftime("%Y-%m-%d")}.xlsx"
    # Создаем BufferedInputFile
    document = BufferedInputFile(file=file_stream.read(), filename=filename)
    # Отправляем как документ
    await bot.send_document(
        chat_id=callback_query.from_user.id,
        document=document,
        caption="📊 Список зарегистрированных пользователей",
        reply_markup=start_menu_keyboard(),
    )


@router.callback_query(F.data == "admin_panel")
async def admin_panel(callback_query: CallbackQuery, state: FSMContext):
    """✅ Панель администратора"""
    await state.clear()
    message_text = (
        "✅ Панель администратора\n\n"
        "📊 Список зарегистрированных пользователей\n"
        "🏠 Список сотрудников на работе"
    )
    await bot.send_message(
        chat_id=callback_query.from_user.id,
        text=message_text,
        reply_markup=admin_keyboard(),
    )


@router.callback_query(F.data == "who_at_work")
async def who_at_work(callback_query: CallbackQuery, state: FSMContext):
    """✅ Получение пользователей, которые на работе"""

    current_date = date.today()

    # Получаем все записи за текущий день
    start_of_day = datetime.combine(
        current_date, datetime.min.time()
    )  # Начало дня: 00:00
    # Конец дня: 23:59:59.999999
    end_of_day = datetime.combine(current_date, datetime.max.time())
    all_records = (
        RecordDataWorkingStart.select()
        .where(
            (RecordDataWorkingStart.time_start >= start_of_day)
            & (RecordDataWorkingStart.time_start <= end_of_day)
        )
        .order_by(RecordDataWorkingStart.time_start.asc())
    )

    # Если записей нет, отправляем сообщение
    if not all_records.exists():
        message_text = "📭 На данный момент никто не на работе."
        logger.info(message_text)
        await bot.send_message(
            chat_id=callback_query.from_user.id,
            text=message_text,
            reply_markup=start_menu_keyboard(),
        )
        return

    # Группируем записи по id_user, чтобы найти последнюю запись для каждого сотрудника
    latest_records = {}
    for record in all_records:
        # Последняя запись перезапишет предыдущие
        latest_records[record.id_user] = record

    # Фильтруем сотрудников, которые "на работе"
    users_at_work = [
        record for record in latest_records.values() if record.event_user == "на работе"
    ]

    # Формируем текст сообщения
    if users_at_work:
        user_list = "\n".join(
            [
                f"👤 {user.name} {user.surname} - {user.store_address} (время: {user.time_start.strftime('%H:%M')})"
                for user in users_at_work
            ]
        )
        message_text = f"📋 Список сотрудников на работе:\n{user_list}"
    else:
        message_text = "📭 На данный момент никто не на работе."

    logger.info(message_text)

    await bot.send_message(
        chat_id=callback_query.from_user.id,
        text=message_text,
        reply_markup=start_menu_keyboard(),
    )


def register_handler_who_at_work():
    """Регистрация хендлера, кто на работе"""
    router.callback_query.register(who_at_work, F.data == "who_at_work")
    router.callback_query.register(admin_panel, F.data == "admin_panel")
    router.callback_query.register(get_register_users, F.data == "get_register_users")
    router.callback_query.register(
        grant_administrator_rights, F.data == "grant_administrator_rights"
    )
