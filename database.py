# -*- coding: utf-8 -*-
from peewee import *


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
    id_user = IntegerField(unique=True)  # id пользователя

    class Meta:
        database = db
        table_name = 'registered_users_start'


def recording_data_users_who_launched_bot(message):
    """
    Записывает в базу данных сотрудников, которые запустили бота

    Args:
        message: Объект сообщения, содержащий информацию о пользователе, который запустил бота
    """
    db.create_tables([Person])
    Person.create(name=message.from_user.first_name,
                  surname=message.from_user.last_name,
                  id_user=message.from_user.id)


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
    id_user = IntegerField(unique=True)  # id пользователя

    class Meta:
        database = db
        table_name = 'registered_users'


def registration_user(message):
    """
    Записывает в базу данных сотрудников, которые зарегистрировались в Telegram боте

    Args:
        message: Объект сообщения, содержащий информацию о пользователе, который зарегистрировался в боте
    """
    db.create_tables([RegisterUserBot])
    RegisterUserBot.create(name=message.from_user.first_name,
                           surname=message.from_user.last_name,
                           id_user=message.from_user.id)


db.connect()
