# -*- coding: utf-8 -*-
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def start_keyboard():
    """Клавиатура главного меню бота"""
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Справка', callback_data='reference'),],])
