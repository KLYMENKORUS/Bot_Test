from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


class ReplyKeyboard:
    """Класс представляющий текствую клавиатуру"""

    @staticmethod
    def main_keyboard(*args: str) -> ReplyKeyboardMarkup:
        kb = ReplyKeyboardMarkup(resize_keyboard=True)
        weather_kb = KeyboardButton(args[0])
        currency_convert = KeyboardButton(args[1])
        random_image = KeyboardButton(args[2])
        polls_kb = KeyboardButton(args[3])
        kb.add(weather_kb, currency_convert).add(random_image, polls_kb)
        return kb

    @staticmethod
    def cancel(*args: str) -> ReplyKeyboardMarkup:
        kb_cancel = ReplyKeyboardMarkup(resize_keyboard=True)
        cancel = KeyboardButton(args[0])
        kb_cancel.add(cancel)
        return kb_cancel

    @staticmethod
    def cancel_currency_convert(*args: str) -> ReplyKeyboardMarkup:
        kb_cancel_exchange = ReplyKeyboardMarkup(resize_keyboard=True)
        cancel_exchange = KeyboardButton(args[0])
        kb_cancel_exchange.add(cancel_exchange)
        return kb_cancel_exchange

    @staticmethod
    def cancel_image(*args: str) -> ReplyKeyboardMarkup:
        cancel_image_kb = ReplyKeyboardMarkup(resize_keyboard=True)
        cancel_image = KeyboardButton(args[0])
        cancel_image_kb.add(cancel_image)
        return cancel_image_kb

    @staticmethod
    def cancel_poll(*args: str) -> ReplyKeyboardMarkup:
        cancel_poll_kb = ReplyKeyboardMarkup(resize_keyboard=True)
        cancel_poll = KeyboardButton(args[0])
        cancel_poll_kb.add(cancel_poll)
        return cancel_poll_kb
