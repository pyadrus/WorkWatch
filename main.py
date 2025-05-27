# -*- coding: utf-8 -*-
import asyncio
import logging
import sys
from aiogram.filters import CommandStart
from aiogram.types import Message
from dispatcher import dp, bot
from keyboards import start_keyboard


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    Обрабатывает команду `/start`.

    :param message: Сообщение от пользователя.
    :return: None
    """
    await bot.send_message(chat_id=message.chat.id, text="Привет, я бот-помощник! Я готов помочь тебе с вашими задачами. Что ты хочешь сделать?", reply_markup=start_keyboard())


async def main() -> None:
    """
    Запускает бота.

    :return: None
    """

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
