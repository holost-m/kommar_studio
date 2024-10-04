from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database.methods import Buttons

def admin_menu():
    to_main_keyboard = InlineKeyboardButton(
        text='В основное меню (в режим пользователя)⬅',
        callback_data='to_main_keyboard'
    )

    lovestory = InlineKeyboardButton(
        text='Lovestory',
        callback_data='a_lovestory'
    )

    family = InlineKeyboardButton(
        text='Семья',
        callback_data='a_family'
    )

    best = InlineKeyboardButton(
        text='Бэсти',
        callback_data='a_best'
    )

    man_of_the_year = InlineKeyboardButton(
        text='Человек года',
        callback_data='a_man_of_the_year'
    )

    corporate = InlineKeyboardButton(
        text='Корпоративные',
        callback_data='a_corporate'
    )

    lookbook = InlineKeyboardButton(
        text='Лукбук',
        callback_data='a_lookbook'
    )

    cost = InlineKeyboardButton(
        text='Стоимость работ',
        callback_data='a_cost'
    )

    faq = InlineKeyboardButton(
        text='FAQ (url статьи) ',
        callback_data='a_faq'
    )

    # Создаем объект инлайн-клавиатуры меню образцов
    samples_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[to_main_keyboard],
                         [lovestory],
                         [family],
                         [best],
                         [man_of_the_year],
                         [corporate],
                         [lookbook],
                         [cost],
                         [faq]])
    return samples_keyboard