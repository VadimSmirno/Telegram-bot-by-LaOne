import logging
from tg_bot import bot
import requests
from bs4 import BeautifulSoup
import random
from aiogram import types, Dispatcher


async def photo(message: types.Message):
    """
    Отправляет случайное фото животного из списка URL-адресов.
    :param message: telegram message object
    :type message: types.Message
    :return: None
    """
    try:
        # список URL-адресов страниц с изображениями животных
        urls = ['https://unsplash.com/s/photos/animals',
                'https://www.google.com/search?rlz=1C1GCEA_enRU1039RU1039&sxsrf=APwXEddKCQFFo2Lwu-DQeHMR853Vnb7M4Q:1682350252194&q=%D0%9A%D0%B0%D1%80%D1%82%D0%B8%D0%BD%D0%BA%D0%B8+%D0%B6%D0%B8%D0%B2%D0%BE%D1%82%D0%BD%D1%8B%D1%85&tbm=isch&source=univ&fir=NHILtzR2qNOiYM%252Ch7_Z5VGHlSmb9M%252C_%253BAeFEL_R80kZi9M%252CkzGubh9WUmdxbM%252C_%253BHX_n3bS7wcKO2M%252Cwc0LEAkKpE1mmM%252C_%253BLSFil4qQ0JMUtM%252Cewoz-i16Wh4-lM%252C_%253BmRlc67_IosbZ_M%252CwncdyLsLSosvPM%252C_%253BoCWqF4sQtSo1CM%252CWflJHZg57ghn1M%252C_%253Byke6UJ5fHr3x9M%252CKUsOvkVSZp4FOM%252C_%253BWj2rzhD6eKqYoM%252CFYVNMrrrim1pMM%252C_%253Bjd6mVvCeGo_AmM%252CBs3mTkCWNMqV3M%252C_%253BgIJZX5Tyi3bHWM%252COBVIfBMiSq8o5M%252C_%253B1p1ikSagZfT2WM%252C1gvVQsldZIyvmM%252C_%253B7eMpLgZXbiutsM%252C87ufcGT2ADUJCM%252C_&usg=AI4_-kRAgmtlK5IgZrYHAE7cZ2YQ7T2tMQ&sa=X&ved=2ahUKEwi1s62J68L-AhUOSvEDHVjdDdEQjJkEegQIFhAC&biw=1904&bih=952&dpr=1']

        # выбираем случайный URL из списка
        url = random.choice(urls)

        # загружаем страницу
        response = requests.get(url, timeout=15)

        # создаем объект BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # находим все элементы <img> на странице
        images = soup.find_all('img')

        # выбираем случайное изображение из списка
        image_url = random.choice(images)['src']

        # загружаем изображение
        response = requests.get(image_url)

        # сохраняем изображение в файл
        with open('random_animal_image.jpg', 'wb') as f:
            f.write(response.content)
        photo = types.InputFile('random_animal_image.jpg')
        await bot.send_photo(chat_id=message.chat.id, photo=photo)
    except Exception as err:
        logging.error(err)
        await message.reply('Упс')


def register_handler_photo(dp: Dispatcher):
    """
    Функция  регистрирует обработчик команды /animals
    :param dp: объект Dispatcher из библиотеки aiogram.
    :type dp: Dispatcher.
    :return: None
    """
    dp.register_message_handler(photo, commands=['animals'])
