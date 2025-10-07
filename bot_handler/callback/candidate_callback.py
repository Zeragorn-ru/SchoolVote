from config_loader import logging
from aiogram import Bot, Router
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.filters.callback_data import CallbackData
from db_handler import DataBase

db = DataBase("base.db")
router: Router = Router()

class CandidateCallback(CallbackData, prefix="candidate"):
    candidate_id: int

class VoteCallback(CallbackData, prefix="vote"):
    cand_id: int

@router.callback_query(CandidateCallback.filter())
async def vote_callback(callback: CallbackQuery, callback_data: CandidateCallback):
    bot: Bot = callback.message.bot

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text = "Голосовать", callback_data = VoteCallback(cand_id = callback_data.candidate_id).pack()), InlineKeyboardButton(text = "<- Назад", callback_data = "list")]
        ])
    
    candidate = (await db.get_candidate_by_id(callback_data.candidate_id))[0]
    
    text = f"<b>{candidate[1]}</b>\n\n{candidate[2]}\n\n<a href='{candidate[3]}'>ТГ канал</a>"

    await bot.edit_message_text(
        chat_id = callback.message.chat.id,
        message_id = callback.message.message_id,
        reply_markup = keyboard,
        text = text,
        parse_mode= "HTML"
        )