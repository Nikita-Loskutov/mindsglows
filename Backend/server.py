from flask import Flask, render_template, send_from_directory, request, jsonify, redirect
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo, ChatMember
from aiogram.filters import Command
from aiogram import F
from threading import Thread
from db_utils import add_user, get_user, update_user_coins, update_invited_friends, award_referral_bonus, daily_reward_amount, accrue_profit_per_hour
from db_utils import get_card_data, update_card_level, session, User
import datetime


TOKEN = '7636282193:AAHHIcQdFrM5ZV2_ObyjjjvUwCqr6FFjL2U' #Ваш токен бота
apiserv = "https://9fb2-57-129-38-235.ngrok-free.app"  #ссылка вашего сервера
your_channel = "https://t.me/your_channel" #ваш тг канал


bot = Bot(token=TOKEN)
dp = Dispatcher()


app = Flask(__name__, static_folder='../src', template_folder='../src')


#Роуты Flask



@dp.message(Command("start"))
async def start(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username or message.from_user.first_name or "User"

    args = message.text.split()[1:] if len(message.text.split()) > 1 else []
    web_app_url = f"{apiserv}/user/{username}?user_id={user_id}"

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Играть в 1 клик 🎮', web_app=WebAppInfo(url=web_app_url))],
        [InlineKeyboardButton(text='Подписаться на канал 📢', url=f'{your_channel}')],
        [InlineKeyboardButton(text='Как заработать на игре 💰', callback_data='how_to_earn')]
    ])

    referrer_id = None
    if args and args[0].startswith('referrer_'):
        referrer_id = args[0].split('_')[1]

    existing_user = get_user(user_id)
    if existing_user:
        await message.answer(
            "Привет! Добро пожаловать в MMM Coin 🎮!\n"
            "Отныне ты — директор. Тапай по экрану, собирай монеты, качай пассивный доход,"
            " разрабатывай собственную стратегию дохода."
            "\nПро друзей не забывай — зови их в игру и получайте вместе ещё больше монет!",
            reply_markup=keyboard
        )
        return

    new_user = add_user(user_id, username, referrer_id=referrer_id)

    if referrer_id:
        premium_status = await check_premium_status(user_id)
        award_referral_bonus(user_id, referrer_id, premium_status)

    await message.answer(
        "Привет! Добро пожаловать в MMM Coin 🎮!\n"
        "Отныне ты — директор. Тапай по экрану, собирай монеты, качай пассивный доход,"
        " разрабатывай собственную стратегию дохода."
        "\nПро друзей не забывай — зови их в игру и получайте вместе ещё больше монет!",
        reply_markup=keyboard
    )



@dp.callback_query(F.data.in_({'how_to_earn'}))
async def button_handler(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    username = callback_query.from_user.username or callback_query.from_user.first_name or "User"

    web_app_url = f"{apiserv}/user/{username}?user_id={user_id}"
    keyboards = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Играть в 1 клик 🎮', web_app=WebAppInfo(url=web_app_url))],
        [InlineKeyboardButton(text='Подписаться на канал 📢', url=f'{your_channel}')]
    ])

    await callback_query.message.answer(
        "Как играть в MMMCoin?\n"
        "💰Tap to earn\nТапай по экрану и собирай монеты.\n"
        "\n⛏Mine\nПрокачивай карточки, которые дадут возможность пассивного дохода.\n"
        "\n⏰ Прибыль в час\nБиржа будет работать для тебя самостоятельно, даже когда ты не в игре в течение"
        " 3х часов. Далее нужно будет перезайти в игру снова.\n"
        "\n📈 LVL\nЧем больше монет у тебя на балансе — тем выше уровень биржи."
        " Чем выше уровень — тем быстрее сможешь зарабатывать ещё больше монет.\n"
        "\n👥 Friends\nПриглашай своих друзей, и вы получите бонусы. Помоги другу перейти в следующие лиги,"
        " и вы получите ещё больше бонусов.",
        reply_markup=keyboards
    )

    await callback_query.answer()


#Запуск Tг бота
async def telegram_main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


#Запуск Flask
def run_flask():
    app.run(host='0.0.0.0', port=5000, use_reloader=False)


if __name__ == '__main__':
    # Flask  в отдельном потоке
    flask_thread = Thread(target=run_flask)
    flask_thread.start()

    # Telegram запускается в основном потоке
    asyncio.run(telegram_main())
