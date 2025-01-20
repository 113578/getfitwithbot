import sys
from loguru import logger
from aiogram import BaseMiddleware
from aiogram.types import Message


logger.remove()
logger.add(sys.stdout, level='INFO', format='{time} {level} {message}')


class LoggingMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Message, data: dict):
        logger.info(f'Получено сообщение: {event.text}')
        return await handler(event, data)
