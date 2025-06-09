# -*- coding: utf-8 -*-
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database import AdminBlockUser
from dispatcher import bot, router
from keyboards.keyboards import start_menu_keyboard
from loguru import logger

from messages.messages import messages_start


@router.callback_query(F.data == "reference")
async def reference(callback_query: CallbackQuery, state: FSMContext):
    """✅ Справка"""
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
        chat_id=callback_query.from_user.id,
        text=messages_start,
        reply_markup=start_menu_keyboard(),
    )


def register_handler_reference():
    """Регистрация справки"""
    router.callback_query.register(reference, F.data == "reference")
