# -*- coding: utf-8 -*-
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def admin_keyboard():
    """Клавиатура администратора"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="👥 Кто на работе", callback_data="who_at_work"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Получить зарегистрированных пользователей",
                    callback_data="get_register_users",
                )
            ],
            [
                InlineKeyboardButton(
                    text="Заблокировать пользователя",
                    callback_data="block",
                )
            ],
            [
                InlineKeyboardButton(
                    text="Разблокировать пользователя",
                    callback_data="unblock",
                )
            ],
            [
                InlineKeyboardButton(
                    text="Дать права администратора",
                    callback_data="grant_administrator_rights",
                )
            ],
            [InlineKeyboardButton(text="⬅ Назад", callback_data="back")],
        ]
    )


def register_admin_keyboard():
    """Клавиатура администратора, приветствие"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="👥 Кто на работе", callback_data="who_at_work"
                )
            ],
            [InlineKeyboardButton(text="Справка", callback_data="reference")],
            [
                InlineKeyboardButton(
                    text="Перерегистрация", callback_data="registration"
                ),
            ],
            [
                InlineKeyboardButton(text="✅ На работе", callback_data="at_work"),
                InlineKeyboardButton(text="🏠 Ушёл", callback_data="left"),
            ],
            [
                InlineKeyboardButton(
                    text="Панель администратора", callback_data="admin_panel"
                )
            ],
        ]
    )
