import asyncio
import logging

from aiogram import Bot, Dispatcher

# импорт файлов проекта

from handlers import (user_handlers,
                      other_handlers,
                      admin_handlers,
                      user_new_year_handlers)
from settings import TOKEN



# Инициализируем логгер
logger = logging.getLogger(__name__)


# Функция конфигурирования и запуска бота
async def main():
    # Конфигурируем логирование
    logging.basicConfig(
        level=logging.ERROR,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')

    # Выводим в консоль информацию о начале запуска бота
    logger.info('Starting bot')



    # Инициализируем бот и диспетчер
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    # Регистриуем роутеры в диспетчере
    dp.include_router(user_handlers.router)
    dp.include_router(user_new_year_handlers.router)
    dp.include_router(admin_handlers.router)
    dp.include_router(other_handlers.router)

    print('Bot is running')
    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
