# -*- coding: utf-8 -*-
from datetime import datetime
from aiogram import F
from aiogram.types import CallbackQuery
from loguru import logger
from database import (
    RegisterUserBot,
    db,
    recording_working_start_or_end,
    AdminBlockUser,
    is_user_already_registered_today,
)
from dispatcher import bot, router
from keyboards.keyboards import shops_keyboard_start, start_menu_keyboard


# Словарь соответствий между callback.data и адресами магазинов
STORE_ADDRESSES = {
    "foundry_68": "Литейная 68",
    "nikitin_5": "Никитина 5",
    "moscow_154b": "Московский 154Б",
    "moscow_34": "Московский 34",
    "aviation_5A": "Авиационная 5А",
    "aviation_13a": "Авиационная 13А",
    "telmana_68A": "Тельмана 68А",
    "he_strokina_2": "О.Н. Строкина 2",
    "bezitskaya_356a": "Бежицкая 356а",
    "krakhmaleva_23": "Крахмалёва 23",
    "pushkin_73": "Пушкина 73",
    "dukeeping_65": "Дуки 65",
    "international_15": "Интернационала 15",
    "international_25": "Интернационала 25",
    "sosnovy_bor_1A": "Сосновый бор 1А",
    "stanke_dimitrova_67": "Станке Димитрова 67",
    "stanke_dimitrova_108b": "Станке Димитрова 108Б",
}


async def check_user_registration(callback_query):
    if is_user_already_registered_today(callback_query.from_user.id):
        await callback_query.message.answer(
            text="Вы уже отметились сегодня. Повторная регистрация невозможна.",
            reply_markup=start_menu_keyboard(),
        )
        await callback_query.answer()
        return True  # Пользователь уже зарегистрирован
    return False  # Пользователь не зарегистрирован сегодня


async def send_user_registration_message(callback_query, store_address):
    db.create_tables([RegisterUserBot])
    user = (
        RegisterUserBot.select()
        .where(RegisterUserBot.id_user == callback_query.from_user.id)
        .first()
    )
    if user.gender == "мужской":
        event_user_start = "пришел на работу"
    elif user.gender == "женский":
        event_user_start = "пришла на работу"

    user_link = (
        f"<a href='https://t.me/{user.username}'>{user.name}  {user.surname}</a>"
    )
    await bot.send_message(
        chat_id=-1002678330553,  # ID чата, куда отправляется сообщение
        text=(
            f"👤 {user_link} {event_user_start}\n"
            f"📍 Адрес: {store_address}\n"
            f"📞 Телефон: {user.phone}\n"
            f"🕒 Время: {datetime.now().strftime('%H:%M')}\n"
            f"✅ Чек лист выполнен"
        ),
        parse_mode="HTML",
        disable_web_page_preview=True,
    )
    return user.name, user.surname, user.phone, event_user_start


@router.callback_query(F.data == "at_work")
async def at_work(callback_query: CallbackQuery):
    """✅ Показывает список магазинов для начала рабочего дня"""
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
        return

    await bot.send_message(
        chat_id=callback_query.from_user.id,
        text="Выберите из списка адрес магазина",
        reply_markup=shops_keyboard_start(),
    )


@router.callback_query(F.data.in_(STORE_ADDRESSES.keys()))
async def handle_store_registration(callback_query: CallbackQuery):
    """✅ Общий хэндлер для регистрации пользователя по любому адресу магазина"""
    if await check_user_registration(callback_query):
        return

    store_address = STORE_ADDRESSES[callback_query.data]
    name, surname, phone, event_user_start = await send_user_registration_message(
        callback_query, store_address
    )

    recording_working_start_or_end(
        callback_query,
        name,
        surname,
        store_address,
        phone,
        event_user_start=event_user_start,
        time_start=datetime.now(),
    )

    await bot.send_message(
        chat_id=callback_query.from_user.id,
        text="Вы успешно зарегистрированы. Хорошего дня!",
        reply_markup=start_menu_keyboard(),
    )


def register_handlers_at_work():
    """Регистрация всех обработчиков"""
    router.callback_query.register(at_work, F.data == "at_work")
    router.callback_query.register(handle_store_registration)
