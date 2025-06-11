# -*- coding: utf-8 -*-
import asyncio
import logging
import sys

from aiogram import F
from aiogram.enums import ChatMemberStatus
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, Message
from loguru import logger

from database import (
    AdminBot,
    RegisterUserBot,
    db,
    is_admin,
    recording_data_users_who_launched_bot,
    AdminBlockUser,
    Person,
    RecordDataWorkingStart,
    get_registered_user,
)
from dispatcher import bot, dp, router
from handlers.admin.admin import register_handler_who_at_work
from handlers.user.user_end import register_handlers_left
from handlers.user.user_reference import register_handler_reference
from handlers.user.user_registration import registration_handler_register_user
from handlers.user.user_start import register_handlers_at_work
from keyboards.admin import register_admin_keyboard
from keyboards.keyboards import register_user_keyboard, start_keyboard
from messages.messages import messages_start

GROUP_CHAT_ID = -1002678330553  # ID группы


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    Обрабатывает команду `/start`.

    :param message: Сообщение от пользователя.
    :return: None
    """
    logger.info(f"Пользователь {message.from_user.id} отправил команду /start")
    # Проверяем, подписан ли пользователь на группу
    chat_member = await bot.get_chat_member(
        chat_id=GROUP_CHAT_ID, user_id=message.from_user.id
    )
    if chat_member.status not in [
        ChatMemberStatus.MEMBER,
        ChatMemberStatus.ADMINISTRATOR,
        ChatMemberStatus.CREATOR,
    ]:
        logger.warning(f"Пользователь {message.from_user.id} не подписан на группу")
        await bot.send_message(
            chat_id=message.from_user.id,
            text="❌ Вы не являетесь сотрудником компании, поэтому не можете использовать бота.\n\n",
        )
        return
    # Записываем данные пользователя, который отправил команду /start
    recording_data_users_who_launched_bot(message)
    db.create_tables(
        [RegisterUserBot, AdminBot, AdminBlockUser, Person, RecordDataWorkingStart]
    )
    # Проверяем, заблокирован ли пользователь
    if (
        AdminBlockUser.select()
        .where(AdminBlockUser.block_id == message.from_user.id)
        .first()
    ):
        logger.warning(
            f"Заблокированный пользователь {message.from_user.id} попытался войти"
        )
        await bot.send_message(
            chat_id=message.chat.id,
            text="❌ Вам запрещён доступ к этому боту.",
        )
        return  # Прерываем выполнение функции
    user = await get_registered_user(update=message)
    # Проверяем, является ли пользователь администратором
    if user:
        if is_admin(message.from_user.id):
            await bot.send_message(
                chat_id=message.chat.id,
                text=messages_start,
                reply_markup=register_admin_keyboard(),
            )
        else:
            await bot.send_message(
                chat_id=message.chat.id,
                text=messages_start,
                reply_markup=start_keyboard(),
            )
    else:
        await bot.send_message(
            chat_id=message.chat.id,
            text="Для использования бота, пройдите регистрацию",
            reply_markup=register_user_keyboard(),
        )


@router.callback_query(F.data == "back")
async def back_start_handler(callback_query: CallbackQuery) -> None:
    """
    Обрабатывает команду `/start`.

    :param callback_query: Сообщение от пользователя.
    :return: None
    """

    # Проверяем, подписан ли пользователь на группу
    # try:
    chat_member = await bot.get_chat_member(
        chat_id=GROUP_CHAT_ID, user_id=callback_query.from_user.id
    )
    if chat_member.status not in [
        ChatMemberStatus.MEMBER,
        ChatMemberStatus.ADMINISTRATOR,
        ChatMemberStatus.CREATOR,
    ]:
        logger.warning(
            f"Пользователь {callback_query.from_user.id} не подписан на группу"
        )
        await bot.send_message(
            chat_id=callback_query.from_user.id,
            text="❌ Вы не являетесь сотрудником компании, поэтому не можете использовать бота.\n\n",
        )
        return
    db.create_tables(
        [RegisterUserBot, AdminBot, AdminBlockUser, Person, RecordDataWorkingStart]
    )
    # Проверяем, заблокирован ли пользователь
    if (
        AdminBlockUser.select()
        .where(AdminBlockUser.block_id == callback_query.from_user.id)
        .first()
    ):
        logger.warning(
            f"Заблокированный пользователь {callback_query.from_user.id} попытался войти"
        )
        await bot.send_message(
            chat_id=callback_query.from_user.id,
            text="❌ Вам запрещён доступ к этому боту.",
        )
        return  # Прерываем выполнение функции
    user = await get_registered_user(update=callback_query)
    # Проверяем, является ли пользователь администратором
    if user:
        if is_admin(callback_query.from_user.id):
            await bot.send_message(
                chat_id=callback_query.from_user.id,
                text=messages_start,
                reply_markup=register_admin_keyboard(),
            )
        else:
            print(user.name, user.surname)
            await bot.send_message(
                chat_id=callback_query.from_user.id,
                text=messages_start,
                reply_markup=start_keyboard(),
            )
    else:
        print("Пользователь не найден.")
        await bot.send_message(
            chat_id=callback_query.from_user.id,
            text="Для использования бота, пройдите регистрацию",
            reply_markup=register_user_keyboard(),
        )


async def main() -> None:
    """
    Запускает бота.

    :return: None
    """
    await dp.start_polling(bot)
    register_handlers_at_work()  # Запускаем функцию регистрации пользователя, которые на работе
    registration_handler_register_user()  # Запускаем функцию регистрации пользователя
    register_handlers_left()  # Запускаем функцию регистрации пользователя, которые ушли
    register_handler_who_at_work()  # Запускаем функцию регистрации пользователя, которые на работе
    register_handler_reference()  # Регистрация справки


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.warning("Бот остановлен!")
