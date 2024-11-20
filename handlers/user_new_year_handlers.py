from aiogram import Router
from aiogram import Bot
from aiogram import F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram.types import CallbackQuery

from keyboards.user_keyboards import (main_keyboard,
                                      samples_keyboard,
                                      to_main_menu_kb)
from service.utils import (dct_admins,
                           is_admin,
                           clean_all_status,
                           save_user)

from database.methods import Buttons, Users
from aiogram.types import (InputFile,
                           InputMediaPhoto)
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


# Инициализируем роутер для обработки пользовательских сообщений
router = Router()


# Создаем кнопку
button = KeyboardButton('Отправить')
# Создаем клавиатуру и добавляем кнопку
keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(button)

# Фильтр на состояние
def new_year_filter(message: Message) -> bool:
    user_id = message.from_user.id
    message_text = message.text

# Нажата кнопка "Заполнить Новогоднюю анкету"
@router.callback_query(F.data == 'new_year_question')
async def process_samples_press(callback: CallbackQuery):
    await callback.message.answer(
        text='Далее Вы можете заполнить новогоднюю анкету.\nНажимайте кнопку "Отправить" для перехода к следующему вопросу',
        reply_markup=keyboard
    )

@router.message(new_year_filter)
async def send_question(message: Message):
    await message.answer(
        text='Главное меню')