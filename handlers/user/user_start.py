# -*- coding: utf-8 -*-
from datetime import datetime

from aiogram import F
from aiogram.types import CallbackQuery
from loguru import logger

from database import (
    recording_working_start_or_end,
    AdminBlockUser,
    is_user_already_registered_today,
    get_registered_user,
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


async def defining_event_by_gender(user, event_men, event_women):
    """
    ✅ Определяет событие в зависимости от пола пользователя

    :param user: объект пользователя
    :param event_men: мужской вариант события
    :param event_women: женский вариант события
    :return event_user: событие в зависимости от пола пользователя
    """
    if user.gender == "мужской":
        event_user: str = event_men
    elif user.gender == "женский":
        event_user: str = event_women

    return event_user


async def send_user_registration_message(callback_query, store_address):
    """
    Отправляет сообщение о регистрации пользователя в группу

    :param callback_query: объект callback_query
    :param store_address: адрес магазина
    """
    user = await get_registered_user(update=callback_query)
    event_user = await defining_event_by_gender(
        user=user, event_men="пришел на работу", event_women="пришла на работу"
    )
    user_link = f"<a href='https://t.me/{user.username}'>{user.name} {user.surname}</a>"

    await bot.send_message(
        chat_id=-1002678330553,  # ID чата, куда отправляется сообщение
        text=(
            f"👤 {user_link} {event_user}\n"
            f"📍 Адрес: {store_address}\n"
            f"📞 Телефон: {user.phone}\n"
            f"🕒 Время: {datetime.now().strftime('%H:%M')}\n"
            f"✅ Чек лист выполнен"
        ),  # Текст сообщения
        parse_mode="HTML",  # Режим разметки текста
        disable_web_page_preview=True,  # Предварительный просмотр страницы
    )
    return user.name, user.surname, user.phone, event_user


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
    """✅ Общий Handler для регистрации пользователя по любому адресу магазина"""
    if await check_user_registration(callback_query):
        return

    store_address = STORE_ADDRESSES[callback_query.data]
    name, surname, phone, event_user_start = await send_user_registration_message(
        callback_query, store_address
    )
    date_event = datetime.now()
    logger.warning(date_event)
    recording_working_start_or_end(
        callback_query,
        name,
        surname,
        store_address,
        phone,
        date_event=date_event,
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
    router.callback_query.register(at_work)
    router.callback_query.register(handle_store_registration)
