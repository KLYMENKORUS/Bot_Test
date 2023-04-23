import requests
from dataclasses import dataclass
from json import JSONDecodeError
from urllib.error import URLError
from requests import Response
from config import EXCHANGE_TOKEN, get_exchange_url

HEADERS = {
    'apikey': EXCHANGE_TOKEN
}


class ApiServiceError(Exception):
    pass


@dataclass(slots=True, frozen=True)
class Exchange:
    convert_to: str
    convert_from: str
    amount: int
    result: str


class APIExchange:
    """Реализация получения данных для конвертации валют"""

    def __init__(self, convert_to: str, convert_from: str, amount: int):
        self.convert_to = convert_to
        self.convert_from = convert_from
        self.amount = amount

    def get_exchange(self) -> Exchange:
        """Ответ от API"""
        exchange_response = self._get_exchange_request(
            self.convert_to, self.convert_from,
            self.amount
        )
        exchange = self._exchange_response(exchange_response)
        return exchange

    def _get_exchange_request(
            self, convert_to: str, convert_from: str, amount: int
    ) -> Response:
        """Запрос к API"""
        url = get_exchange_url.format(convert_to,
                                      convert_from,
                                      amount)
        try:
            return requests.get(url, headers=HEADERS)
        except URLError:
            raise ApiServiceError

    def _exchange_response(self, response: Response):
        """Парсинг ответа от API и преобразование в JSON"""
        try:
            exchange_response_dict = response.json()
        except JSONDecodeError:
            raise ApiServiceError
        return Exchange(
            convert_to=self._parse_convert_to(exchange_response_dict),
            convert_from=self._parse_convert_from(exchange_response_dict),
            amount=self._parse_amount(exchange_response_dict),
            result=self._parse_result(exchange_response_dict)
        )

    def _parse_convert_to(self, exchange_response_dict: dict) -> str:
        """Парсинг валюты которую пользователь хочет получить в итоге"""
        try:
            return exchange_response_dict['query']['to']
        except (IndexError, KeyError):
            raise ApiServiceError

    def _parse_convert_from(self, exchange_response_dict: dict) -> str:
        """Получение валюты которую хочет пользователь сконвертировать"""
        try:
            return exchange_response_dict['query']['from']
        except (IndexError, KeyError):
            raise ApiServiceError

    def _parse_amount(self, exchange_response_dict: dict) -> int:
        """Получение суммы конвертации"""
        try:
            return exchange_response_dict['query']['amount']
        except (IndexError, KeyError):
            raise ApiServiceError

    def _parse_result(self, exchange_response_dict: dict) -> str:
        """Получение сконвертированого результата"""
        try:
            return f"{exchange_response_dict['result']:.2f}"
        except (IndexError, KeyError):
            raise ApiServiceError

    def format_exchange(self, exchange: Exchange) -> str:
        """Вывод отформатированных данных"""
        return (
            f'Входная валюта: {exchange.convert_from}\n'
            f'Выходная валюта: {exchange.convert_to}\n'
            f'Введенная сумма: {exchange.amount}\n'
            f'Итог конвертации: {exchange.result}'
        )

