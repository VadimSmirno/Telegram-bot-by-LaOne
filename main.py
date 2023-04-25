from aiogram import executor
from tg_bot import dp
from functions_bot import start, weather, exchange_rates, random_animals, poll

start.register_handlers_start(dp)
weather.register_handlers_weather(dp)
exchange_rates.register_handler_exchange_rates(dp)
exchange_rates.register_callback_query_handler(dp)
random_animals.register_handler_photo(dp)
poll.register_polls(dp)

if __name__ == '__main__':
    executor.start_polling(dp)
