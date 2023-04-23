from dataclasses import dataclass
from aiogram import types, Dispatcher
from aiogram.types import Poll
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import bot
from keyboards.keyboards import ReplyKeyboard


@dataclass(slots=True, frozen=True)
class Polls:
    question: str
    options: list
    correct_options_id: int


class FSMCreatePoll(StatesGroup):
    question = State()
    options = State()
    correct_options_id = State()


class PollHandler:

    async def start_create_poll_cmd(self, message: types.Message):
        await FSMCreatePoll.question.set()
        await bot.send_message(
            message.from_user.id,
            f'Ok, {message.from_user.first_name}.\n'
            'Укажи вопрос для создания опроса.',
            reply_markup=ReplyKeyboard.cancel_poll(
                'Отменить создание опроса'
            )
        )

    async def cancel_create_poll(self, message: types.Message,
                                 state: FSMContext) -> None:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await bot.send_message(
            message.from_user.id,
            'Ok, отменяю создание опроса.\n'
            f'{message.from_user.first_name} выбери тогда другую функцию!',
            reply_markup=ReplyKeyboard.main_keyboard(
                'Погода', 'Конвертация валюты',
                'Случайная картинка', 'Создать опрос'
            )
        )

    async def load_question_poll(self, message: types.Message,
                                 state: FSMContext) -> None:
        async with state.proxy() as data:
            data['question'] = message.text

        await FSMCreatePoll.next()
        await bot.send_message(
            message.from_user.id,
            f'Хорошо {message.from_user.first_name},\n'
            'теперь укажи варианты ответов через запятую.',
            reply_markup=ReplyKeyboard.cancel_poll('Отменить создание опроса')
        )

    async def load_options_poll(self, message: types.Message,
                                state: FSMContext) -> None:
        async with state.proxy() as data:
            data['options'] = message.text.strip().split(',')

        await FSMCreatePoll.next()
        await bot.send_message(
            message.from_user.id,
            f'Ok, {message.from_user.first_name},'
            'Теперь укажи правильный ответ цифрой начиная с 1',
            reply_markup=ReplyKeyboard.cancel_poll('Отменить создание опроса')
        )

    async def load_correct_answer(self, message: types.Message,
                                  state: FSMContext) -> None:
        async with state.proxy() as data:
            data['correct_options_id'] = int(message.text) - 1

        # создаем объект Polls
        poll = Polls(question=data['question'], options=data['options'],
                     correct_options_id=data['correct_options_id'])

        # создаем объект типа Poll
        telegram_poll = Poll(
            question=poll.question,
            options=poll.options,
            is_anonymous=True,
            correct_option_id=poll.correct_options_id
        )
        await bot.send_poll(
            chat_id=message.chat.id,
            question=telegram_poll.question,
            options=telegram_poll.options,
            is_anonymous=telegram_poll.is_anonymous,
            type='quiz',
            correct_option_id=telegram_poll.correct_option_id,
            reply_markup=ReplyKeyboard.main_keyboard(
                'Погода', 'Конвертация валюты',
                'Случайная картинка', 'Создать опрос'
            )
        )
        await state.finish()

    def register_handler(self, dp: Dispatcher):
        dp.register_message_handler(
            self.start_create_poll_cmd,
            Text(equals='Создать опрос', ignore_case=True),
            state=None
        )
        dp.register_message_handler(
            self.cancel_create_poll,
            Text(equals='Отменить создание опроса', ignore_case=True),
            state='*'
        )
        dp.register_message_handler(
            self.load_question_poll, state=FSMCreatePoll.question
        )
        dp.register_message_handler(
            self.load_options_poll,
            state=FSMCreatePoll.options
        )
        dp.register_message_handler(
            self.load_correct_answer, state=FSMCreatePoll.correct_options_id
        )
