from aiogram import Router
from aiogram import F
from aiogram.types import CallbackQuery
from keyboards.admin_keyboards import admin_menu
from keyboards.user_keyboards import to_main_menu_kb, main_keyboard
from service.utils import dct_admins
from aiogram.types import Message
from service.utils import (dct_admins,
                           clean_all_status,
                           remove_files,
                           is_admin)
from service.xls_writer import Exel_writer
from database.methods import Buttons, Users
from aiogram.types import FSInputFile

router = Router()



# Нажата кнопка "edit_all". Режим редактирования
@router.callback_query(F.data == 'edit_all')
async def process_to_edit_all(callback: CallbackQuery):
    id = callback.from_user.id

    clean_all_status(dct_admins, id)

    await callback.message.answer(text='Выберите кнопку для редактирования',
                                  reply_markup=admin_menu())

# Нажата кнопка "get_users". Отправить ексель файл
@router.callback_query(F.data == 'get_users')
async def process_to_edit_all(callback: CallbackQuery, bot):

    # сохраняем ексель
    Exel_writer.write_to_excel(Users.get_all_users())

    # Путь к файлу
    file_path = 'service/users.xlsx'

    # Создание объекта InputFile
    input_file = FSInputFile(file_path)

    # Отправка файла
    await bot.send_document(callback.from_user.id, document=input_file)

    await callback.message.answer(text='Скачайте файл и перейдите в главное меню',
                                  reply_markup=to_main_menu_kb()
                                  )

# Нажата кнопка "a_lovestory". Режим редактирования
@router.callback_query(F.data == 'a_lovestory')
async def process_to_a_lovestory(callback: CallbackQuery):
    id = callback.from_user.id
    Buttons.delete_photo('lovestory')
    if is_admin(dct_admins, id):
        dct_admins[id]['status'] = 'a_lovestory'
        await callback.message.answer(text='Выберите несколько фото, добавьте их описание одним сообщением')


# Нажата кнопка "a_family". Режим редактирования
@router.callback_query(F.data == 'a_family')
async def process_to_a_family(callback: CallbackQuery):
    id = callback.from_user.id
    Buttons.delete_photo('family')
    if is_admin(dct_admins, id):
        dct_admins[id]['status'] = 'a_family'
        await callback.message.answer(text='Выберите несколько фото, добавьте их описание одним сообщением')

# Нажата кнопка "a_best". Режим редактирования
@router.callback_query(F.data == 'a_best')
async def process_to_a_best(callback: CallbackQuery):
    id = callback.from_user.id
    Buttons.delete_photo('best')
    if is_admin(dct_admins, id):
        dct_admins[id]['status'] = 'a_best'
        await callback.message.answer(text='Выберите несколько фото, добавьте их описание одним сообщением')


# Нажата кнопка "a_man_of_the_year". Режим редактирования
@router.callback_query(F.data == 'a_man_of_the_year')
async def process_to_a_man_of_the_year(callback: CallbackQuery):
    id = callback.from_user.id
    Buttons.delete_photo('man_of_the_year')
    if is_admin(dct_admins, id):
        dct_admins[id]['status'] = 'a_man_of_the_year'
        await callback.message.answer(text='Выберите несколько фото, добавьте их описание одним сообщением')

# Нажата кнопка "a_corporate". Режим редактирования
@router.callback_query(F.data == 'a_corporate')
async def process_to_a_corporate(callback: CallbackQuery):
    id = callback.from_user.id
    Buttons.delete_photo('corporate')
    if is_admin(dct_admins, id):
        dct_admins[id]['status'] = 'a_corporate'
        await callback.message.answer(text='Выберите несколько фото, добавьте их описание одним сообщением')

# Нажата кнопка "a_lookbook". Режим редактирования
@router.callback_query(F.data == 'a_lookbook')
async def process_to_a_lookbook(callback: CallbackQuery):
    id = callback.from_user.id
    Buttons.delete_photo('lookbook')
    if is_admin(dct_admins, id):
        dct_admins[id]['status'] = 'a_lookbook'
        await callback.message.answer(text='Выберите несколько фото, добавьте их описание одним сообщением')


# Нажата кнопка "a_cost". Режим редактирования
@router.callback_query(F.data == 'a_cost')
async def process_to_a_cost(callback: CallbackQuery):
    id = callback.from_user.id
    Buttons.delete_photo('cost')
    if is_admin(dct_admins, id):
        dct_admins[id]['status'] = 'a_cost'
        await callback.message.answer(text='Выберите несколько фото, добавьте их описание одним сообщением')

# Нажата кнопка "a_faq". Режим редактирования
@router.callback_query(F.data == 'a_faq')
async def process_to_a_faq(callback: CallbackQuery):
    id = callback.from_user.id
    if is_admin(dct_admins, id):
        dct_admins[id]['status'] = 'a_faq'
        await callback.message.answer(text='Вставьте корректную ссылку на статью FAQ')










def my_filter_photo_text(message: Message) -> bool:
    id = message.from_user.id
    status_filter = dct_admins[id]['status'] in ['a_lovestory',
                                                 'a_family',
                                                 'a_best',
                                                 'a_man_of_the_year',
                                                 'a_corporate',
                                                 'a_lookbook',
                                                 'a_cost']
    return is_admin(dct_admins, id) and status_filter


@router.message(my_filter_photo_text)
async def edit_info_photo_text(message: Message):
    id = message.from_user.id
    status = dct_admins[id]['status'][2:]

    if message.photo:
        Buttons.save_photo(status, message.photo[-1].file_id)

    if message.caption:
        Buttons.update_text_answer(status, message.caption)


    if dct_admins[id]['status'] and not dct_admins[id]['in_work']:
        dct_admins[id]['in_work'] = True
        await message.answer(
            text='Для выхода из режима редактирования перейдите в главное меню',
            reply_markup=to_main_menu_kb()
        )
    else:
        pass


def my_filter_url(message: Message) -> bool:
    id = message.from_user.id
    status_filter = dct_admins[id]['status'] in ['a_faq']
    return is_admin(dct_admins, id) and status_filter


@router.message(my_filter_url)
async def edit_info_url(message: Message):
    id = message.from_user.id
    status = dct_admins[id]['status'][2:]
    if message.text and message.text.startswith('https://telegra.ph/'):
        Buttons.update_url(status, message.text)
        text = 'Сохранено! Для выхода из режима редактирования перейдите в главное меню'
    else:
        text = 'Некорректный url! Для выхода из режима редактирования перейдите в главное меню'

    await message.answer(
        text=text,
        reply_markup=to_main_menu_kb()
    )