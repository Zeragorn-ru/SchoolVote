# -*- coding: utf-8 -*-
from config_loader import logging
from aiogram import Bot, Router, F
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, FSInputFile, InputMediaPhoto, Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from hashlib import sha3_256

router: Router = Router()

@router.message(Command("start"))
async def start_command(message: Message, state: FSMContext) -> None:
    await state.clear()
    bot = message.bot

    if message.text.replace("/start ", "") == "":
        text = "Отправьте код"
    else:
        text = f"Привет {message.text.replace("/start ", "")}"

    await bot.send_message(
        chat_id = message.chat.id,
        text = text
    )