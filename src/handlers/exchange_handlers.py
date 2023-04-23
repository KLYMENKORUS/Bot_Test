import asyncio

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import bot
from service.exchange_api_service import APIExchange
from keyboards.keyboards import ReplyKeyboard


# создаем машину состояния
# для сохранение ответов пользователя
class FSMExchange(StatesGroup):
    convert_from = State()
    convert_to = State()
    amount = State()


class ExchangeHandler:

    # хендлер для команды "Конвертация валюты", а также
    # запуск FSM
    async def convert_currency_command(self, message: types.Message) -> None:
        await FSMExchange.convert_from.set()
        await bot.send_message(
            message.from_user.id,
            f'Ok, {message.from_user.first_name}.\n'
            'Введи валюту которую хочешь конвертировать, в формате (USD).',
            reply_markup=ReplyKeyboard.cancel_currency_convert(
                'Отменить конвертацию'
            )
        )

    # хендлер для отмены конвертации валюты
    async def cancel_convert_currency(self, message: types.Message,
                                      state: FSMContext) -> None:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await bot.send_message(
            message.from_user.id,
            'Ok, отменяю конвертацию валют.\n'
            f'{message.from_user.first_name} выбери тогда другую функцию!',
            reply_markup=ReplyKeyboard.main_keyboard(
                'Погода', 'Конвертация валюты',
                'Случайная картинка', 'Создать опрос'
            )
        )

    # хендлер для загрузки введенной им валюты
    # которую пользователь хочет сконвертировать
    async def load_current_from(self, message: types.Message,
                                state: FSMContext) -> None:
        async with state.proxy() as data:
            data['convert_from'] = message.text

        await FSMExchange.next()
        await bot.send_message(
            message.from_user.id,
            f'Ok, {message.from_user.first_name}.\n'
            'Теперь укажи валюту на которую хочешь сконвертировать результат.',
            reply_markup=ReplyKeyboard.cancel_currency_convert(
                'Отменить конвертацию'
            )
        )

    # хендлер для загрузки введенной им валюты
    # которую хочет получить пользователь в конечном итоге
    async def load_current_to(self, message: types.Message,
                              state: FSMContext) -> None:
        async with state.proxy() as data:
            data['convert_to'] = message.text

        await FSMExchange.next()
        await bot.send_message(
            message.from_user.id,
            f'Хорошо - теперь укажи сумму {data["convert_from"]},\n'
            'для точности укажи целым числом.',
            reply_markup=ReplyKeyboard.cancel_currency_convert(
                'Отменить конвертацию'
            )
        )

    # загрузка суммы которую пользователь хочет
    # с конвертировать, и результат конвертации
    async def load_amount(self, message: types.Message,
                          state: FSMContext) -> None:
        async with state.proxy() as data:
            data['amount'] = int(message.text)

        try:
            api_exchange = APIExchange(
                data['convert_to'], data['convert_from'],
                data['amount']
            )
            exchange = api_exchange.get_exchange()
            formatted_exchange = api_exchange.format_exchange(exchange)
            await message.answer('Минутку выполняю конвертацию...')
            await asyncio.sleep(3)
            await bot.send_message(
                message.from_user.id, formatted_exchange,
                reply_markup=ReplyKeyboard.main_keyboard(
                    'Погода', 'Конвертация валюты',
                    'Случайная картинка', 'Создать опрос'
                )
            )
        except:
            await bot.send_message(
                message.from_user.id,
                'Произошла ошибка при конвертации валют повторите еще раз.',
                reply_markup=ReplyKeyboard.main_keyboard(
                    'Погода', 'Конвертация валюты',
                    'Случайная картинка', 'Создать опрос'
                )
            )
        await state.finish()

    # регистрация хендлеров
    def register_handler(self, dp: Dispatcher):
        dp.register_message_handler(
            self.convert_currency_command, Text(equals='Конвертация валюты',
                                                ignore_case=True),
            state=None
        )
        dp.register_message_handler(
            self.cancel_convert_currency, Text(equals='Отменить конвертацию',
                                               ignore_case=True),
            state='*'
        )
        dp.register_message_handler(
            self.load_current_from, state=FSMExchange.convert_from
        )
        dp.register_message_handler(
            self.load_current_to, state=FSMExchange.convert_to
        )
        dp.register_message_handler(
            self.load_amount, state=FSMExchange.amount
        )