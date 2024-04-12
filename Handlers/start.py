from aiogram import F,Router, types
from aiogram.filters import CommandStart ,StateFilter, or_f
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

from sqlalchemy.ext.asyncio import AsyncSession

from Auxiliary.states import Start
from Auxiliary.keybaords import startKB, agreeKB

from Assests import memorycode_API_requests

from Logging.LoggerConfig import logger

from requests import exceptions
# Start router
sr = Router()


@sr.message(CommandStart())
async def start(message: Message):
    await message.answer(text="Здравствуйте!\n\nЭто чат-бот от проекта <a href='https://memorycode.ru/'>memorycode.ru</a>\n\nЗдесь вы можете заполнить страницу памяти о человеке.", reply_markup=startKB.as_markup())

