from aiogram import F
from loguru import logger
from dispatcher import bot, router
from database import registration_user
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup

from keyboards import start_keyboard


class RegisterState(StatesGroup):
    name = State()
    surname = State()
    phone = State()

@router.callback_query(F.data == 'registration')
async def registration_user_handler(callback_query: CallbackQuery, state: FSMContext):
    """Регистрация пользователя в Telegram боте"""
    text = ('Для регистрации введите свое имя')
    await bot.send_message(chat_id=callback_query.from_user.id,
                           text=text)
    await state.set_state(RegisterState.name)

@router.message(RegisterState.name)
async def handle_registration_name(message: Message, state: FSMContext):
    """Обработка имени пользователя"""
    user_name = message.text
    await state.update_data(user_name=user_name)
    text = ('Введите свою фамилию')
    await bot.send_message(chat_id=message.from_user.id,
                           text=text)
    await state.set_state(RegisterState.surname)
    
@router.message(RegisterState.surname)
async def handle_registration_surname(message: Message, state: FSMContext):
    """Обработка фамилии пользователя"""
    user_surname = message.text
    await state.update_data(user_surname=user_surname)
    text = ('Введите свой номер телефона')
    await bot.send_message(chat_id=message.from_user.id,
                           text=text)
    await state.set_state(RegisterState.phone)

@router.message(RegisterState.phone)
async def handle_registration_phone(message: Message, state: FSMContext):
    """Обработка номера телефона пользователя"""
    user_phone = message.text
    await state.update_data(user_phone=user_phone)

    user_data = await state.get_data()
    user_name = user_data.get('user_name')
    user_surname = user_data.get('user_surname')
    user_phone = user_data.get('user_phone')
    
    logger.info(f'User: {user_name}, {user_surname}, {user_phone}')
     
    registration_user(message=message, name=user_name, surname=user_surname, phone=user_phone)
    await state.clear()
    text = ('👋 Добро пожаловать в бот для учета сотрудников на рабочем месте!\n\n'
                'Этот бот помогает фиксировать ваше присутствие на рабочем месте и уведомлять коллег.\n\n'

                '📌 Основные команды:\n'
                '✅ "На работе" — зарегистрировать приход. Укажите ваши ФИО и адрес магазина (из списка).\n'
                '🏠 "Ушёл" — зарегистрировать уход.\n'
                '📖 "Справка" — повторно показать это сообщение.\n\n'

                '🔔 Уведомления: При отметке прихода или ухода бот автоматически сообщит об этом в общий чат сотрудников.\n'
                '👥 Для администраторов: Доступна кнопка "Кто на работе" для просмотра списка присутствующих. \n'
                '⚠️ Важно: Доступ к боту только для сотрудников компании.\n\n'

                ' Хорошего дня! 😊')
    await bot.send_message(chat_id=message.chat.id, text=text, reply_markup=start_keyboard())

def registration_handler_register_user():
    """Регистрация хендлеров"""
    router.callback_query.register(registration_user_handler,
                            text='registration')
    router.callback_query.register(handle_registration_name)
    router.callback_query.register(handle_registration_surname)
    router.callback_query.register(handle_registration_phone)
    
