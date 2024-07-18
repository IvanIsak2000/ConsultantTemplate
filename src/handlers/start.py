import asyncio
import aiogram
from secrets import choice
from aiogram import Router, F
from aiogram import types
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types
from aiogram.types import URLInputFile
from utils.other.emoji import send_emoji
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import URLInputFile
from aiogram.fsm.state import StatesGroup, State


from kb.inline import *
from utils.db.models import *
from utils.db.user import *
from filters.status import * 

router = Router()


@router.message(Command('start'))
async def start(message: types.Message, state: FSMContext):
    await message.answer('Hello!')
 