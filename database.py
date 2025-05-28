# -*- coding: utf-8 -*-
from datetime import datetime
from peewee import *
from loguru import logger


db = SqliteDatabase('base.db')


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
        table_name = 'registered_users_start'


def recording_data_users_who_launched_bot(message):
    """
    Записывает в базу данных сотрудников, которые запустили бота

    Args:
        message: Объект сообщения, содержащий информацию о пользователе, который запустил бота
    """
    try:
        db.create_tables([Person])
        Person.create(name=message.from_user.first_name,
                      surname=message.from_user.last_name,
                      id_user=message.from_user.id)
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
    name = CharField()  # имя сотрудника
    surname = CharField()  # фамилия сотрудника
    id_user = IntegerField()  # id пользователя

    class Meta:
        database = db
        table_name = 'registered_users'


def registration_user(message):
    """
    Записывает в базу данных сотрудников, которые зарегистрировались в Telegram боте

    Args:
        message: Объект сообщения, содержащий информацию о пользователе, который зарегистрировался в боте
    """
    try:
        db.create_tables([RegisterUserBot])
        RegisterUserBot.create(name=message.from_user.first_name,
                               surname=message.from_user.last_name,
                               id_user=message.from_user.id)
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
    store_address = CharField()  # адрес магазина
    time_start = DateTimeField()  # время начала работы

    class Meta:
        database = db
        table_name = 'working_start'


def recording_working_start(callback_query, store_address):
    """
    Записывает в базу данных сотрудников, которые начали работать

    Args:
        message: Объект сообщения, содержащий информацию о пользователе, который начал работать
    """
    try:
        db.create_tables([RecordDataWorkingStart])
        RecordDataWorkingStart.create(id_user=callback_query.from_user.id,
                                      name=callback_query.from_user.first_name,
                                      surname=callback_query.from_user.last_name,
                                      store_address=store_address,
                                      time_start=datetime.now())
    except Exception as error:
        logger.exception(error)


db.connect()
