from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database.methods import Buttons

def main_keyboard(is_admin=False):
    # Создаем объекты инлайн-кнопок главного меню
    # url кнопка

    make_order = InlineKeyboardButton(
        text='Сделать заказ (перейти в чат)',
        url=Buttons.get_url('make_order')
    )

    samples = InlineKeyboardButton(
        text='Образцы работ',
        callback_data='samples'
    )

    cost = InlineKeyboardButton(
        text='Стоимость работ',
        callback_data='cost'
    )

    # url кнопка
    faq = InlineKeyboardButton(
        text='FAQ (Часто задаваемые вопросы)',
        url=Buttons.get_url('faq')
    )

    get_promocode = InlineKeyboardButton(
        text='Получить промокод',
        callback_data='get_promocode'
    )

    edit_all = InlineKeyboardButton(
        text='Редактировать (админ)✏️',
        callback_data='edit_all'
    )

    # отправит ексель файл
    get_users = InlineKeyboardButton(
        text='Список пользователей✏️',
        callback_data='get_users'
    )

    # Создаем объект инлайн-клавиатуры главного меню
    if is_admin:
        return InlineKeyboardMarkup(
        inline_keyboard=[[make_order],
                        [samples],
                        [cost],
                        [faq],
                        [get_promocode],
                        [edit_all], # добавили админу
                        [get_users]]) # добавили админу
    else:
        return InlineKeyboardMarkup(
        inline_keyboard=[[make_order],
                        [samples],
                        [cost],
                        [faq],
                        [get_promocode]])


def samples_keyboard():

    # Создаем объекты инлайн-кнопок меню с примерами работ
    to_main_keyboard = InlineKeyboardButton(
        text='В основное меню⬅',
        callback_data='to_main_keyboard'
    )

    lovestory = InlineKeyboardButton(
        text='Lovestory',
        callback_data='lovestory'
    )

    family = InlineKeyboardButton(
        text='Семья',
        callback_data='family'
    )

    best = InlineKeyboardButton(
        text='Бэсти',
        callback_data='best'
    )

    man_of_the_year = InlineKeyboardButton(
        text='Человек года',
        callback_data='man_of_the_year'
    )

    corporate = InlineKeyboardButton(
        text='Корпоративные',
        callback_data='corporate'
    )

    lookbook = InlineKeyboardButton(
        text='Лукбук',
        callback_data='lookbook'
    )

    # Создаем объект инлайн-клавиатуры меню образцов
    samples_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[to_main_keyboard],
                        [lovestory],
                        [family],
                        [best],
                        [man_of_the_year],
                        [corporate],
                        [lookbook]])
    return samples_keyboard


def to_main_menu_kb():
    to_main_keyboard = InlineKeyboardButton(
        text='В основное меню⬅',
        callback_data='to_main_keyboard'
    )

    to_main_menu_kb = InlineKeyboardMarkup(
        inline_keyboard=[[to_main_keyboard]])

    return to_main_menu_kb