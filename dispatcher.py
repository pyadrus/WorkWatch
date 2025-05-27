# -*- coding: utf-8 -*-
import os
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram import Router
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env')
TOKEN = os.getenv('BOT_TOKEN')  # Токен бота


dp = Dispatcher()

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

router = Router()
dp.include_router(router)
