import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis

from config.config import load_config
from handlers.fill_form import fill_form_router
from handlers.invalid import invalid_router
from handlers.other import other_router
from keyboards.menu_commands import set_main_menu
from middlewares.not_banned import NotBannedMiddleware

# init logger
logger = logging.getLogger(__name__)


# launch bot
async def main():

    # load config
    config = load_config()

    # set basic logging config
    logging.basicConfig(
        level=logging.getLevelName(level=config.log.level),
        format=config.log.format,
        style=config.log.style,
    )

    # init redis and storage
    redis = Redis(host="localhost")
    storage = RedisStorage(redis=redis)

    logger.info("Starting bot")
    # init bot and dispatcher
    bot = Bot(
        token=config.bot.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher(storage=storage)

    # init database and include it into workflow_data
    db: dict[int, dict[str, str | None]] = {}
    dp.workflow_data.update(db=db)

    # setting menu-commands
    await set_main_menu(bot)

    # include routers into dispatcher
    dp.include_router(fill_form_router)
    dp.include_router(invalid_router)
    dp.include_router(other_router)

    # include middlewares into dispatcher
    dp.update.outer_middleware(NotBannedMiddleware())

    # delete webhook and run polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
