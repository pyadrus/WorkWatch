# -*- coding: utf-8 -*-
from datetime import date, datetime

from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from loguru import logger

from database import (RecordDataWorkingStart)
from dispatcher import bot, router
from keyboards import start_menu_keyboard


@router.callback_query(F.data == "who_at_work")
async def who_at_work(callback_query: CallbackQuery, state: FSMContext):
    """✅ Получение пользователей, которые на работе"""

    current_date = date.today()

    # Получаем все записи за текущий день
    start_of_day = datetime.combine(
        current_date, datetime.min.time())  # Начало дня: 00:00
    # Конец дня: 23:59:59.999999
    end_of_day = datetime.combine(current_date, datetime.max.time())
    all_records = RecordDataWorkingStart.select().where(
        (RecordDataWorkingStart.time_start >= start_of_day) &
        (RecordDataWorkingStart.time_start <= end_of_day)
    ).order_by(RecordDataWorkingStart.time_start.asc())

    # Если записей нет, отправляем сообщение
    if not all_records.exists():
        message_text = "📭 На данный момент никто не на работе."
        logger.info(message_text)
        await bot.send_message(
            chat_id=callback_query.from_user.id,
            text=message_text,
            reply_markup=start_menu_keyboard()
        )
        return

    # Группируем записи по id_user, чтобы найти последнюю запись для каждого сотрудника
    latest_records = {}
    for record in all_records:
        # Последняя запись перезапишет предыдущие
        latest_records[record.id_user] = record

    # Фильтруем сотрудников, которые "на работе"
    users_at_work = [
        record for record in latest_records.values()
        if record.event_user == "на работе"
    ]

    # Формируем текст сообщения
    if users_at_work:
        user_list = "\n".join(
            [f"👤 {user.name} {user.surname} - {user.store_address} (время: {user.time_start.strftime('%H:%M')})"
                for user in users_at_work]
        )
        message_text = f"📋 Список сотрудников на работе:\n{user_list}"
    else:
        message_text = "📭 На данный момент никто не на работе."

    logger.info(message_text)

    await bot.send_message(
        chat_id=callback_query.from_user.id,
        text=message_text,
        reply_markup=start_menu_keyboard()
    )


def register_handler_who_at_work():
    """Регистрация хендлера, кто на работе"""
    router.callback_query.register(who_at_work, F.data == "who_at_work")
