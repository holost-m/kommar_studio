from database.methods import Buttons, Users
from aiogram.types import (InputFile,
                           InputMediaPhoto,
                           BufferedInputFile,
                           FSInputFile)
import os
import random
from aiogram.types.user import User
import datetime
from settings import dct_admins


dct_admins = {459017020: {'status': None, 'in_work': False},  # Маша 'not'/'photo'/'text'
               762151919: {'status': None, 'in_work': False}}  # Миша


def get_photo_text(button_name):
    data = Buttons.answer(button_name)
    text_answer = data[5]
    photos = data[6]
    media = []
    filenames = []
    if photos:

        for i in photos:
            filename = f'photo_tmp/file{random.randint(1000, 99999)}.jpg'
            filenames.append(filename)
            with open(filename, 'wb') as file:
                file.write(i[0])
            photo1 = FSInputFile(filename)
            media.append(InputMediaPhoto(media=photo1))
            # удаляем файл
    return media, text_answer, filenames


def remove_files(filenames):
    for file in filenames:
        os.remove(file)

def is_admin(dct_admins, id):
    return id in dct_admins

def clean_all_status(dct_admins, id):
    if is_admin(dct_admins, id):
        dct_admins[id]['in_work'] = False
        dct_admins[id]['status'] = None

def save_user(user: User):
    dct_user = {}
    tg_id: int = user.id
    first_name: str = user.first_name
    last_name: str = user.last_name
    username: str = user.username
    url: str = f'https://t.me/{username}'
    current_date_iso = str(datetime.datetime.now())

    Users.save_user(tg_id, first_name, last_name, username, url, current_date_iso)



