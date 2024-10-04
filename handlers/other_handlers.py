from aiogram import Router
from aiogram.types import Message
from service.utils import (is_admin,
                           dct_admins)

from keyboards.user_keyboards import main_keyboard

router = Router()


@router.message()
async def send_echo(message: Message):
    id = message.from_user.id
    await message.answer(
        text='Главное меню',
        reply_markup=main_keyboard(is_admin(dct_admins, id))
    )