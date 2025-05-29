# -*- coding: utf-8 -*-
from datetime import datetime

from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from loguru import logger

from database import recording_working_start
from dispatcher import bot, router
from keyboards import shops_keyboard, start_menu_keyboard


@router.callback_query(F.data == "at_work")
async def at_work(callback_query: CallbackQuery, state: FSMContext):
    """✅ Регистрация пользователей и запись данных в базу данных"""
    await bot.send_message(
        chat_id=callback_query.from_user.id,
        text='Выберите из списка адрес магазина',
        reply_markup=shops_keyboard()
    )


@router.callback_query(F.data == "foundry_68")
async def foundry_68(callback_query: CallbackQuery, state: FSMContext):
    """✅ Регистрация пользователя и запись данных в базу данных, адрес магазина Литейная 68"""
    try:
        store_address = "Литейная 68"
        await bot.send_message(
            chat_id=callback_query.from_user.id,
            text='Вы зарегистрированы. Хорошего дня!',
            reply_markup=start_menu_keyboard()
        )
        location_user = callback_query.message.location.longitude
        logger.info(f"location_user: {location_user}")
        recording_working_start(callback_query, store_address)
        await bot.send_message(
            chat_id=-1002678330553,
            text=f'{callback_query.from_user.first_name,}, {callback_query.from_user.last_name} пришел на работу {datetime.now()}'
        )
    except Exception as e:
        logger.exception(e)


@router.callback_query(F.data == "nikitin_5")
async def nikitin_5(callback_query: CallbackQuery, state: FSMContext):
    """✅ Регистрация пользователя и запись данных в базу данных, адрес магазина Никитина 5"""
    store_address = "Никитина 5"
    await bot.send_message(
        chat_id=callback_query.from_user.id,
        text='Вы зарегистрированы. Хорошего дня!',
        reply_markup=start_menu_keyboard()
    )
    recording_working_start(callback_query, store_address)
    await bot.send_message(
        chat_id=-1002678330553,
        text=f'{callback_query.from_user.first_name,}, {callback_query.from_user.last_name} пришел на работу {datetime.now()}')


@router.callback_query(F.data == "moscow_154b")
async def moscow_154b(callback_query: CallbackQuery, state: FSMContext):
    """✅ Регистрация пользователя и запись данных в базу данных, адрес магазина Московский 154Б"""
    store_address = "Московский 154Б"
    await bot.send_message(
        chat_id=callback_query.from_user.id,
        text='Вы зарегистрированы. Хорошего дня!',
        reply_markup=start_menu_keyboard()
    )
    recording_working_start(callback_query, store_address)
    await bot.send_message(
        chat_id=-1002678330553,
        text=f'{callback_query.from_user.first_name,}, {callback_query.from_user.last_name} пришел на работу {datetime.now()}')


@router.callback_query(F.data == "moscow_34")
async def moscow_34(callback_query: CallbackQuery, state: FSMContext):
    """✅ Регистрация пользователя и запись данных в базу данных, адрес магазина Московский 34"""
    store_address = "Московский 34"
    await bot.send_message(
        chat_id=callback_query.from_user.id,
        text='Вы зарегистрированы. Хорошего дня!',
        reply_markup=start_menu_keyboard()
    )
    recording_working_start(callback_query, store_address)
    await bot.send_message(
        chat_id=-1002678330553,
        text=f'{callback_query.from_user.first_name,}, {callback_query.from_user.last_name} пришел на работу {datetime.now()}')


@router.callback_query(F.data == "aviation_5A")
async def aviation_5A(callback_query: CallbackQuery, state: FSMContext):
    """✅ Регистрация пользователя и запись данных в базу данных, адрес магазина Авиационная 5А"""
    store_address = "Авиационная 5А"
    await bot.send_message(
        chat_id=callback_query.from_user.id,
        text='Вы зарегистрированы. Хорошего дня!',
        reply_markup=start_menu_keyboard()
    )
    recording_working_start(callback_query, store_address)
    await bot.send_message(
        chat_id=-1002678330553,
        text=f'{callback_query.from_user.first_name,}, {callback_query.from_user.last_name} пришел на работу {datetime.now()}')


@router.callback_query(F.data == "aviation_13a")
async def aviation_13a(callback_query: CallbackQuery, state: FSMContext):
    """✅ Регистрация пользователя и запись данных в базу данных, адрес магазина Авиационная 13А"""
    store_address = "Авиационная 13А"
    await bot.send_message(
        chat_id=callback_query.from_user.id,
        text='Вы зарегистрированы. Хорошего дня!',
        reply_markup=start_menu_keyboard()
    )
    recording_working_start(callback_query, store_address)
    await bot.send_message(
        chat_id=-1002678330553,
        text=f'{callback_query.from_user.first_name,}, {callback_query.from_user.last_name} пришел на работу {datetime.now()}')


@router.callback_query(F.data == "telmana_68A")
async def telmana_68A(callback_query: CallbackQuery, state: FSMContext):
    """✅ Регистрация пользователя и запись данных в базу данных, адрес магазина Тельмана 68А"""
    store_address = "Тельмана 68А"
    await bot.send_message(
        chat_id=callback_query.from_user.id,
        text='Вы зарегистрированы. Хорошего дня!',
        reply_markup=start_menu_keyboard()
    )
    recording_working_start(callback_query, store_address)
    await bot.send_message(
        chat_id=-1002678330553,
        text=f'{callback_query.from_user.first_name,}, {callback_query.from_user.last_name} пришел на работу {datetime.now()}')


@router.callback_query(F.data == "he_strokina_2")
async def he_strokina_2(callback_query: CallbackQuery, state: FSMContext):
    """✅ Регистрация пользователя и запись данных в базу данных, адрес магазина О.Н. Строкина 2"""
    store_address = "О.Н. Строкина 2"
    await bot.send_message(
        chat_id=callback_query.from_user.id,
        text='Вы зарегистрированы. Хорошего дня!',
        reply_markup=start_menu_keyboard()
    )
    recording_working_start(callback_query, store_address)
    await bot.send_message(
        chat_id=-1002678330553,
        text=f'{callback_query.from_user.first_name,}, {callback_query.from_user.last_name} пришел на работу {datetime.now()}')


@router.callback_query(F.data == "bezitskaya_356a")
async def bezitskaya_356a(callback_query: CallbackQuery, state: FSMContext):
    """✅ Регистрация пользователя и запись данных в базу данных, адрес магазина Бежицкая 356а"""
    store_address = "Бежицкая 356а"
    await bot.send_message(
        chat_id=callback_query.from_user.id,
        text='Вы зарегистрированы. Хорошего дня!',
        reply_markup=start_menu_keyboard()
    )
    recording_working_start(callback_query, store_address)
    await bot.send_message(
        chat_id=-1002678330553,
        text=f'{callback_query.from_user.first_name,}, {callback_query.from_user.last_name} пришел на работу {datetime.now()}')


@router.callback_query(F.data == "krakhmaleva_23")
async def krakhmaleva_23(callback_query: CallbackQuery, state: FSMContext):
    """✅ Регистрация пользователя и запись данных в базу данных, адрес магазина Крахмалёва 23"""
    store_address = "Крахмалёва 23"
    await bot.send_message(
        chat_id=callback_query.from_user.id,
        text='Вы зарегистрированы. Хорошего дня!',
        reply_markup=start_menu_keyboard()
    )
    recording_working_start(callback_query, store_address)
    await bot.send_message(
        chat_id=-1002678330553,
        text=f'{callback_query.from_user.first_name,}, {callback_query.from_user.last_name} пришел на работу {datetime.now()}')


@router.callback_query(F.data == "pushkin_73")
async def pushkin_73(callback_query: CallbackQuery, state: FSMContext):
    """✅ Регистрация пользователя и запись данных в базу данных, адрес магазина Пушкина 73"""
    store_address = "Пушкина 73"
    await bot.send_message(
        chat_id=callback_query.from_user.id,
        text='Вы зарегистрированы. Хорошего дня!',
        reply_markup=start_menu_keyboard()
    )
    recording_working_start(callback_query, store_address)
    await bot.send_message(
        chat_id=-1002678330553,
        text=f'{callback_query.from_user.first_name,}, {callback_query.from_user.last_name} пришел на работу {datetime.now()}')


@router.callback_query(F.data == "dukeeping_65")
async def dukeeping_65(callback_query: CallbackQuery, state: FSMContext):
    """✅ Регистрация пользователя и запись данных в базу данных, адрес магазина Дуки 65"""
    store_address = "Дуки 65"
    await bot.send_message(
        chat_id=callback_query.from_user.id,
        text='Вы зарегистрированы. Хорошего дня!',
        reply_markup=start_menu_keyboard()
    )
    recording_working_start(callback_query, store_address)
    await bot.send_message(
        chat_id=-1002678330553,
        text=f'{callback_query.from_user.first_name,}, {callback_query.from_user.last_name} пришел на работу {datetime.now()}')


@router.callback_query(F.data == "international_15")
async def international_15(callback_query: CallbackQuery, state: FSMContext):
    """✅ Регистрация пользователя и запись данных в базу данных, адрес магазина Интернационала 15"""
    store_address = "Интернационала 15"
    await bot.send_message(
        chat_id=callback_query.from_user.id,
        text='Вы зарегистрированы. Хорошего дня!',
        reply_markup=start_menu_keyboard()
    )
    recording_working_start(callback_query, store_address)
    await bot.send_message(
        chat_id=-1002678330553,
        text=f'{callback_query.from_user.first_name,}, {callback_query.from_user.last_name} пришел на работу {datetime.now()}')


@router.callback_query(F.data == "international_25")
async def international_25(callback_query: CallbackQuery, state: FSMContext):
    """✅ Регистрация пользователя и запись данных в базу данных, адрес магазина Интернационала 25"""
    store_address = "Интернационала 25"
    await bot.send_message(
        chat_id=callback_query.from_user.id,
        text='Вы зарегистрированы. Хорошего дня!',
        reply_markup=start_menu_keyboard()
    )
    recording_working_start(callback_query, store_address)
    await bot.send_message(
        chat_id=-1002678330553,
        text=f'{callback_query.from_user.first_name,}, {callback_query.from_user.last_name} пришел на работу {datetime.now()}')


@router.callback_query(F.data == "sosnovy_bor_1A")
async def sosnovy_bor_1A(callback_query: CallbackQuery, state: FSMContext):
    """✅ Регистрация пользователя и запись данных в базу данных, адрес магазина Сосновый бор 1А"""
    store_address = "Сосновый бор 1А"
    await bot.send_message(
        chat_id=callback_query.from_user.id,
        text='Вы зарегистрированы. Хорошего дня!',
        reply_markup=start_menu_keyboard()
    )
    recording_working_start(callback_query, store_address)
    await bot.send_message(
        chat_id=-1002678330553,
        text=f'{callback_query.from_user.first_name,}, {callback_query.from_user.last_name} пришел на работу {datetime.now()}')


@router.callback_query(F.data == "stanke_dimitrova_67")
async def stanke_dimitrova_67(callback_query: CallbackQuery, state: FSMContext):
    """✅ Регистрация пользователя и запись данных в базу данных, адрес магазина Станке Димитрова 67"""
    store_address = "Станке Димитрова 67"
    await bot.send_message(
        chat_id=callback_query.from_user.id,
        text='Вы зарегистрированы. Хорошего дня!',
        reply_markup=start_menu_keyboard()
    )
    recording_working_start(callback_query, store_address)
    await bot.send_message(
        chat_id=-1002678330553,
        text=f'{callback_query.from_user.first_name,}, {callback_query.from_user.last_name} пришел на работу {datetime.now()}')


@router.callback_query(F.data == "stanke_dimitrova_108b")
async def stanke_dimitrova_108b(callback_query: CallbackQuery, state: FSMContext):
    """✅ Регистрация пользователя и запись данных в базу данных, адрес магазина Станке Димитрова 108Б"""
    store_address = "Станке Димитрова 108Б"
    await bot.send_message(
        chat_id=callback_query.from_user.id,
        text='Вы зарегистрированы. Хорошего дня!',
        reply_markup=start_menu_keyboard()
    )
    recording_working_start(callback_query, store_address)
    await bot.send_message(
        chat_id=-1002678330553,
        text=f'{callback_query.from_user.first_name,}, {callback_query.from_user.last_name} пришел на работу {datetime.now()}')


def register_handlers_at_work():
    """Регистрация хэндлеров"""
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
    router.callback_query.register(
        stanke_dimitrova_67, text="stanke_dimitrova_67")
    router.callback_query.register(
        stanke_dimitrova_108b, text="stanke_dimitrova_108b")
