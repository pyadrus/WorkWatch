# -*- coding: utf-8 -*-
from aiogram.fsm.state import State, StatesGroup


class RegisterState(StatesGroup):
    name = State()  # имя пользователя
    surname = State()  # фамилия пользователя
    phone = State()  # номер телефона пользователя
    gender = State()  # пол пользователя
