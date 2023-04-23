import json
import urllib.request
from json import JSONDecodeError
from typing import Literal
from urllib.error import URLError
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
from config import open_weather_token, get_weather_url


class ApiServiceError(Exception):
    pass


Celsius = float


class WeatherType(str, Enum):
    THUNDERSTORM = "Гроза \U0001F329"
    DRIZZLE = "Изморось \U0001F327"
    RAIN = "Дождь \U0001F327"
    SNOW = "Снег \U0001F328"
    CLEAR = "Ясно \U00002600"
    FOG = "Туман \U0001F32B"
    CLOUDS = "Облачно \U00002601"


@dataclass(slots=True, frozen=True)
class Weather:
    temperature: Celsius
    weather_type: WeatherType
    sunrise: datetime
    sunset: datetime
    length_of_the_day: timedelta
    city: str


class APIWeather:
    """
    Реализация получения данных о погоде через API OpenWeather
    """
    def __init__(self, city: str):
        self.city = city

    def get_weather(self) -> Weather:
        """Ответ от API OpenWeather"""
        open_weather_response = self._get_openweather_response(self.city)
        weather = self._parse_openweather_response(open_weather_response)
        return weather

    def _get_openweather_response(self, city: str) -> str:
        """Запрос к API по городу и передача
        ответа в метод _parse_openweather_response
        """
        url = get_weather_url.format(city, open_weather_token)
        try:
            return urllib.request.urlopen(url).read()
        except URLError:
            raise ApiServiceError

    def _parse_openweather_response(self, response: str) -> Weather:
        """Парсинг ответа от API и преобразование в JSON"""
        try:
            open_weather_dict = json.loads(response)
        except JSONDecodeError:
            raise ApiServiceError
        return Weather(
            temperature=self._parse_temperature(open_weather_dict),
            weather_type=self._parse_weather_type(open_weather_dict),
            sunrise=self._parse_sun_time(open_weather_dict, 'sunrise'),
            sunset=self._parse_sun_time(open_weather_dict, 'sunset'),
            length_of_the_day=self._parse_length_of_the_day(open_weather_dict),
            city=self._parse_city(open_weather_dict)
        )

    def _parse_temperature(self, open_weather_dict: dict) -> Celsius:
        """Парсинг температуры"""
        return round(open_weather_dict['main']['temp'])

    def _parse_weather_type(self, open_weather_dict: dict) -> WeatherType:
        """Парсинг типа погоды"""
        try:
            weather_type_id = str(open_weather_dict['weather'][0]['id'])
        except (IndexError, KeyError):
            raise ApiServiceError

        weather_types = {
            '1': WeatherType.THUNDERSTORM,
            '3': WeatherType.DRIZZLE,
            '5': WeatherType.RAIN,
            '6': WeatherType.SNOW,
            '7': WeatherType.FOG,
            '800': WeatherType.CLEAR,
            '80': WeatherType.CLOUDS
        }
        for _id, _weather_type in weather_types.items():
            if weather_type_id.startswith(_id):
                return _weather_type
        raise ApiServiceError

    def _parse_sun_time(
            self, open_weather_dict: dict,
            time: Literal['sunrise'] | Literal['sunset']) -> datetime:
        """Парсинг времени заката и восхода"""
        return datetime.fromtimestamp(open_weather_dict['sys'][time])

    def _parse_length_of_the_day(self, open_weather_dict: dict) -> timedelta:
        """Вычисление продолжительности дня"""
        return self._parse_sun_time(open_weather_dict, 'sunset') -\
               self._parse_sun_time(open_weather_dict, 'sunrise')

    def _parse_city(self, open_weather_dict: dict) -> str:
        return open_weather_dict['name']

    def format_weather(self, weather: Weather) -> str:
        """Вывод отформатированных данных о погоде"""
        return (
            f'\U000026C5 Погода в городе {weather.city}:\n'
            f'\U0001F321 Tемпература {weather.temperature}°C, '
            f'{weather.weather_type}\n'
            f'\U0001F305 Восход: {weather.sunrise.strftime("%H:%M")}\n'
            f'\U0001F307 Закат: {weather.sunset.strftime("%H:%M")}\n'
            '\U0001F567 Продолжительность дня: '
            f'{weather.length_of_the_day}')

