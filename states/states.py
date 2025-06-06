# -*- coding: utf-8 -*-
from aiogram.fsm.state import State, StatesGroup


class RegisterState(StatesGroup):
    """Регистрация пользователей"""

    name = State()  # имя пользователя
    surname = State()  # фамилия пользователя
    phone = State()  # номер телефона пользователя
    gender = State()  # пол пользователя


class AdminState(StatesGroup):
    """Управление админа"""

    admin_id = State()  # айди админа
    block_id = State()  # айди пользователя, которого надо заблокировать
    unblock_id = State()  # айди пользователя, которого надо разблокировать
