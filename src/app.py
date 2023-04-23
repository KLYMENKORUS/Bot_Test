from aiogram import executor, Bot, Dispatcher
from config import bot, dp, storage
from handlers.start import StartBot
from handlers.weather_handlers import WeatherHandler
from handlers.exchange_handlers import ExchangeHandler
from handlers.random_image_handlers import RandomImageHandler
from handlers.polls_handler import PollHandler


class CreateBot:

    def __init__(self, bot: Bot, dp: Dispatcher, storage):
        self.bot = bot
        self.dp = dp
        self.storage = storage

    async def on_startup(self, _):
        print('Бот в работе')

    def start(self):
        # регистрация хендлеров для команды start
        start = StartBot()
        start.register_handler(self.dp)

        # регистрация хендлеров для API OpenWeather
        weather = WeatherHandler()
        weather.register_handler(self.dp)

        # регистрация хендлеров для API Exchange
        exchange = ExchangeHandler()
        exchange.register_handler(self.dp)

        # регистрация хендлеров для поиска рандомной картинки
        random_search = RandomImageHandler()
        random_search.register_handler(self.dp)

        # регистрация хендлеров для создания опросов
        polls = PollHandler()
        polls.register_handler(self.dp)

        executor.start_polling(
            dispatcher=self.dp, on_startup=self.on_startup,
            skip_updates=True
        )


if __name__ == '__main__':
    bot = CreateBot(bot, dp, storage)
    bot.start()