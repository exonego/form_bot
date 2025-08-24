from collections.abc import Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User

from config.config import Config, load_config


class NotBannedMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict], Awaitable],
        event: TelegramObject,
        data: dict,
    ):
        user: User = data.get("event_from_user")
        if user is not None:
            config: Config = load_config()
            if user.id in config.bot.ban_list:
                return

        return await handler(event, data)
