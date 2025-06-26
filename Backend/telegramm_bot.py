import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from db_utils import add_user, get_user, award_referral_bonus

TOKEN = '7636282193:AAHHIcQdFrM5ZV2_ObyjjjvUwCqr6FFjL2U'  # замените на ваш токен
apiserv = "https://4e27-57-129-20-194.ngrok-free.app"  # сюда подставьте адрес после запуска ngrok, например https://1234abcd.ngrok-free.app
your_channel = "https://t.me/your_channel"

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username or message.from_user.first_name or "User"
    args = message.text.split()[1:] if len(message.text.split()) > 1 else []
    web_app_url = f"{apiserv}/?user_id={user_id}&username={username}"

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Играть в 1 клик 🎮', web_app=WebAppInfo(url=web_app_url))],
        [InlineKeyboardButton(text='Подписаться на канал 📢', url=your_channel)],
        [InlineKeyboardButton(text='Как заработать на игре 💰', callback_data='how_to_earn')]
    ])

    referrer_id = None
    if args and args[0].startswith('referrer_'):
        referrer_id = args[0].split('_')[1]

    existing_user = get_user(user_id)
    if existing_user:
        await message.answer(
            "Привет! Добро пожаловать в MMM Coin 🎮!\n"
            "Отныне ты — директор. Тапай по экрану, собирай монеты, качай пассивный доход, разрабатывай стратегию.\n"
            "Зови друзей — вместе бонусы больше!",
            reply_markup=keyboard
        )
        return

    new_user = add_user(user_id, username, referrer_id=referrer_id)
    if referrer_id:
        premium_status = False  # если нужно — реализуйте premium check
        award_referral_bonus(user_id, referrer_id, premium_status)

    await message.answer(
        "Привет! Добро пожаловать в MMM Coin 🎮!\n"
        "Отныне ты — директор. Тапай по экрану, собирай монеты, качай пассивный доход, разрабатывай стратегию.\n"
        "Зови друзей — вместе бонусы больше!",
        reply_markup=keyboard
    )

@dp.callback_query(lambda q: q.data == 'how_to_earn')
async def button_handler(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    username = callback_query.from_user.username or callback_query.from_user.first_name or "User"
    web_app_url = f"{apiserv}/?user_id={user_id}&username={username}"
    keyboards = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Играть в 1 клик 🎮', web_app=WebAppInfo(url=web_app_url))],
        [InlineKeyboardButton(text='Подписаться на канал 📢', url=your_channel)]
    ])
    await callback_query.message.answer(
        "Как играть в MMMCoin?\n"
        "💰 Tap to earn — Тапай по экрану и собирай монеты.\n"
        "⛏ Mine — Прокачивай карточки для пассивного дохода.\n"
        "⏰ Прибыль в час — работает даже если ты оффлайн.\n"
        "📈 LVL — Чем выше уровень, тем быстрее заработок.\n"
        "👥 Friends — зови друзей и получайте бонусы вместе.",
        reply_markup=keyboards
    )
    await callback_query.answer()

if __name__ == '__main__':
    print("Бот запущен. Для остановки нажмите Ctrl+C")
    asyncio.run(dp.start_polling(bot))