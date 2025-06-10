# -*- coding: utf-8 -*-
from datetime import datetime

from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from loguru import logger

from database import RegisterUserBot, db, recording_working_start_or_end, AdminBlockUser
from dispatcher import bot, router
from keyboards.keyboards import shops_keyboard_end, start_menu_keyboard


@router.callback_query(F.data == "left")
async def left(callback_query: CallbackQuery, state: FSMContext):
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
    db.create_tables([RegisterUserBot])
    user = (
        RegisterUserBot.select()
        .where(RegisterUserBot.id_user == callback_query.from_user.id)
        .first()
    )

    if user.gender == "мужской":
        event_user_end = "покинул работу"
    elif user.gender == "женский":
        event_user_end = "покинула работу"

    now = datetime.now().strftime("%H:%M")
    user_link = f"<a href='https://t.me/{user.username}'>{user.name} {user.surname}</a>"
    await bot.send_message(
        chat_id=-1002678330553,  # ID чата, куда отправляется сообщение
        text=(
            f"👤 {user_link} {event_user_end}\n"
            f"📍 Адрес: {store_address}\n"
            f"📞 Телефон: {user.phone}\n"
            f"🕒 Время: {now}"
        ),  # Текст сообщения
        parse_mode="HTML",  # Режим разметки текста
        disable_web_page_preview=True,  # Предварительный просмотр страницы
    )
    return user.name, user.surname, event_user_end, user.phone


@router.callback_query(F.data == "foundry_68_end")
async def foundry_68_end(callback_query: CallbackQuery, state: FSMContext):
    """✅ Регистрация пользователя и запись данных в базу данных, адрес магазина Литейная 68"""
    try:
        await bot.send_message(
            chat_id=callback_query.from_user.id,
            text="До свидания!",
            reply_markup=start_menu_keyboard(),
        )
        store_address = "Литейная 68"
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
    except Exception as e:
        logger.exception(e)


@router.callback_query(F.data == "nikitin_5_end")
async def nikitin_5_end(callback_query: CallbackQuery, state: FSMContext):
    """✅ Регистрация пользователя и запись данных в базу данных, адрес магазина Никитина 5"""
    await bot.send_message(
        chat_id=callback_query.from_user.id,
        text="До свидания!",
        reply_markup=start_menu_keyboard(),
    )
    store_address = "Никитина 5"
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


@router.callback_query(F.data == "moscow_154b_end")
async def moscow_154b_end(callback_query: CallbackQuery, state: FSMContext):
    """✅ Регистрация пользователя и запись данных в базу данных, адрес магазина Московский 154Б"""
    await bot.send_message(
        chat_id=callback_query.from_user.id,
        text="До свидания!",
        reply_markup=start_menu_keyboard(),
    )
    store_address = "Московский 154Б"
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


@router.callback_query(F.data == "moscow_34_end")
async def moscow_34_end(callback_query: CallbackQuery, state: FSMContext):
    """✅ Регистрация пользователя и запись данных в базу данных, адрес магазина Московский 34"""
    await bot.send_message(
        chat_id=callback_query.from_user.id,
        text="До свидания!",
        reply_markup=start_menu_keyboard(),
    )
    store_address = "Московский 34"
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


@router.callback_query(F.data == "aviation_5A_end")
async def aviation_5A_end(callback_query: CallbackQuery, state: FSMContext):
    """✅ Регистрация пользователя и запись данных в базу данных, адрес магазина Авиационная 5А"""
    await bot.send_message(
        chat_id=callback_query.from_user.id,
        text="До свидания!",
        reply_markup=start_menu_keyboard(),
    )
    store_address = "Авиационная 5А"
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


@router.callback_query(F.data == "aviation_13a_end")
async def aviation_13a_end(callback_query: CallbackQuery, state: FSMContext):
    """✅ Регистрация пользователя и запись данных в базу данных, адрес магазина Авиационная 13А"""
    await bot.send_message(
        chat_id=callback_query.from_user.id,
        text="До свидания!",
        reply_markup=start_menu_keyboard(),
    )
    store_address = "Авиационная 13А"
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


@router.callback_query(F.data == "telmana_68A_end_end")
async def telmana_68A_end_end(callback_query: CallbackQuery, state: FSMContext):
    """✅ Регистрация пользователя и запись данных в базу данных, адрес магазина Тельмана 68А"""
    await bot.send_message(
        chat_id=callback_query.from_user.id,
        text="До свидания!",
        reply_markup=start_menu_keyboard(),
    )
    store_address = "Тельмана 68А"
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


@router.callback_query(F.data == "he_strokina_2_end")
async def he_strokina_2_end(callback_query: CallbackQuery, state: FSMContext):
    """✅ Регистрация пользователя и запись данных в базу данных, адрес магазина О.Н. Строкина 2"""
    await bot.send_message(
        chat_id=callback_query.from_user.id,
        text="До свидания!",
        reply_markup=start_menu_keyboard(),
    )
    store_address = "О.Н. Строкина 2"
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


@router.callback_query(F.data == "bezitskaya_356a_end")
async def bezitskaya_356a_end(callback_query: CallbackQuery, state: FSMContext):
    """✅ Регистрация пользователя и запись данных в базу данных, адрес магазина Бежицкая 356а"""
    await bot.send_message(
        chat_id=callback_query.from_user.id,
        text="До свидания!",
        reply_markup=start_menu_keyboard(),
    )
    store_address = "Бежицкая 356а"
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


@router.callback_query(F.data == "krakhmaleva_23_end")
async def krakhmaleva_23_end(callback_query: CallbackQuery, state: FSMContext):
    """✅ Регистрация пользователя и запись данных в базу данных, адрес магазина Крахмалёва 23"""
    await bot.send_message(
        chat_id=callback_query.from_user.id,
        text="До свидания!",
        reply_markup=start_menu_keyboard(),
    )
    store_address = "Крахмалёва 23"
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


@router.callback_query(F.data == "pushkin_73_end")
async def pushkin_73_end(callback_query: CallbackQuery, state: FSMContext):
    """✅ Регистрация пользователя и запись данных в базу данных, адрес магазина Пушкина 73"""
    await bot.send_message(
        chat_id=callback_query.from_user.id,
        text="До свидания!",
        reply_markup=start_menu_keyboard(),
    )
    store_address = "Пушкина 73"
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


@router.callback_query(F.data == "dukeeping_65_end")
async def dukeeping_65_end(callback_query: CallbackQuery, state: FSMContext):
    """✅ Регистрация пользователя и запись данных в базу данных, адрес магазина Дуки 65"""
    await bot.send_message(
        chat_id=callback_query.from_user.id,
        text="До свидания!",
        reply_markup=start_menu_keyboard(),
    )
    store_address = "Дуки 65"
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


@router.callback_query(F.data == "international_15_end")
async def international_15_end(callback_query: CallbackQuery, state: FSMContext):
    """✅ Регистрация пользователя и запись данных в базу данных, адрес магазина Интернационала 15"""
    await bot.send_message(
        chat_id=callback_query.from_user.id,
        text="До свидания!",
        reply_markup=start_menu_keyboard(),
    )
    store_address = "Интернационала 15"
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


@router.callback_query(F.data == "international_25_end")
async def international_25_end(callback_query: CallbackQuery, state: FSMContext):
    """✅ Регистрация пользователя и запись данных в базу данных, адрес магазина Интернационала 25"""
    await bot.send_message(
        chat_id=callback_query.from_user.id,
        text="До свидания!",
        reply_markup=start_menu_keyboard(),
    )
    store_address = "Интернационала 25"
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


@router.callback_query(F.data == "sosnovy_bor_1A_end")
async def sosnovy_bor_1A_end(callback_query: CallbackQuery, state: FSMContext):
    """✅ Регистрация пользователя и запись данных в базу данных, адрес магазина Сосновый бор 1А"""
    await bot.send_message(
        chat_id=callback_query.from_user.id,
        text="До свидания!",
        reply_markup=start_menu_keyboard(),
    )
    store_address = "Сосновый бор 1А"
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


@router.callback_query(F.data == "stanke_dimitrova_67_end")
async def stanke_dimitrova_67_end(callback_query: CallbackQuery, state: FSMContext):
    """✅ Регистрация пользователя и запись данных в базу данных, адрес магазина Станке Димитрова 67"""
    await bot.send_message(
        chat_id=callback_query.from_user.id,
        text="До свидания!",
        reply_markup=start_menu_keyboard(),
    )
    store_address = "Станке Димитрова 67"
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


@router.callback_query(F.data == "stanke_dimitrova_108b_end")
async def stanke_dimitrova_108b_end(callback_query: CallbackQuery, state: FSMContext):
    """✅ Регистрация пользователя и запись данных в базу данных, адрес магазина Станке Димитрова 108Б"""
    await bot.send_message(
        chat_id=callback_query.from_user.id,
        text="До свидания!",
        reply_markup=start_menu_keyboard(),
    )
    store_address = "Станке Димитрова 108Б"
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
    router.callback_query.register(foundry_68_end, text="foundry_68_end")
    router.callback_query.register(nikitin_5_end, text="nikitin_5_end")
    router.callback_query.register(moscow_154b_end, text="moscow_154b_end")
    router.callback_query.register(moscow_34_end, text="moscow_34_end")
    router.callback_query.register(aviation_5A_end, text="aviation_5A_end")
    router.callback_query.register(aviation_13a_end, text="aviation_13a_end")
    router.callback_query.register(telmana_68A_end_end, text="telmana_68A_end_end")
    router.callback_query.register(he_strokina_2_end, text="he_strokina_2_end")
    router.callback_query.register(bezitskaya_356a_end, text="bezitskaya_356a_end")
    router.callback_query.register(krakhmaleva_23_end, text="krakhmaleva_23_end")
    router.callback_query.register(pushkin_73_end, text="pushkin_73_end")
    router.callback_query.register(dukeeping_65_end, text="dukeeping_65_end")
    router.callback_query.register(international_15_end, text="international_15_end")
    router.callback_query.register(international_25_end, text="international_25_end")
    router.callback_query.register(sosnovy_bor_1A_end, text="sosnovy_bor_1A_end")
    router.callback_query.register(
        stanke_dimitrova_67_end, text="stanke_dimitrova_67_end"
    )
    router.callback_query.register(
        stanke_dimitrova_108b_end, text="stanke_dimitrova_108b_end"
    )
