# -*- coding: utf-8 -*-
from datetime import datetime

from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from loguru import logger

from database import RegisterUserBot, db, recording_working_start, AdminBlockUser
from dispatcher import bot, router
from keyboards.keyboards import shops_keyboard_start, start_menu_keyboard


@router.callback_query(F.data == "at_work")
async def at_work(callback_query: CallbackQuery, state: FSMContext):
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
        reply_markup=shops_keyboard_start(),
    )


async def send_user_registration_message(callback_query, store_address):
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
        event_user = "пришел на работу"
    elif user.gender == "женский":
        event_user = "пришла на работу"

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
    return user.name, user.surname, "на работе", user.phone


@router.callback_query(F.data == "foundry_68")
async def foundry_68(callback_query: CallbackQuery, state: FSMContext):
    """✅ Регистрация пользователя и запись данных в базу данных, адрес магазина Литейная 68"""
    try:
        await bot.send_message(
            chat_id=callback_query.from_user.id,
            text="Вы зарегистрированы. Хорошего дня!",
            reply_markup=start_menu_keyboard(),
        )

        name, surname, event_user, phone = await send_user_registration_message(
            callback_query, "Литейная 68"
        )
        recording_working_start(
            callback_query, name, surname, event_user, "Литейная 68", phone
        )
    except Exception as e:
        logger.exception(e)


@router.callback_query(F.data == "nikitin_5")
async def nikitin_5(callback_query: CallbackQuery, state: FSMContext):
    """✅ Регистрация пользователя и запись данных в базу данных, адрес магазина Никитина 5"""
    await bot.send_message(
        chat_id=callback_query.from_user.id,
        text="Вы зарегистрированы. Хорошего дня!",
        reply_markup=start_menu_keyboard(),
    )
    name, surname, event_user, phone = await send_user_registration_message(
        callback_query, "Никитина 5"
    )
    recording_working_start(
        callback_query, name, surname, event_user, "Никитина 5", phone
    )


@router.callback_query(F.data == "moscow_154b")
async def moscow_154b(callback_query: CallbackQuery, state: FSMContext):
    """✅ Регистрация пользователя и запись данных в базу данных, адрес магазина Московский 154Б"""
    await bot.send_message(
        chat_id=callback_query.from_user.id,
        text="Вы зарегистрированы. Хорошего дня!",
        reply_markup=start_menu_keyboard(),
    )
    name, surname, event_user, phone = await send_user_registration_message(
        callback_query, "Московский 154Б"
    )
    recording_working_start(
        callback_query, name, surname, event_user, "Московский 154Б", phone
    )


@router.callback_query(F.data == "moscow_34")
async def moscow_34(callback_query: CallbackQuery, state: FSMContext):
    """✅ Регистрация пользователя и запись данных в базу данных, адрес магазина Московский 34"""
    await bot.send_message(
        chat_id=callback_query.from_user.id,
        text="Вы зарегистрированы. Хорошего дня!",
        reply_markup=start_menu_keyboard(),
    )
    name, surname, event_user, phone = await send_user_registration_message(
        callback_query, "Московский 34"
    )
    recording_working_start(
        callback_query, name, surname, event_user, "Московский 34", phone
    )


@router.callback_query(F.data == "aviation_5A")
async def aviation_5A(callback_query: CallbackQuery, state: FSMContext):
    """✅ Регистрация пользователя и запись данных в базу данных, адрес магазина Авиационная 5А"""
    await bot.send_message(
        chat_id=callback_query.from_user.id,
        text="Вы зарегистрированы. Хорошего дня!",
        reply_markup=start_menu_keyboard(),
    )
    name, surname, event_user, phone = await send_user_registration_message(
        callback_query, "Авиационная 5А"
    )
    recording_working_start(
        callback_query, name, surname, event_user, "Авиационная 5А", phone
    )


@router.callback_query(F.data == "aviation_13a")
async def aviation_13a(callback_query: CallbackQuery, state: FSMContext):
    """✅ Регистрация пользователя и запись данных в базу данных, адрес магазина Авиационная 13А"""
    await bot.send_message(
        chat_id=callback_query.from_user.id,
        text="Вы зарегистрированы. Хорошего дня!",
        reply_markup=start_menu_keyboard(),
    )
    name, surname, event_user, phone = await send_user_registration_message(
        callback_query, "Авиационная 13А"
    )
    recording_working_start(
        callback_query, name, surname, event_user, "Авиационная 13А", phone
    )


@router.callback_query(F.data == "telmana_68A")
async def telmana_68A(callback_query: CallbackQuery, state: FSMContext):
    """✅ Регистрация пользователя и запись данных в базу данных, адрес магазина Тельмана 68А"""
    await bot.send_message(
        chat_id=callback_query.from_user.id,
        text="Вы зарегистрированы. Хорошего дня!",
        reply_markup=start_menu_keyboard(),
    )
    name, surname, event_user, phone = await send_user_registration_message(
        callback_query, "Тельмана 68А"
    )
    recording_working_start(
        callback_query, name, surname, event_user, "Тельмана 68А", phone
    )


@router.callback_query(F.data == "he_strokina_2")
async def he_strokina_2(callback_query: CallbackQuery, state: FSMContext):
    """✅ Регистрация пользователя и запись данных в базу данных, адрес магазина О.Н. Строкина 2"""
    await bot.send_message(
        chat_id=callback_query.from_user.id,
        text="Вы зарегистрированы. Хорошего дня!",
        reply_markup=start_menu_keyboard(),
    )
    name, surname, event_user, phone = await send_user_registration_message(
        callback_query, "О.Н. Строкина 2"
    )
    recording_working_start(
        callback_query, name, surname, event_user, "О.Н. Строкина 2", phone
    )


@router.callback_query(F.data == "bezitskaya_356a")
async def bezitskaya_356a(callback_query: CallbackQuery, state: FSMContext):
    """✅ Регистрация пользователя и запись данных в базу данных, адрес магазина Бежицкая 356а"""
    await bot.send_message(
        chat_id=callback_query.from_user.id,
        text="Вы зарегистрированы. Хорошего дня!",
        reply_markup=start_menu_keyboard(),
    )
    name, surname, event_user, phone = await send_user_registration_message(
        callback_query, "Бежицкая 356а"
    )
    recording_working_start(
        callback_query, name, surname, event_user, "Бежицкая 356а", phone
    )


@router.callback_query(F.data == "krakhmaleva_23")
async def krakhmaleva_23(callback_query: CallbackQuery, state: FSMContext):
    """✅ Регистрация пользователя и запись данных в базу данных, адрес магазина Крахмалёва 23"""
    await bot.send_message(
        chat_id=callback_query.from_user.id,
        text="Вы зарегистрированы. Хорошего дня!",
        reply_markup=start_menu_keyboard(),
    )
    name, surname, event_user, phone = await send_user_registration_message(
        callback_query, "Крахмалёва 23"
    )
    recording_working_start(
        callback_query, name, surname, event_user, "Крахмалёва 23", phone
    )


@router.callback_query(F.data == "pushkin_73")
async def pushkin_73(callback_query: CallbackQuery, state: FSMContext):
    """✅ Регистрация пользователя и запись данных в базу данных, адрес магазина Пушкина 73"""
    await bot.send_message(
        chat_id=callback_query.from_user.id,
        text="Вы зарегистрированы. Хорошего дня!",
        reply_markup=start_menu_keyboard(),
    )
    name, surname, event_user, phone = await send_user_registration_message(
        callback_query, "Пушкина 73"
    )
    recording_working_start(
        callback_query, name, surname, event_user, "Пушкина 73", phone
    )


@router.callback_query(F.data == "dukeeping_65")
async def dukeeping_65(callback_query: CallbackQuery, state: FSMContext):
    """✅ Регистрация пользователя и запись данных в базу данных, адрес магазина Дуки 65"""
    await bot.send_message(
        chat_id=callback_query.from_user.id,
        text="Вы зарегистрированы. Хорошего дня!",
        reply_markup=start_menu_keyboard(),
    )
    name, surname, event_user, phone = await send_user_registration_message(
        callback_query, "Дуки 65"
    )
    recording_working_start(callback_query, name, surname, event_user, "Дуки 65", phone)


@router.callback_query(F.data == "international_15")
async def international_15(callback_query: CallbackQuery, state: FSMContext):
    """✅ Регистрация пользователя и запись данных в базу данных, адрес магазина Интернационала 15"""
    await bot.send_message(
        chat_id=callback_query.from_user.id,
        text="Вы зарегистрированы. Хорошего дня!",
        reply_markup=start_menu_keyboard(),
    )
    name, surname, event_user, phone = await send_user_registration_message(
        callback_query, "Интернационала 15"
    )
    recording_working_start(
        callback_query, name, surname, event_user, "Интернационала 15", phone
    )


@router.callback_query(F.data == "international_25")
async def international_25(callback_query: CallbackQuery, state: FSMContext):
    """✅ Регистрация пользователя и запись данных в базу данных, адрес магазина Интернационала 25"""
    await bot.send_message(
        chat_id=callback_query.from_user.id,
        text="Вы зарегистрированы. Хорошего дня!",
        reply_markup=start_menu_keyboard(),
    )
    name, surname, event_user, phone = await send_user_registration_message(
        callback_query, "Интернационала 25"
    )
    recording_working_start(
        callback_query, name, surname, event_user, "Интернационала 25", phone
    )


@router.callback_query(F.data == "sosnovy_bor_1A")
async def sosnovy_bor_1A(callback_query: CallbackQuery, state: FSMContext):
    """✅ Регистрация пользователя и запись данных в базу данных, адрес магазина Сосновый бор 1А"""
    await bot.send_message(
        chat_id=callback_query.from_user.id,
        text="Вы зарегистрированы. Хорошего дня!",
        reply_markup=start_menu_keyboard(),
    )
    name, surname, event_user, phone = await send_user_registration_message(
        callback_query, "Сосновый бор 1А"
    )
    recording_working_start(
        callback_query, name, surname, event_user, "Сосновый бор 1А", phone
    )


@router.callback_query(F.data == "stanke_dimitrova_67")
async def stanke_dimitrova_67(callback_query: CallbackQuery, state: FSMContext):
    """✅ Регистрация пользователя и запись данных в базу данных, адрес магазина Станке Димитрова 67"""
    await bot.send_message(
        chat_id=callback_query.from_user.id,
        text="Вы зарегистрированы. Хорошего дня!",
        reply_markup=start_menu_keyboard(),
    )
    name, surname, event_user, phone = await send_user_registration_message(
        callback_query, "Станке Димитрова 67"
    )
    recording_working_start(
        callback_query, name, surname, event_user, "Станке Димитрова 67", phone
    )


@router.callback_query(F.data == "stanke_dimitrova_108b")
async def stanke_dimitrova_108b(callback_query: CallbackQuery, state: FSMContext):
    """✅ Регистрация пользователя и запись данных в базу данных, адрес магазина Станке Димитрова 108Б"""
    await bot.send_message(
        chat_id=callback_query.from_user.id,
        text="Вы зарегистрированы. Хорошего дня!",
        reply_markup=start_menu_keyboard(),
    )
    name, surname, event_user, phone = await send_user_registration_message(
        callback_query, "Станке Димитрова 108Б"
    )
    recording_working_start(
        callback_query, name, surname, event_user, "Станке Димитрова 108Б", phone
    )


def register_handlers_at_work():
    """Регистрация хэндлеров, на работе"""
    router.callback_query.register(at_work, text="at_work")
    router.callback_query.register(foundry_68, text="foundry_68")
    router.callback_query.register(nikitin_5, text="nikitin_5")
    router.callback_query.register(moscow_154b, text="moscow_154b")
    router.callback_query.register(moscow_34, text="moscow_34")
    router.callback_query.register(aviation_5A, text="aviation_5A")
    router.callback_query.register(aviation_13a, text="aviation_13a")
    router.callback_query.register(telmana_68A, text="telmana_68A")
    router.callback_query.register(he_strokina_2, text="he_strokina_2")
    router.callback_query.register(bezitskaya_356a, text="bezitskaya_356a")
    router.callback_query.register(krakhmaleva_23, text="krakhmaleva_23")
    router.callback_query.register(pushkin_73, text="pushkin_73")
    router.callback_query.register(dukeeping_65, text="dukeeping_65")
    router.callback_query.register(international_15, text="international_15")
    router.callback_query.register(international_25, text="international_25")
    router.callback_query.register(sosnovy_bor_1A, text="sosnovy_bor_1A")
    router.callback_query.register(stanke_dimitrova_67, text="stanke_dimitrova_67")
    router.callback_query.register(stanke_dimitrova_108b, text="stanke_dimitrova_108b")
