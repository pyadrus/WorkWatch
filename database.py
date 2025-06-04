# -*- coding: utf-8 -*-
from datetime import datetime

from loguru import logger
from peewee import *

db = SqliteDatabase("base.db")


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


def recording_data_users_who_launched_bot(message):
    """
    Записывает в базу данных сотрудников, которые запустили бота

    Args:
        message: Объект сообщения, содержащий информацию о пользователе, который запустил бота
    """
    try:
        db.create_tables([Person])
        Person.create(
            name=message.from_user.first_name or "",
            surname=message.from_user.last_name or "",
            id_user=message.from_user.id,
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

    Args:
        callback: Объект колбэка, содержащий информацию о пользователе.
        name (str): Имя сотрудника.
        surname (str): Фамилия сотрудника.
        phone (str): Телефон сотрудника.
        gender (str): Пол сотрудника.
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
    event_user = CharField()  # событие пользователя
    store_address = CharField()  # адрес магазина
    phone = CharField()  # телефон сотрудника
    time_start = DateTimeField()  # время начала работы

    class Meta:
        database = db
        table_name = "working_user"


def recording_working_start(
    callback_query, name, surname, event_user, store_address, phone
):
    """
    Записывает в базу данных сотрудников, которые начали работать

    Args:
        message: Объект сообщения, содержащий информацию о пользователе, который начал работать
    """
    try:
        db.create_tables([RecordDataWorkingStart])
        RecordDataWorkingStart.create(
            id_user=callback_query.from_user.id,
            name=name,
            surname=surname,
            event_user=event_user,
            store_address=store_address,
            phone=phone,
            time_start=datetime.now(),
        )
    except Exception as error:
        logger.exception(error)


db.connect()
