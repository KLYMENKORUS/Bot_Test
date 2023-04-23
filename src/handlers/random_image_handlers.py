import asyncio

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import bot
from service.random_image import GoogleRandomImage
from keyboards.keyboards import ReplyKeyboard


class FSMImage(StatesGroup):
    query = State()


class RandomImageHandler:

    async def cmd_random_image(self, message: types.Message) -> None:
        await FSMImage.query.set()
        await bot.send_message(
            message.from_user.id,
            f'Ok, {message.from_user.first_name}.\n'
            'Введи любую тему картинки которую ты хочешь получить,\n'
            'например "животные"',
            reply_markup=ReplyKeyboard.cancel_image(
                'Отменить загрузку картинки'
            )
        )

    async def cancel_query(self, message: types.Message,
                           state: FSMContext) -> None:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await bot.send_message(
            message.from_user.id,
            'Ok, отменяю загрузку картинки.\n'
            f'{message.from_user.first_name} выбери тогда другую функцию!',
            reply_markup=ReplyKeyboard.main_keyboard(
                'Погода', 'Конвертация валюты',
                'Случайная картинка', 'Создать опрос'
            )
        )

    async def load_query(self, message: types.Message,
                         state: FSMContext) -> None:
        async with state.proxy() as data:
            data['query'] = message.text

        try:
            query = GoogleRandomImage(data['query'])
            image_url = query.search()

            await message.answer(
                f'Минутку ищу картинку по запросу: {data["query"]}'
            )
            await asyncio.sleep(3)

            if image_url is not None:
                await bot.send_photo(
                    message.from_user.id, photo=image_url,
                    caption=f'Случайная картинка по твоему запросу: {data["query"]}',
                    reply_markup=ReplyKeyboard.main_keyboard(
                        'Погода', 'Конвертация валюты',
                        'Случайная картинка', 'Создать опрос'
                    )
                )
                await state.finish()
            else:
                await bot.send_message(
                    message.from_user.id,
                    f'По твоему запросу {data["query"]} ничего не нашел. Извини.\n'
                    'Попробуй еще раз!',
                    reply_markup=ReplyKeyboard.main_keyboard(
                        'Погода', 'Конвертация валюты',
                        'Случайная картинка', 'Создать опрос'
                    )
                )
        except:
            await message.answer(
                'Извини, произошла ошибка при поиске картинки попробуй еще раз!.',
                reply_markup=ReplyKeyboard.main_keyboard(
                    'Погода', 'Конвертация валюты',
                    'Случайная картинка', 'Создать опрос'
                )
            )
        await state.finish()

    def register_handler(self, dp: Dispatcher):
        dp.register_message_handler(
            self.cmd_random_image, Text(equals='Случайная картинка',
                                        ignore_case=True),
            state=None
        )
        dp.register_message_handler(
            self.cancel_query, Text(equals='Отменить загрузку картинки',
                                    ignore_case=True),
            state='*'
        )
        dp.register_message_handler(
            self.load_query, state=FSMImage.query
        )