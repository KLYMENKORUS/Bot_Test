from aiogram import types, Dispatcher
from config import bot
from keyboards.keyboards import ReplyKeyboard


class StartBot:

    async def start_command(self, message: types.Message) -> None:
        await bot.send_sticker(
            message.from_user.id,
            sticker='CAACAgIAAxkBAAEIpv5kQTlIwy54xdJpGh_x-2YewXKgewACAQEAAladvQoivp8OuMLmNC8E'
        )
        await bot.send_message(
            message.from_user.id,
            f'Привет {message.from_user.first_name}.\n'
            'Я бот у которого есть такие функции:\n'
            '\t-Определение текущей погоды по определенному городу;\n'
            '\t-Конвертация валют;\n'
            '\t-Отправка случайной картинки милых животных;\n'
            '\t-Создание опросов.', reply_markup=ReplyKeyboard.main_keyboard(
                'Погода', 'Конвертация валюты',
                'Случайная картинка', 'Создать опрос'
            )
        )

    def register_handler(self, dp: Dispatcher):
        dp.register_message_handler(self.start_command, commands=['start'])