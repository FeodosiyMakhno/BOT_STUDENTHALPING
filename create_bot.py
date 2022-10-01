from aiogram import Bot,types
from aiogram.dispatcher import Dispatcher
import config
from aiogram.contrib.fsm_storage.memory import MemoryStorage


bot = Bot(config.TOKEN,parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot,storage=MemoryStorage())