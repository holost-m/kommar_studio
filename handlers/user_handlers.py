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


# Инициализируем роутер для обработки пользовательских сообщений
router = Router()


# Этот хэндлер срабатывает на команду /start
@router.message(CommandStart())
async def process_start_command(message: Message, bot):
    tg_id: int = message.from_user.id
    if tg_id not in Users.get_tg_ids():
        save_user(message.from_user)

    await bot.send_message(762151919, f'Пользователь https://t.me/{message.from_user.username} запустил бота')
    await bot.send_message(459017020, f'Пользователь https://t.me/{message.from_user.username} запустил бота')

    await message.answer(
        text='Главное меню',
        reply_markup=main_keyboard(is_admin(dct_admins, message.from_user.id))
    )


# Нажата кнопка "Образцы работ"
@router.callback_query(F.data == 'samples')
async def process_samples_press(callback: CallbackQuery):
    await callback.message.answer(
        text='Здесь Вы можете просмотреть образцы наших работ',
        reply_markup=samples_keyboard()
    )



# Нажата кнопка "В главное меню"
@router.callback_query(F.data == 'to_main_keyboard')
async def process_to_main(callback: CallbackQuery):
    id = callback.from_user.id
    clean_all_status(dct_admins, id)
    await callback.message.answer(
        text='Главное меню',
        reply_markup=main_keyboard(is_admin(dct_admins, callback.from_user.id))
    )


# Нажата кнопка "Lovestory"
@router.callback_query(F.data == 'lovestory')
async def process_to_lovestory(callback: CallbackQuery):
    data = Buttons.answer('lovestory')
    if data[6]:
        media = [InputMediaPhoto(media=photo[0]) for photo in data[6]]
        await callback.message.answer_media_group(media)
    await callback.message.answer(text=data[5], reply_markup=to_main_menu_kb())

# Нажата кнопка "family"
@router.callback_query(F.data == 'family')
async def process_to_family(callback: CallbackQuery):
    data = Buttons.answer('family')
    if data[6]:
        media = [InputMediaPhoto(media=photo[0]) for photo in data[6]]
        await callback.message.answer_media_group(media)
    await callback.message.answer(text=data[5], reply_markup=to_main_menu_kb())

# Нажата кнопка "best"
@router.callback_query(F.data == 'best')
async def process_to_best(callback: CallbackQuery):
    data = Buttons.answer('best')
    if data[6]:
        media = [InputMediaPhoto(media=photo[0]) for photo in data[6]]
        await callback.message.answer_media_group(media)
    await callback.message.answer(text=data[5], reply_markup=to_main_menu_kb())

# Нажата кнопка "man_of_the_year"
@router.callback_query(F.data == 'man_of_the_year')
async def process_to_man_of_the_year(callback: CallbackQuery):
    data = Buttons.answer('man_of_the_year')
    if data[6]:
        media = [InputMediaPhoto(media=photo[0]) for photo in data[6]]
        await callback.message.answer_media_group(media)
    await callback.message.answer(text=data[5], reply_markup=to_main_menu_kb())

# Нажата кнопка "corporate"
@router.callback_query(F.data == 'corporate')
async def process_to_corporate(callback: CallbackQuery):
    data = Buttons.answer('corporate')
    if data[6]:
        media = [InputMediaPhoto(media=photo[0]) for photo in data[6]]
        await callback.message.answer_media_group(media)
    await callback.message.answer(text=data[5], reply_markup=to_main_menu_kb())

# Нажата кнопка "lookbook"
@router.callback_query(F.data == 'lookbook')
async def process_to_lookbook(callback: CallbackQuery):
    data = Buttons.answer('lookbook')
    if data[6]:
        media = [InputMediaPhoto(media=photo[0]) for photo in data[6]]
        await callback.message.answer_media_group(media)
    await callback.message.answer(text=data[5], reply_markup=to_main_menu_kb())

# Нажата кнопка "cost"
@router.callback_query(F.data == 'cost')
async def process_to_cost(callback: CallbackQuery):
    data = Buttons.answer('cost')
    if data[6]:
        media = [InputMediaPhoto(media=photo[0]) for photo in data[6]]
        await callback.message.answer_media_group(media)
    await callback.message.answer(text=data[5], reply_markup=to_main_menu_kb())

# Нажата кнопка "get_promocode"
@router.callback_query(F.data == 'get_promocode')
async def process_to_cost(callback: CallbackQuery):
    data = Buttons.answer('get_promocode')
    await callback.message.answer(text=data[5],
                                  reply_markup=to_main_menu_kb())

# Нажата кнопка "new_year"
@router.callback_query(F.data == 'new_year')
async def process_to_cost(callback: CallbackQuery):
    data = Buttons.answer('new_year')
    if data[6]:
        media = [InputMediaPhoto(media=photo[0]) for photo in data[6]]
        await callback.message.answer_media_group(media)
    await callback.message.answer(text=data[5], reply_markup=to_main_menu_kb())




