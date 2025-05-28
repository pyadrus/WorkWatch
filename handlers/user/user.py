# -*- coding: utf-8 -*-
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from dispatcher import router, bot
from keyboards import shops_keyboard


@router.callback_query(F.data == "at_work")
async def at_work(callback_query: CallbackQuery, state: FSMContext):
    """Регистрация пользователей и запись данных в базу данных"""
    await bot.send_message(
        chat_id=callback_query.from_user.id,
        text='Выберите из списка адрес магазина',
        reply_markup=shops_keyboard()
    )


def register_handlers_at_work():
    """Регистрация хэндлеров"""
    router.callback_query.register(at_work, text="at_work")
