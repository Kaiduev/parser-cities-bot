import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import CallbackQuery
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from config import TOKEN
from db import Database
from parser import parse_cities

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer("Hi!\nI'm ParserBot!.")


@dp.message_handler(commands=['help'])
async def help(message: types.Message):
    await message.answer("/parse")


@dp.message_handler(commands=['parse'])
async def parse(message: types.Message):
    await message.answer("parsing...")
    cities = parse_cities()
    conn = Database(db_name='cities_data', db_user='bot', db_password='password', db_host='128.199.68.239')
    conn.insert_data(cities)
    conn.connection_close()
    await message.answer("done")

callBackQueryList = list()


@dp.message_handler()
async def search(message: types.Message):
    conn = Database(db_name='cities_data', db_user='bot', db_password='password', db_host='128.199.68.239')
    result = conn.search_city(
        city_name=message.text
    )
    global result_all
    result_all = result
    if len(result) == 0:
        await message.answer("Городов с таким названием не найдено!")
    else:
        buttons = list()
        for city in result:
            button = InlineKeyboardButton(text=city[0], callback_data=str(city[0]))
            buttons.append(button)
        reply_inline = InlineKeyboardMarkup().add(*buttons)
        conn.connection_close()
        await message.answer("Найдено в базе:", reply_markup=reply_inline)


@dp.callback_query_handler()
async def call_people_quantity(call: CallbackQuery):
    found = False
    for city in result_all:
        if city[0] == call.data:
            found = True
            await call.message.answer("Численность: " + city[4] + "\n\nСсылка: " + city[3])
    if not found:
        await call.message.answer("Выбирать можно только из последнего списка!")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
