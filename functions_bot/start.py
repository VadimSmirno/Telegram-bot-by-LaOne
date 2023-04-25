from aiogram import types
from aiogram import Dispatcher

start_message = f'Привет! Хочешь узнать погоду в своем городе? /weather \n' \
                f'Хочешь конвертировать валюты /exchange_rates\n' \
                f'Хочешь посмотреть картинку милого животного? /animals \n' \
                f'Хочешь создать опрос /poll'


async def start_command(message: types.Message):
    """
       Обработчик команд /start и /help. Отправляет сообщение start_message при получении этих команд.
       :param message: Объект Message из aiogram, содержащий информацию о полученном сообщении.
       :type message: types.Message
       :return: None
    """
    await message.reply(start_message)


def register_handlers_start(dp: Dispatcher):
    """
        Регистрирует обработчик команд /start и /help.
        :param dp: Объект Dispatcher из aiogram.
        :type dp: Dispatcher
        :return: None
    """
    dp.register_message_handler(start_command, commands=['start', 'help'])
