from aiogram import Router
from aiogram.types import Message
from service.utils import (is_admin,
                           dct_admins)

from keyboards.user_keyboards import main_keyboard
from states.user_states import fsm

router = Router()

def echo_filter(message: Message) -> bool:
    """
    Будет работать если пользователь анкету не проходил или уже все прошел
    """
    user_id = message.from_user.id
    message_text = message.text
    message_photo = message.photo
    return not fsm.is_correct_state(user_id)


@router.message(echo_filter)
async def send_echo(message: Message):
    id = message.from_user.id
    await message.answer(
        text='Главное меню',
        reply_markup=main_keyboard(is_admin(dct_admins, id))
    )