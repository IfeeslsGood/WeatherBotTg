import datetime
import requests
from config import token
from config import bot_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

bot = Bot(token=bot_token)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def hi(message: types.Message):
    await message.reply("Привет! Укажи город")


@dp.message_handler()
async def get_weather(message: types.Message):
    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Дождь \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B"
    }

    try:
        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={token}&units=metric"
        )
        data = r.json()

        city = data["name"]
        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "Посмотри в окно"
        temp = data["main"]["temp"]
        temp_min = data["main"]["temp_min"]
        temp_max = data["main"]["temp_max"]
        wind_speed = data["wind"]["speed"]
        sunrise_datatime = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        await message.answer(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
                             f"Город: {city}\n"
                             f"Температура сейчас: {temp}C° {wd}\n"
                             f"Максимальная температура: {temp_max}C°\n"
                             f"Минимальная температура: {temp_min}C°\n"
                             f"Скорость ветра: {wind_speed} м/c\n"
                             f"Рассвет солнца {sunrise_datatime}\n"
                             f"Закат солнца {sunset_timestamp}\n")

    except:
        await message.reply("Check city name!")


if __name__ == '__main__':
    executor.start_polling(dp)
