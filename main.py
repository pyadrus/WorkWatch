# -*- coding: utf-8 -*-
import asyncio
import logging
import sys
from aiogram.filters import CommandStart
from aiogram.types import Message
from dispatcher import dp, bot
from keyboards import start_keyboard
from peewee import *

db = SqliteDatabase('base.db')


class Person(Model):
    """База данных сотрудников, которые зарегистрировались в телеграмм боте"""
    name = CharField() # имя сотрудника
    peewee = CharField() # фамилия сотрудника

    class Meta:
        database = db
        table_name = 'registered_users'


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    Обрабатывает команду `/start`.

    :param message: Сообщение от пользователя.
    :return: None
    """
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


async def main() -> None:
    """
    Запускает бота.

    :return: None
    """

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
