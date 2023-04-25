import requests
import datetime
import logging
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from tg_bot import dp, SearchCity
import os

formater = '%(asctime)s [%(filename)s:  %(lineno)d] %(levelname)s %(message)s'
logging.basicConfig(level=logging.INFO, format=formater)

open_weather_token = os.environ.get("open_weather_token")


async def get_city(message: types.Message):
    """
        Обработчик команды /weather. Отправляет сообщение пользователю с просьбой ввести название города.
        :param message: Объект Message из aiogram, содержащий информацию о полученном сообщении.
        :type message: types.Message
        :return: None
    """
    await message.reply('напиши название города')
    await SearchCity.city.set()  # переход в машино-состояние город


async def get_weather(message: types.Message, state: FSMContext):
    """
        Обработчик для получения погоды в заданном городе. Получает название города от пользователя, делает запрос к API
        погоды и отправляет сообщение с информацией о погоде в заданном городе.
        :param message: Объект Message из aiogram, содержащий информацию о полученном сообщении.
        :type message: types.Message
        :param state: Объект FSMContext из aiogram, содержащий информацию о текущем состоянии бота.
        :type state: FSMContext
        :return: None
    """

    # Определение словаря для отображения значений состояния погоды в смайлы
    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Дождь \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B"
    }
    async  with state.proxy() as data:
        data['city'] = message.text

        try:
            r = requests.get(
                f"http://api.openweathermap.org/data/2.5/weather?q={data.get('city')}&appid={open_weather_token}&units=metric",
                timeout=10
            )
            data = r.json()
            # Извлечение информации о погоде из ответа API
            city = data["name"]
            cur_weather = data["main"]["temp"]

            weather_description = data["weather"][0]["main"]
            if weather_description in code_to_smile:
                wd = code_to_smile[weather_description]
            else:
                wd = "Посмотри в окно, не пойму что там за погода!"

            humidity = data["main"]["humidity"]
            pressure = data["main"]["pressure"]
            wind = data["wind"]["speed"]
            sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
            sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
            length_of_the_day = datetime.datetime.fromtimestamp(
                data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(
                data["sys"]["sunrise"])

            # Отправка сообщения с информацией о погоде
            await message.reply(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
                                f"Погода в городе: {city}\nТемпература: {cur_weather}C° {wd}\n"
                                f"Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст\nВетер: {wind} м/с\n"
                                f"Восход солнца: {sunrise_timestamp}\nЗакат солнца: {sunset_timestamp}\nПродолжительность дня: {length_of_the_day}\n"
                                f"Хорошего дня!"
                                )

        except Exception as ex:
            logging.error(ex)
            await message.reply("\U00002620 Проверьте название города \U00002620")
        await state.finish()


def register_handlers_weather(dp: Dispatcher):
    """
        Функция, которая регистрирует обработчики для получения погоды в определенном городе.
        Регистрирует обработчик для получения названия города и переводит машину-состояние в режим города.
        Регистрирует обработчик для получения погоды и передает в качестве аргумента машину-состояний.

        Parameters:
            dp (Dispatcher): диспетчер.

        Returns:
            None.
    """
    dp.register_message_handler(get_city, commands=['weather'])
    dp.register_message_handler(get_weather, state=SearchCity.city)
