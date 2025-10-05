# -*- coding: utf-8 -*-
from aiogram import Bot, Dispatcher, Router
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
import asyncio
from config_loader import config, logging
from bot_handler import routers
import aiogram

try:
    bot: Bot = Bot(config["BOTTOKEN"])
except aiogram.utils.token.TokenValidationError:
    logging.critical("INVALID BOT TOKEN")
    raise

dp: Dispatcher= Dispatcher()

async def on_startup(dispatcher: Dispatcher) -> None:
    logging.info("Bot started")

def routers_register(routers: list) -> None:
    for router in routers:
        dp.include_router(router)

async def main() -> None:
    dp.startup.register(on_startup)
    routers_register(routers)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())