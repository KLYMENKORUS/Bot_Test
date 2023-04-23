import os

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

load_dotenv()

# Настройки OpenWeather
open_weather_token = os.getenv('open_weather_token')
get_weather_url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}&units=metric'

# Настройки Exchange Rates API
EXCHANGE_TOKEN = os.getenv('EXCHANGE_TOKEN')
get_exchange_url = 'https://api.apilayer.com/exchangerates_data/convert?to={}&from={}&amount={}'

# Настройки бота
TOKEN_BOT = os.getenv('TOKEN_BOT')
storage = MemoryStorage()
bot = Bot(TOKEN_BOT)
dp = Dispatcher(bot, storage=storage)
