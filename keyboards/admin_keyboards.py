from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database.methods import Buttons

def admin_menu():
    to_main_keyboard = InlineKeyboardButton(
        text='В основное меню (в режим пользователя)⬅',
        callback_data='to_main_keyboard'
    )

    lovestory = InlineKeyboardButton(
        text='Lovestory🔮',
        callback_data='a_lovestory'
    )

    family = InlineKeyboardButton(
        text='Семья🔮',
        callback_data='a_family'
    )

    best = InlineKeyboardButton(
        text='Бэсти🔮',
        callback_data='a_best'
    )

    man_of_the_year = InlineKeyboardButton(
        text='Человек года🔮',
        callback_data='a_man_of_the_year'
    )

    corporate = InlineKeyboardButton(
        text='Корпоративные🔮',
        callback_data='a_corporate'
    )

    lookbook = InlineKeyboardButton(
        text='Лукбук🔮',
        callback_data='a_lookbook'
    )

    cost = InlineKeyboardButton(
        text='Стоимость работ',
        callback_data='a_cost'
    )

    get_promocode = InlineKeyboardButton(
        text='Промокод',
        callback_data='a_get_promocode'
    )

    faq = InlineKeyboardButton(
        text='Ссылка на статью faq (url)',
        callback_data='a_faq'
    )

    make_order = InlineKeyboardButton(
        text='Ссылка на чат (Сделать заказ)',
        callback_data='a_make_order'
    )

    new_year = InlineKeyboardButton(
        text='НОВОГОДНИЙ ЖУРНАЛ',
        callback_data='a_new_year'
    )

    # Создаем объект инлайн-клавиатуры admin_menu
    admin_menu = InlineKeyboardMarkup(
        inline_keyboard=[[to_main_keyboard],
                         [lovestory],
                         [family],
                         [best],
                         [man_of_the_year],
                         [corporate],
                         [lookbook],
                         [cost],
                         [get_promocode],
                         [faq],
                         [make_order],
                         [new_year]])
    return admin_menu