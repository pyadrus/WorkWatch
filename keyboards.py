# -*- coding: utf-8 -*-
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def start_keyboard():
    """Клавиатура главного меню бота"""
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text='Справка', callback_data='reference'),],
                         [InlineKeyboardButton(text='✅ На работе', callback_data='at_work'),
                          InlineKeyboardButton(text="🏠 Ушёл", callback_data="left")]]
    )


def shops_keyboard():
    """Клавиатура выбора магазинов, для сотрудников"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Литейная 68',
                                  callback_data='foundry_68'),],
            [InlineKeyboardButton(text='Никитина 5',
                                  callback_data='nikitin_5'),],
            [InlineKeyboardButton(text='Московский 154Б',
                                  callback_data='moscow_154b'),],
            [InlineKeyboardButton(text='Московский 34',
                                  callback_data='moscow_34'),],
            [InlineKeyboardButton(text='Авиационная 5А',
                                  callback_data='aviation_5A'),],
            [InlineKeyboardButton(text='Авиационная 13а',
                                  callback_data='aviation_13a'),],
            [InlineKeyboardButton(text='Станке Димитрова 108Б',
                                  callback_data='stanke_dimitrova_108b'),],
            [InlineKeyboardButton(text='Тельмана 68а',
                                  callback_data='telmana_68A'),],
            [InlineKeyboardButton(text='О.Н. Строкина 2',
                                  callback_data='he_strokina_2'),],
            [InlineKeyboardButton(text='Бежицкая 356а',
                                  callback_data='bezitskaya_356a'),],
            [InlineKeyboardButton(text='Крахмалёва 23',
                                  callback_data='krakhmaleva_23'),],
            [InlineKeyboardButton(text='Пушкина 73',
                                  callback_data='pushkin_73'),],
            [InlineKeyboardButton(text='Станке Димитрова 67',
                                  callback_data='stanke_dimitrova_67'),],
            [InlineKeyboardButton(text='Интернационала 15',
                                  callback_data='international_15'),],
            [InlineKeyboardButton(text='Интернационала 25',
                                  callback_data='international_25'),],
            [InlineKeyboardButton(text='Сосновый бор 1А',
                                  callback_data='international_25'),],
            [InlineKeyboardButton(text='Дуки 65',
                                  callback_data='dukeeping_65'),],
        ]
    )
