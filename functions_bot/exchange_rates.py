import requests
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import logging
from aiogram import types, Dispatcher
from aiogram.types import CallbackQuery
import os

formater = '%(asctime)s [%(filename)s:  %(lineno)d] %(levelname)s %(message)s'
logging.basicConfig(level=logging.INFO, format=formater)

exchange_rates_key = os.environ.get("Exchange_Rates_API")


async def exchange_rate_keyboard(message: types.Message):
    """
        Отправляет сообщение с клавиатурой для конвертации валют.
        :param message: сообщение, которое вызвало функцию
        :type message: types.Message
        :return: None
    """
    button1 = InlineKeyboardButton('USD/EUR', callback_data='USD/EUR')
    button2 = InlineKeyboardButton('USD/GBP', callback_data='USD/GBP')
    button3 = InlineKeyboardButton('RUB/USD', callback_data='RUB/USD')
    button4 = InlineKeyboardButton('RUB/EUR', callback_data='RUB/EUR')
    markup = InlineKeyboardMarkup().add(button1, button2).row(button3, button4)
    await message.answer('Конвертация', reply_markup=markup)


async def exchange_rate_callback_query(callback_query: CallbackQuery):
    """
        Обрабатывает callback_query при выборе пользователем валют для конвертации.
        Получает от API курс выбранных валют и отправляет сообщение с результатом.
        :param callback_query: callback_query, которое вызвало функцию
        :type callback_query: types.CallbackQuery
        :return: None
    """
    # Отвечаем пользователю на callback_query.
    await callback_query.answer(callback_query.data)
    # Убираем клавиатуру из сообщения, чтобы пользователь не мог отправить новое сообщение со старой клавиатурой.
    await callback_query.message.edit_reply_markup(reply_markup=None)
    # Получаем коды двух валют из callback_query.data
    currency1 = callback_query.data.split('/')[0]
    currency2 = callback_query.data.split('/')[1]
    try:
        url = f"https://api.apilayer.com/exchangerates_data/convert?to={currency1}&from={currency2}&amount=1"

        payload = {}
        headers = {
            "apikey": exchange_rates_key
        }
        # Делаем GET запрос на API.
        response = requests.request("GET", url, headers=headers, data=payload, timeout=15)
        result = response.json()['info']['rate'] # Получаем курс валюты
        date = response.json()['date']  # Получаем дату, на которую был произведен запрос.
        await callback_query.message.reply(f'На сегодня {date} \n'
                                           f'Курс {currency1} по отношению к {currency2} составляет {result}\n')
    except (KeyError, TimeoutError) as err:
        logging.error(err)
        await callback_query.message.answer('Упс')


def register_handler_exchange_rates(dp: Dispatcher):
    """
        Регистрирует обработчик команды /exchange_rates, который вызывает функцию exchange_rate_keyboard.
        :param dp: диспетчер бота
        :type dp: Dispatcher
        :return: None
    """
    dp.register_message_handler(exchange_rate_keyboard, commands=['exchange_rates'])


def register_callback_query_handler(dp: Dispatcher):
    """
       Регистрирует обработчик callback_query, вызываемый при нажатии на кнопки клавиатуры exchange_rate_keyboard.
       :param dp: диспетчер бота
       :type dp: Dispatcher
       :return: None
    """
    dp.register_callback_query_handler(exchange_rate_callback_query,
                                       lambda c: c.data in ['USD/EUR', 'USD/GBP', 'RUB/USD', 'RUB/EUR'])
