# -*- coding: utf-8 -*-
from config_loader import logging
from aiogram import Bot, Router, F
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, FSInputFile, InputMediaPhoto
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters.callback_data import CallbackData
from db_handler import DataBase

db = DataBase("base.db")
router: Router = Router()

class CandidateCallback(CallbackData, prefix="candidate"):
    candidate_id: int

@router.callback_query(F.data == "list")
async def vote_callback(callback: CallbackQuery):
    bot = callback.message.bot

    text = "Выберите кандидата из списка ниже, вы можете ознакомиться с его программой и проголосовать за него"
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text = candidate[1], callback_data = CandidateCallback(candidate_id = candidate[0]).pack())]
        for candidate in await db.get_candidates()])

    await bot.edit_message_text(
        chat_id = callback.message.chat.id,
        message_id = callback.message.message_id,
        reply_markup = keyboard,
        text = text
    )
