import asyncio
from aiogram import Bot, Dispatcher
from config.conifg import TELEGRAM_TOKEN
from src.handlers import (
    general_router,
    logging_router,
    parameters_router
)
from src.middlewares import LoggingMiddleware


bot = Bot(token=TELEGRAM_TOKEN)

dp = Dispatcher()
dp.include_router(general_router)
dp.include_router(parameters_router)
dp.include_router(logging_router)
dp.message.middleware(LoggingMiddleware())


async def main() -> None:
    """
    Запускает Telegram-бота и обрабатывает сообщения в режиме long-polling.

    Returns
    --------
    None
    """
    print('Telegram-бот запущен.')
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
