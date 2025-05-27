import asyncio
import logging
import sys
import os
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

from dotenv import load_dotenv

load_dotenv(dotenv_path='.env')
TOKEN = os.getenv('BOT_TOKEN')  # Токен бота


dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    Ответ на команду `/start`
    """
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")


async def main() -> None:
    """
    Запуск бота
    """
    bot = Bot(token=TOKEN, default=DefaultBotProperties(
        parse_mode=ParseMode.HTML))

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
