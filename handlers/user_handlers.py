from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from keyboards.user_keyboards import main_keyboard

# Инициализируем роутер для обработки пользовательских сообщений
router = Router()

# Этот хэндлер срабатывает на команду /start
@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer('Привет! Роутеры работают)')