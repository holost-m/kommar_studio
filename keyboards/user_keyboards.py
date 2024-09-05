from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


# Создаем объекты инлайн-кнопок
make_order = InlineKeyboardButton(
    text='Сделать заказ',
    callback_data='make_order'
)

samples = InlineKeyboardButton(
    text='образцы',
    callback_data='samples'
)

cost = InlineKeyboardButton(
    text='Стоимость работ',
    callback_data='cost'
)

faq = InlineKeyboardButton(
    text='FAQ (Часто задаваемые вопросы)',
    callback_data='faq'
)

get_promocode = InlineKeyboardButton(
    text='Получить промокод',
    callback_data='get_promocode'
)

# Создаем объект инлайн-клавиатуры
main_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[make_order],
                    [samples],
                    [cost],
                    [faq],
                    [get_promocode]])