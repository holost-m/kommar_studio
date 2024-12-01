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
from states.user_states import fsm


# Инициализируем роутер для обработки пользовательских сообщений
router = Router()

def get_kb(user_id):
    # Создаем кнопку
    text_button = fsm.get_current_button(user_id)
    button = KeyboardButton(text=text_button)
    # Создаем клавиатуру и добавляем кнопку
    keyboard = ReplyKeyboardMarkup(keyboard=[[button]], resize_keyboard=True)
    return keyboard

def get_kb_text(user_id):
    # Создаем кнопку
    return fsm.get_current_button(user_id)



# Фильтр на состояние
def new_year_filter_next(message: Message) -> bool:
    """
    Сработает если у пользователя корректное состояние и он нажал отправить
    :param message:
    :return: bool
    """


    user_id = message.from_user.id
    message_text = message.text

    # если тип нажатие кнопки - обрабатываем любые нажатия, чтобы не ждать пока кнопку нажмет
    if fsm.get_type_question(user_id) == 'press_button':
        return True

    # обработка последнего состояния???????
    condition = (fsm.is_correct_state(user_id) and (message_text == get_kb_text(user_id))
                 or fsm.is_last_state(user_id)) # не будет формироваться клавиатура для последнего
    return condition

# фильтр на callback (пользователь не пользовался анкетой)
def callback_filter(callback: CallbackQuery):
    """
    Сработает только при нажатии на кнопку и если пользователь не проходил анкету,
    или уже прошел, тогда мы покажем ему ответы
    """
    callback_data = callback.data
    user_id = callback.from_user.id
    condition = (callback_data == 'new_year_questions'
                 and fsm.get_state(user_id) is None
                 or fsm.is_last_state(user_id))
    return condition

# фильтр только на текст
def only_text_filter(message: Message) -> bool:
    user_id = message.from_user.id
    message_text = message.text


    condition = (fsm.is_correct_state(user_id)
                 and message_text
                 and fsm.get_type_question(user_id) == 'text')
    return condition

# фильтр для photo_text
def photo_text_filter(message: Message) -> bool:
    user_id = message.from_user.id
    message_text = message.text
    message_photo = message.photo

    condition = ((fsm.is_correct_state(user_id)
                 and fsm.get_type_question(user_id) == 'photo_text')
                 and (message_text or message_photo))
    return condition

def press_button_filter(message: Message) -> bool:
    user_id = message.from_user.id
    return fsm.get_type_question(user_id) == 'press_button'

# Нажата кнопка "Заполнить Новогоднюю анкету". Точка входа
@router.callback_query(callback_filter)
async def process_samples_press(callback: CallbackQuery):
    user_id = callback.from_user.id

    if not fsm.is_last_state(user_id):

        # инициализируем словарь
        fsm.create_answer_tmpl(user_id)
        fsm.next_state(user_id)


        # здесь просто надо давать первый вопрос и все!!!
        text, descr = fsm.get_question(user_id)
        current_state = fsm.get_state(user_id)  # всегда будет 1

        await callback.message.answer(
            text=f'{current_state}. {text}\n\n{descr}', reply_markup=get_kb(user_id))

    elif fsm.is_last_state(user_id):
        await callback.message.answer(
            text='Ваши шашлыки', reply_markup=to_main_menu_kb()
        )

# Переключает состояние и возвращает вопрос по нему
@router.message(new_year_filter_next)
async def send_question(message: Message):
    user_id = message.from_user.id
    fsm.next_state(user_id)

    # получаем текущее состояние
    current_state = fsm.get_state(user_id)

    # если пользователь не ответил на все вопросы
    if int(current_state) != fsm.last_state:
        # получаем вопрос
        text, descr = fsm.get_question(user_id)

        await message.answer(
            text=f'{current_state}. {text}\n\n{descr}', reply_markup=get_kb(user_id))
    else:
        await message.answer(text='Анкета заполнена!', reply_markup=to_main_menu_kb())

# текстовый обработчик
@router.message(only_text_filter)
async def add_text(message: Message):

    """
    Текст, который пришел надо добавить в словарь в редис
    """
    user_id = message.from_user.id
    message_text = message.text
    fsm.add_text(user_id, message_text)
    await message.answer(
        text=f'Нажмите кнопку или добавьте еще информацию', reply_markup=get_kb(user_id))

# photo_text обработчик. добавить их в список
@router.message(photo_text_filter)
async def add_photo_text(message: Message):
    """
    Получить все id photo и добавить их в редис.
    В первом сообщении придет текст и первое фото, в остальных сообщения только фото
    Поэтому эта функция будет срабатывать столько раз, сколько пришло фото
    """
    user_id = message.from_user.id
    message_text = message.text
    message_caption = message.caption
    media_group_id = message.media_group_id

    if message.photo:
        photo_id = message.photo[-1].file_id
        fsm.add_photo(user_id, photo_id)

    if message_text:
        fsm.add_text(user_id, message_text)

    if message_caption:
        fsm.add_text(user_id, message_caption)

    await message.answer(
        text=f'Нажмите кнопку или добавьте еще информацию', reply_markup=get_kb(user_id))