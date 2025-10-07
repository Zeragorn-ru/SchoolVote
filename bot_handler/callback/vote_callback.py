from config_loader import logging
from aiogram import Bot, Router
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData
from db_handler import DataBase

db = DataBase("base.db")
router: Router = Router()

class VoteCallback(CallbackData, prefix="vote"):
    cand_id: int

@router.callback_query(VoteCallback.filter())
async def vote_callback(callback: CallbackQuery, callback_data: VoteCallback):
    bot: Bot = callback.message.bot

    cand_id = callback_data.cand_id
    candidate = (await db.get_candidate_by_id(cand_id))[0]
    print(candidate)

    try:
        db.vote(callback.from_user.id, cand_id)

        text = f"Спасибо, ваш голос за {candidate[1]} учтён!"
    
    except Exception as e:
        logging.error(f"Vote error: {e}")
        text = f"Произлошла ошибка СРОЧНО СООБЩИТЕ ТЕХ-АДМИНУ!"

    await bot.edit_message_text(
            chat_id = callback.message.chat.id,
            message_id = callback.message.message_id,
            text = text
        )