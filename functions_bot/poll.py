from aiogram.types import Poll, PollOption, PollAnswer
from aiogram import types, Dispatcher
from tg_bot import bot
from aiogram.dispatcher.filters import filters


async def polls(messages: types.Message):
    """
       Отправляет опрос с вопросом о любимом цвете и вариантами ответов (Red, Blue, Green, Yellow).
       :param message: Объект сообщения Telegram.
       :return: None
    """
    poll = Poll(
        question='Ваш любимый цвет?',
        options=[
            PollOption(text='Red'),
            PollOption(text='Blue'),
            PollOption(text='Green'),
            PollOption(text='Yellow'),
        ],
        type='regular',  # опрос с одним ответом
        is_anonymous=True,
        allows_multiple_answers=False,
    )

    # отправка опроса
    await bot.send_poll(chat_id=messages.chat.id, question=poll.question, options=[o.text for o in poll.options],
                        type=poll.type, is_anonymous=poll.is_anonymous,
                        allows_multiple_answers=poll.allows_multiple_answers)


def register_polls(dp: Dispatcher):
    """
        Функция регистрирует обработчик сообщений для команды /poll.
        :param dp: Диспетчер бота.
        :type dp: :class:`telegram.ext.Dispatcher`
    """
    dp.register_message_handler(polls, commands=['poll'])

