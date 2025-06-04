# -*- coding: utf-8 -*-
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from dispatcher import bot, router
from keyboards import start_menu_keyboard


@router.callback_query(F.data == "reference")
async def reference(callback_query: CallbackQuery, state: FSMContext):
    """✅ Справка"""
    text = (
        "👋 Добро пожаловать в бот для учета сотрудников на рабочем месте!\n\n"
        "Этот бот помогает фиксировать ваше присутствие на рабочем месте и уведомлять коллег.\n\n"
        "📌 Основные команды:\n"
        '✅ "На работе" — зарегистрировать приход. Укажите ваши ФИО и адрес магазина (из списка).\n'
        '🏠 "Ушёл" — зарегистрировать уход.\n'
        '📖 "Справка" — повторно показать это сообщение.\n'
        '"Перерегистрация" — В случае не верного ввода данных можно повторно зарегистрировать данные о себе.\n\n'
        "🔔 Уведомления: При отметке прихода или ухода бот автоматически сообщит об этом в общий чат сотрудников.\n"
        '👥 Для администраторов: Доступна кнопка "Кто на работе" для просмотра списка присутствующих. \n'
        "⚠️ Важно: Доступ к боту только для сотрудников компании.\n\n"
    )

    await bot.send_message(
        chat_id=callback_query.from_user.id,
        text=text,
        reply_markup=start_menu_keyboard(),
    )


def register_handler_reference():
    """Регистрация справки"""
    router.callback_query.register(reference, F.data == "reference")
