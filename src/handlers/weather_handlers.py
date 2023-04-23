from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import bot
from keyboards.keyboards import ReplyKeyboard
from service.weather_api_service import APIWeather


class FSMWeather(StatesGroup):
    city = State()


class WeatherHandler:

    # хендлер который ловит команду "Погода", и
    # активируем машину состояний для записи названия города
    async def weather_command(self, message: types.Message) -> None:
        await FSMWeather.city.set()
        await bot.send_message(
            message.from_user.id,
            f'Ok {message.from_user.first_name}, введи название города,\n'
            'на английском языке, для определение текущей погоды.',
            reply_markup=ReplyKeyboard.cancel('Отмена')
        )

    # отмена загрузки названия города
    async def cancel_load_name_city(self, message: types.Message,
                                    state: FSMContext) -> None:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await bot.send_message(
            message.from_user.id,
            'Ok, отменяю загрузку погоды.\n'
            f'{message.from_user.first_name} выбери тогда другую функцию!',
            reply_markup=ReplyKeyboard.main_keyboard(
                'Погода', 'Конвертация валюты',
                'Случайная картинка', 'Создать опрос'
            )
        )

    # ловим название города от пользователя и обращаемся к API для
    # получения погоды
    async def load_name_city(self, message: types.Message,
                             state: FSMContext) -> None:
        async with state.proxy() as data:
            data['city'] = message.text
        try:
            api_weather = APIWeather(data['city'])
            weather = api_weather.get_weather()
            formatted_weather = api_weather.format_weather(weather)
            await message.answer(formatted_weather,
                                 reply_markup=ReplyKeyboard.main_keyboard(
                                     'Погода', 'Конвертация валюты',
                                     'Случайная картинка', 'Создать опрос'
                                 ))
        except:
            await message.answer(
                'Извините, произошла ошибка при получении погоды для вашего города.',
                reply_markup=ReplyKeyboard.main_keyboard(
                    'Погода', 'Конвертация валюты',
                    'Случайная картинка', 'Создать опрос'
                )
            )
        await state.finish()

    # регистрация хендлеров
    def register_handler(self, dp: Dispatcher) -> None:
        dp.register_message_handler(
            self.weather_command, Text(equals='Погода', ignore_case=True),
            state=None
        )
        dp.register_message_handler(
            self.cancel_load_name_city,
            Text(equals='Отмена', ignore_case=True), state='*'
        )
        dp.register_message_handler(self.load_name_city, state=FSMWeather.city)

