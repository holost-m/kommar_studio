from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database.methods import Buttons

def main_keyboard(is_admin=False):
    # Создаем объекты инлайн-кнопок главного меню
    # url кнопка

    new_year = InlineKeyboardButton(
        text='🎄СОЗДАТЬ ВАШ НОВОГОДНИЙ ЖУРНАЛ🎄',
        callback_data='new_year'
    )

    make_order = InlineKeyboardButton(
        text='✅ЗАКАЗАТЬ (чат с редактором)',
        url=Buttons.get_url('make_order')
    )

    samples = InlineKeyboardButton(
        text='📓Каким будет ваш журнал',
        callback_data='samples'
    )

    cost = InlineKeyboardButton(
        text='💎Стоимость',
        callback_data='cost'
    )

    # url кнопка
    faq = InlineKeyboardButton(
        text='❓FAQ (доставка, сроки, печать, содержание)',
        url=Buttons.get_url('faq')
    )

    get_promocode = InlineKeyboardButton(
        text='💝Получить промокод',
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
        inline_keyboard=[[new_year],
                        [make_order],
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
        text='❤️Капсула «Love is…»',
        callback_data='lovestory'
    )

    family = InlineKeyboardButton(
        text='🤍Капсула «Семья»',
        callback_data='family'
    )

    best = InlineKeyboardButton(
        text='💅Капсула «Бэсти»',
        callback_data='best'
    )

    man_of_the_year = InlineKeyboardButton(
        text='🏆Капсула «Человек года»',
        callback_data='man_of_the_year'
    )

    corporate = InlineKeyboardButton(
        text='📓Журналы для бизнеса',
        callback_data='corporate'
    )

    lookbook = InlineKeyboardButton(
        text='📸Ваш lookbook',
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
    make_order = InlineKeyboardButton(
        text='✅ЗАКАЗАТЬ',
        url=Buttons.get_url('make_order')
    )

    to_main_keyboard = InlineKeyboardButton(
        text='В основное меню⬅',
        callback_data='to_main_keyboard'
    )

    to_main_menu_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [make_order],
            [to_main_keyboard]
            ]
    )

    return to_main_menu_kb