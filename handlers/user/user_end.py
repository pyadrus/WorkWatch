# -*- coding: utf-8 -*-
from datetime import datetime

from aiogram import F
from aiogram.types import CallbackQuery
from loguru import logger

from database import RegisterUserBot, db, recording_working_start_or_end, AdminBlockUser
from dispatcher import bot, router
from handlers.user.user_start import (
    defining_event_by_gender,
    reads_table_with_registered_users,
)
from keyboards.keyboards import shops_keyboard_end, start_menu_keyboard


@router.callback_query(F.data == "left")
async def left(callback_query: CallbackQuery):
    """✅ Регистрация пользователей и запись данных в базу данных"""
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
        text="Выберите из списка адрес магазина",
        reply_markup=shops_keyboard_end(),
    )


async def send_user_registration_message_end(callback_query, store_address):
    """
    Обработка и отправка сообщения в группу

    Args:
        callback_query (CallbackQuery): Объект запроса от пользователя.
        store_address (str): Адрес магазина.

    Returns:
        None
    """
    user = await reads_table_with_registered_users(callback_query)
    event_user = await defining_event_by_gender(
        user=user, event_men="покинул работу", event_women="покинул работу"
    )
    user_link = f"<a href='https://t.me/{user.username}'>{user.name} {user.surname}</a>"
    await bot.send_message(
        chat_id=-1002678330553,  # ID чата, куда отправляется сообщение
        text=(
            f"👤 {user_link} {event_user}\n"
            f"📍 Адрес: {store_address}\n"
            f"📞 Телефон: {user.phone}\n"
            f"🕒 Время: {datetime.now().strftime("%H:%M")}"
        ),  # Текст сообщения
        parse_mode="HTML",  # Режим разметки текста
        disable_web_page_preview=True,  # Предварительный просмотр страницы
    )
    return user.name, user.surname, event_user, user.phone


# Словарь соответствий между callback.data и адресами магазинов
STORE_ADDRESSES_END = {
    "foundry_68_end": "Литейная 68",
    "nikitin_5_end": "Никитина 5",
    "moscow_154b_end": "Московский 154Б",
    "moscow_34_end": "Московский 34",
    "aviation_5A_end": "Авиационная 5А",
    "aviation_13a_end": "Авиационная 13А",
    "telmana_68A_end_end": "Тельмана 68А",
    "he_strokina_2_end": "О.Н. Строкина 2",
    "bezitskaya_356a_end": "Бежицкая 356а",
    "krakhmaleva_23_end": "Крахмалёва 23",
    "pushkin_73_end": "Пушкина 73",
    "dukeeping_65_end": "Дуки 65",
    "international_15_end": "Интернационала 15",
    "international_25_end": "Интернационала 25",
    "sosnovy_bor_1A_end": "Сосновый бор 1А",
    "stanke_dimitrova_67_end": "Станке Димитрова 67",
    "stanke_dimitrova_108b_end": "Станке Димитрова 108Б",
}


@router.callback_query(F.data.in_(STORE_ADDRESSES_END.keys()))
async def handle_store_end(callback_query: CallbackQuery):
    """✅ Обработчик выхода из смены для всех магазинов"""
    await bot.send_message(
        chat_id=callback_query.from_user.id,
        text="До свидания!",
        reply_markup=start_menu_keyboard(),
    )

    store_address = STORE_ADDRESSES_END[callback_query.data]
    name, surname, event_user_end, phone = await send_user_registration_message_end(
        callback_query, store_address
    )

    recording_working_start_or_end(
        callback_query,
        name,
        surname,
        store_address,
        phone,
        event_user_end=event_user_end,
        time_end=datetime.now(),
    )


def register_handlers_left():
    """Регистрация хэндлеров, кто покинул работу"""
    router.callback_query.register(left, text="at_work")
    router.callback_query.register(handle_store_end)
