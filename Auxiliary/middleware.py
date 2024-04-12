from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from typing import Callable, Dict, Any, Awaitable
from sqlalchemy.ext.asyncio import async_sessionmaker

# Промежуточный слой для работы базы данных
class DataBaseSession(BaseMiddleware):
    def __init__(self, session_pool: async_sessionmaker):
        self.session_pool = session_pool

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ):
        async with self.session_pool() as session:
            data["session"] = session
            return await handler(event, data)