# -*- coding: utf-8 -*-
from config_loader import logging
from aiogram import Bot, Router, F
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, FSInputFile, InputMediaPhoto, Message
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from db_handler import DataBase, SchoolUserNotFoundError, SchoolUserAlreadyLinkedError

db = DataBase("base.db")
router: Router = Router()

class InputState(StatesGroup):
    code = State()

@router.message(Command("start"))
async def start_command(message: Message, state: FSMContext) -> None:
    await state.clear()
    bot = message.bot
    code = message.text.replace("/start", "")

    if not ((message.from_user.id,) in await db.get_users_tg_ids()):
        logging.info(f"Try add user: {message.from_user.id}:{message.from_user.username}")
        await db.add_tg_user(message.from_user.id, message.from_user.username)

    if code == "":
        text = f"Привет {message.from_user.full_name}, отправь свой код для голосований."
        await state.set_state(InputState.code)
        keyboard = None

    if (await db.is_linked(message.from_user.id)):
        text = f"Ознакомьтесь со списком и выберите кандидата"
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Выбрать кандидата", callback_data="list")]
        ])

    else:
        try:
            await db.link_tg2school(message.from_user.id, int(code))
            text = f"Ознакомьтесь со списком и выберите кандидата"
        
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="Выбрать кандидата", callback_data="list")]
            ])
        except SchoolUserNotFoundError:
            text = "Пользователь с таким кодом не найден, попробуйте проверить код или обратитесь к организаторам."
            keyboard = None
            await state.set_state(InputState.code)

        except SchoolUserAlreadyLinkedError:
            text = "Пользователь с таким кодом уже существует, попробуйте проверить код или обратитесь к организаторам."
            keyboard = None
            await state.set_state(InputState.code)

        except ValueError:
            text = "Проверьте правильность кода и отправьте его еще раз"
            keyboard = None
            await state.set_state(InputState.code)

    await bot.send_message(
        chat_id = message.chat.id,
        text = text,
        reply_markup = keyboard
    )


@router.message(StateFilter(InputState.code))
async def code_input(message: Message, state: FSMContext):
    await state.clear()
    bot = message.bot
    code = message.text.replace("/start", "")

    if code == "":
        text = f"Привет {message.from_user.full_name}, отправь свой код для голосований."
        await state.set_state(InputState.code)
        keyboard = None
    else:
        try:
            await db.link_tg2school(message.from_user.id, int(code))
            text = f"Ознакомьтесь со списком и выберите кандидата"
        
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="Выбрать кандидата", callback_data="list")]
            ])
        except SchoolUserNotFoundError:
            text = "Пользователь с таким кодом не найден, попробуйте проверить код или обратитесь к организаторам. Вы можете отправить код еще раз."
            keyboard = None
            await state.set_state(InputState.code)

        except SchoolUserAlreadyLinkedError:
            text = "Пользователь с таким кодом уже существует, попробуйте проверить код или обратитесь к организаторам. Вы можете отправить код еще раз."
            keyboard = None
            await state.set_state(InputState.code)
        
        except ValueError:
            text = "Проверьте правильность кода и отправьте его еще раз"
            keyboard = None
            await state.set_state(InputState.code)

    await bot.send_message(
        chat_id = message.chat.id,
        text = text,
        reply_markup = keyboard
    )