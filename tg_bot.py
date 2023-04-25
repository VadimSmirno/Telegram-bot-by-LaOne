from aiogram.dispatcher.filters.state import State, StatesGroup
import os
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv

load_dotenv() # Загрузка переменных окружения из .env файла
tg_bot_token = os.getenv('tg_bot_token')
bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot, storage=MemoryStorage())

class SearchCity(StatesGroup):
    # Создание StatesGroup с состоянием city для поиска города
    city = State()


