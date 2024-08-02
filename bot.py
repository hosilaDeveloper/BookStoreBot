import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils import executor
import requests

API_TOKEN = '7282232490:AAEjq4oUSjwvigtXjhgKAr3hUrVMuNvi7k0'
API_BASE_URL = 'http://127.0.0.1:8000/api'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

main_menu_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
main_menu_keyboard.add(types.KeyboardButton("Address"), types.KeyboardButton("Books"))


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply('Assalomu-alaykum, Hush kelibsiz. Kerakli tugmani tanlang', reply_markup=main_menu_keyboard)


@dp.message_handler(text='Address')
async def address(message: types.Message):
    await message.reply('Mirzo Ulug\'bek Ko\'chasi 54A uy')


@dp.message_handler(text='Books')
async def books(message: types.Message):
    response = requests.get(API_BASE_URL + '/book/')
    if response.status_code == 200:
        books = response.json()
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        for book in books:
            keyboard.add(InlineKeyboardButton(book['title'], callback_data=f"book_{book['id']}"))
        await message.answer('Kerakli Kitobni tanlang', reply_markup=keyboard)

    else:
        await message.answer('Uzr Xatolik yuz berdi')


@dp.callback_query_handler(lambda query: query.data.startswith('book_'))
async def callback(query: types.CallbackQuery):
    await query.answer('Assalomu alikkum')
    try:
        book_id = query.data.split('_')[1]
        response = requests.get(f"{API_BASE_URL}/book/{book_id}/")
        if response.status_code == 200:
            book = response.json()
            book_info = (
                f"Title: {book['title']}\n"
                f"Author: {book['author']}\n"
                f"Price: ${book['price']}\n"
                f"Description: {book['description']}"
            )
            keyboard = InlineKeyboardMarkup()
            keyboard.add(InlineKeyboardButton(text="Order", callback_data=f"order_{book_id}"))
            keyboard.add(InlineKeyboardButton(text="Back", callback_data="back_to_books"))
            await query.message.answer(book_info, reply_markup=keyboard)
        else:
            await query.answer('Uzr Xatolik yuz berdi')
    except Exception as e:
        logging.error(f"Error in book_details handler: {e}")
        await bot.send_message(chat_id=query.from_user.id, text="An error occurred. Please try again later.")


@dp.callback_query_handler(lambda c: c.data == 'back_to_books')
async def back_to_books(callback_query: types.CallbackQuery):
    await books(callback_query.message)


@dp.callback_query_handler(lambda c: c.data.startswith('order_'))
async def order_book(callback_query: types.CallbackQuery):
    book_id = callback_query.data.split('_')[1]
    await bot.send_message(chat_id=callback_query.from_user.id,
                           text="Please provide your name and phone number in the format:\nName\nPhone Number")

    @dp.message_handler()
    async def receive_order(message: types.Message):
        data = message.text.split('\n')
        if len(data) == 2:
            name, phone = data
            await message.answer(f"Thank you for your order, {name}! We will contact you at {phone}.")
        else:
            await message.answer("Please provide the information in the correct format.")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
