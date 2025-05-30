# -*- coding: utf-8 -*-
import asyncio
import logging
import sys

from aiogram import F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from loguru import logger

from database import RegisterUserBot, db, recording_data_users_who_launched_bot
from dispatcher import bot, dp, router
from handlers.admin.admin import register_handler_who_at_work
from handlers.user.user_end import register_handlers_left
from handlers.user.user_reference import register_handler_reference
from handlers.user.user_registration import registration_handler_register_user
from handlers.user.user_start import register_handlers_at_work
from keyboards import register_user_keyboard, start_keyboard


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    Обрабатывает команду `/start`.

    :param message: Сообщение от пользователя.
    :return: None
    """
    id_user = message.from_user.id  # id пользователя, отправившего команду /start
    logger.info(f'Пользователь {id_user} отправил команду /start')

    # Записываем данные пользователя, который отправил команду /start
    recording_data_users_who_launched_bot(message)

    db.create_tables([RegisterUserBot])
    user = RegisterUserBot.select().where(RegisterUserBot.id_user == id_user).first()

    if user:
        print(user.name, user.surname)
        # Записываем данные пользователя, который зарегистрировался в базе данных
        text = ('👋 Добро пожаловать в бот для учета сотрудников на рабочем месте!\n\n'
                'Этот бот помогает фиксировать ваше присутствие на рабочем месте и уведомлять коллег.\n\n'

                '📌 Основные команды:\n'
                '✅ "На работе" — зарегистрировать приход. Укажите ваши ФИО и адрес магазина (из списка).\n'
                '🏠 "Ушёл" — зарегистрировать уход.\n'
                '📖 "Справка" — повторно показать это сообщение.\n\n'

                '🔔 Уведомления: При отметке прихода или ухода бот автоматически сообщит об этом в общий чат сотрудников.\n'
                '👥 Для администраторов: Доступна кнопка "Кто на работе" для просмотра списка присутствующих. \n'
                '⚠️ Важно: Доступ к боту только для сотрудников компании.\n\n'

                ' Хорошего дня! 😊')
        await bot.send_message(chat_id=message.chat.id, text=text, reply_markup=start_keyboard())
    else:
        print("Пользователь не найден.")
        text = ('Для использования бота, пройдите регистрацию')
        await bot.send_message(chat_id=message.chat.id, text=text, reply_markup=register_user_keyboard())


@router.callback_query(F.data == 'back')
async def back_start_handler(callback_query: CallbackQuery, state: FSMContext) -> None:
    """
    Обрабатывает команду `/start`.

    :param message: Сообщение от пользователя.
    :return: None
    """
    id_user = callback_query.from_user.id  # id пользователя, отправившего команду /start
    logger.info(f'Пользователь {id_user} отправил команду /start')

    text = ('👋 Добро пожаловать в бот для учета сотрудников на рабочем месте!\n\n'
            'Этот бот помогает фиксировать ваше присутствие на рабочем месте и уведомлять коллег.\n\n'

            '📌 Основные команды:\n'
            '✅ "На работе" — зарегистрировать приход. Выберите адрес магазина (из списка).\n'
            '🏠 "Ушёл" — зарегистрировать уход.\n'
            '📖 "Справка" — повторно показать это сообщение.\n\n'

            '🔔 Уведомления: При отметке прихода или ухода бот автоматически сообщит об этом в общий чат сотрудников.\n'
            '👥 Для администраторов: Доступна кнопка "Кто на работе" для просмотра списка присутствующих. \n'
            '⚠️ Важно: Доступ к боту только для сотрудников компании.\n\n'

            ' Хорошего дня! 😊')
    await bot.send_message(chat_id=callback_query.from_user.id, text=text, reply_markup=start_keyboard())


async def main() -> None:
    """
    Запускает бота.

    :return: None
    """
    await dp.start_polling(bot)
    # Запускаем функцию регистрации пользователя, которые на работе
    register_handlers_at_work()
    # Запускаем функцию регистрации пользователя
    registration_handler_register_user()
    # Запускаем функцию регистрации пользователя, которые ушли
    register_handlers_left()
    # Запускаем функцию регистрации пользователя, которые на работе
    register_handler_who_at_work()
    # Регистрация справки
    register_handler_reference()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.warning("Бот остановлен!")
