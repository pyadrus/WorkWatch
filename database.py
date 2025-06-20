# -*- coding: utf-8 -*-
from datetime import datetime

from loguru import logger
from peewee import *

from date_utility.date_utility import today

db = SqliteDatabase("base.db")


class AdminBlockUser(Model):
    """
    База данных пользователей, которые заблокированы администратором

    Attributes:
       block_id (int): Уникальный идентификатор администратора
    """

    block_id = IntegerField(unique=True)  # id администратора делаем уникальным

    class Meta:
        database = db
        table_name = "block_users"


class AdminBot(Model):
    """
    База данных администраторов Telegram бота

    Attributes:
       id_admin (int): Уникальный идентификатор администратора
    """

    id_admin = IntegerField(unique=True)  # id администратора делаем уникальным

    class Meta:
        database = db
        table_name = "admins_bot"


def is_admin(user_id: int) -> bool:
    """
    Проверяет, является ли пользователь с заданным ID администратором.

    :param user_id: ID пользователя для проверки.
    :return: True, если пользователь — администратор, иначе False.
    """
    try:
        return AdminBot.get_or_none(AdminBot.id_admin == user_id) is not None
    except Exception as e:
        logger.error(f"Ошибка при проверке администратора: {e}")
        return False


class Person(Model):
    """
    База данных сотрудников, которые запустили Telegram бота

    Attributes:
       name (str): Имя сотрудника
       surname (str): Фамилия сотрудника
       id_user (int): Уникальный идентификатор пользователя
    """

    name = CharField()  # имя сотрудника
    surname = CharField()  # фамилия сотрудника
    id_user = IntegerField()  # id пользователя

    class Meta:
        database = db
        table_name = "registered_users_start"


def recording_data_users_who_launched_bot(update):
    """
    Записывает в базу данных сотрудников, которые запустили бота

    Args:
        update: Объект сообщения, содержащий информацию о пользователе, который запустил бота
    """
    try:
        db.create_tables([Person])
        Person.create(
            name=update.from_user.first_name or "",
            surname=update.from_user.last_name or "",
            id_user=update.from_user.id,
        )
    except Exception as error:
        logger.exception(error)


class RegisterUserBot(Model):
    """
    База данных сотрудников, которые зарегистрировались в Telegram боте

    Attributes:
       name (str): Имя сотрудника
       surname (str): Фамилия сотрудника
       id_user (int): Уникальный идентификатор пользователя
    """

    id_user = IntegerField()  # id пользователя
    name_telegram = CharField()  # имя аккаунта телеграмм
    surname_telegram = CharField()  # фамилия аккаунта Telegram
    username = CharField()  # username аккаунта Telegram
    name = CharField()  # имя сотрудника
    surname = CharField()  # фамилия сотрудника
    phone = CharField()  # телефон сотрудника
    gender = CharField()  # пол сотрудника
    registration_date = CharField()  # дата регистрации

    class Meta:
        database = db
        table_name = "registered_users"


def registration_user(callback, name, surname, phone, gender):
    """
    Записывает или обновляет данные сотрудника в базе данных,
    если он зарегистрировался в Telegram боте.
    :param callback: Объект колбэка, содержащий информацию о пользователе.
    :param name: Имя сотрудника.
    :param  surname: Фамилия сотрудника.
    :param phone: Телефон сотрудника.
    :param gender: Пол сотрудника.
    :return: None
    """
    try:
        db.create_tables([RegisterUserBot])
        user, created = RegisterUserBot.get_or_create(
            id_user=callback.from_user.id,
            defaults={
                "name_telegram": callback.from_user.first_name or "",
                "surname_telegram": callback.from_user.last_name or "",  # ✅ Не None
                "username": callback.from_user.username or "",
                "name": name,
                "surname": surname,
                "phone": phone,
                "gender": gender,
                "registration_date": datetime.now(),
            },
        )
        if not created:
            # Если пользователь уже существует — обновляем его данные
            user.name_telegram = callback.from_user.first_name or ""
            user.surname_telegram = callback.from_user.last_name or ""
            user.username = callback.from_user.username or ""
            user.name = name
            user.surname = surname
            user.phone = phone
            user.gender = gender
            user.registration_date = datetime.now()
            user.save()
    except Exception as error:
        logger.exception(error)


class RecordDataWorkingStart(Model):
    """
    База данных сотрудников, которые начали работать

    Attributes:
       id_user (int): Уникальный идентификатор пользователя
       time_start (str): Время начала работы
    """

    id_user = IntegerField()  # id пользователя
    name = CharField()  # имя сотрудника
    surname = CharField()  # фамилия сотрудника
    username = CharField(null=True)  # username аккаунта Telegram
    event_user_start = CharField()  # событие пользователя
    date_event = DateField()  # дата события
    time_start = DateTimeField()  # время начала работы
    event_user_end = CharField(null=True)  # событие пользователя
    time_end = DateTimeField(null=True)  # время окончания работы
    store_address = CharField()  # адрес магазина
    phone = CharField()  # телефон сотрудника

    class Meta:
        database = db
        table_name = "working_user"


def recording_working_start_or_end(
    callback_query,
    name,
    surname,
    store_address,
    phone,
    event_user_start=None,
    event_user_end=None,
    time_start=None,
    time_end=None,
    date_event=None,
):
    """
    Обрабатывает запись начала или окончания работы сотрудника.
    Если есть только event_user_start — создаётся новая запись.
    Если есть только event_user_end — обновляется существующая запись.
    :param callback_query: Объект callback_query, содержащий информацию о пользователе.
    :param name: Имя сотрудника.
    :param surname: Фамилия сотрудника.
    :param store_address: Адрес магазина.
    :param phone: Телефон сотрудника.
    :param event_user_start: Событие начала работы.
    :param event_user_end: Событие окончания работы.
    :param time_start: Время начала работы.
    :param time_end: Время окончания работы.
    :param date_event: Дата события
    """
    try:
        db.create_tables([RecordDataWorkingStart])
        user_id = callback_query.from_user.id

        if event_user_start and not event_user_end:
            # Создаём запись о входе
            data = {
                "id_user": user_id,
                "name": name,
                "surname": surname,
                "username": callback_query.from_user.username or None,
                "event_user_start": event_user_start,
                "date_event": date_event,
                "time_start": time_start,
                "event_user_end": None,
                "time_end": None,
                "store_address": store_address,
                "phone": phone,
            }
            logger.info(f"[ENTRY] Creating work start record: {data}")
            RecordDataWorkingStart.create(**data)

        elif event_user_end and not event_user_start:
            # Обновляем существующую запись
            record = (
                RecordDataWorkingStart.select()
                .where(
                    (RecordDataWorkingStart.id_user == user_id)
                    & (
                        fn.DATE(RecordDataWorkingStart.time_start)
                        == datetime.now().date()
                    )
                    & (RecordDataWorkingStart.event_user_end.is_null(True))
                )
                .order_by(RecordDataWorkingStart.time_start.desc())
                .first()
            )
            if record:
                record.event_user_end = event_user_end
                record.time_end = time_end
                record.save()
                logger.info(f"[EXIT] Updated work end record for user {user_id}")
            else:
                logger.warning(
                    f"[EXIT] No entry record found for user {user_id} to update."
                )

    except Exception as error:
        logger.exception(f"[ERROR] {error}")


async def get_registered_user(update):
    """
    Универсальная функция для получения зарегистрированного пользователя по update-объекту (message или callback_query)

    :param update: объект message или callback_query
    :return: объект пользователя из модели RegisterUserBot или None
    """
    db.create_tables([RegisterUserBot])  # Создаем таблицу, если её нет
    return (
        RegisterUserBot.select()
        .where(RegisterUserBot.id_user == update.from_user.id)
        .first()
    )


def is_user_already_registered_today(user_id):
    """
    Проверяет, есть ли у пользователя запись за сегодняшний день.
    :param user_id: ID пользователя
    """
    try:
        return (
            RecordDataWorkingStart.select()
            .where(
                (RecordDataWorkingStart.id_user == user_id)
                & (fn.DATE(RecordDataWorkingStart.time_start) == today)
                & (RecordDataWorkingStart.event_user_end.is_null(True))  # важно!
            )
            .exists()
        )
    except Exception as e:
        logger.exception(e)
        return False


db.connect()
