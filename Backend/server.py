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


TOKEN = '7930529716:AAF5TYEKKTsG_jUD3k0gtzIa3YvAfikUIdk' #Ваш токен бота
apiserv = "https://e0a0-57-129-20-199.ngrok-free.app"  #ссылка вашего сервера
your_channel = "https://t.me/your_channel" #ваш тг канал


bot = Bot(token=TOKEN)
dp = Dispatcher()


app = Flask(__name__, static_folder='../src', template_folder='../src')


#Роуты Flask
@app.route('/')
def index():
    user_id = request.args.get('user_id', 0)
    username = request.args.get('username', 'Guest')
    user = get_user(user_id)

    if user:
        level_thresholds = [
            0,  # Уровень 1
            5000,  # Уровень 2
            25000,  # Уровень 3
            100000,  # Уровень 4
            1000000,  # Уровень 5
            2000000,  # Уровень 6
            10000000,  # Уровень 7
            50000000,  # Уровень 8
            1000000000,  # Уровень 9
            10000000000  # Уровень 10
        ]

        current_level = user.level
        if current_level < len(level_thresholds):
            next_level_coins = level_thresholds[current_level] - level_thresholds[current_level - 1]
        else:
            next_level_coins = "Max level"

        return render_template(
            'index.html',
            user_id=user.user_id,
            username=user.username,
            coins=user.coins,
            profit_per_tap=user.profit_per_tap,
            profit_per_hour=user.profit_per_hour,
            level=user.level,
            next_level_coins=next_level_coins
        )
    else:
        return render_template(
            'index.html',
            user_id=user_id,
            username=username,
            coins=0,
            profit_per_tap=1,
            profit_per_hour=0,
            level=1,
            next_level_coins=5000
        )

@app.route('/mine')
def mine():
    user_id = request.args.get('user_id', 1)
    user = session.query(User).filter_by(user_id=user_id).first()
    card_data_token = get_card_data(user, 'token')
    card_data_staking = get_card_data(user, 'staking')
    card_data_genesis = get_card_data(user, 'genesis')
    card_data_echeleon = get_card_data(user, 'echeleon')
    card_data_ledger = get_card_data(user, 'ledger')
    card_data_quantum = get_card_data(user, 'quantum')
    card_data_multitap = get_card_data(user, 'multitap')
    return render_template('mine.html', user_id=user_id, card_data_token=card_data_token, card_data_staking=card_data_staking, card_data_genesis=card_data_genesis, card_data_echeleon=card_data_echeleon, card_data_ledger=card_data_ledger, card_data_quantum=card_data_quantum, card_data_multitap=card_data_multitap)


@app.route('/upgrade_card', methods=['POST'])
def upgrade_card():
    user_id = request.json.get('user_id')
    card_type = request.json.get('card_type')
    if update_card_level(user_id, card_type):
        user = session.query(User).filter_by(user_id=user_id).first()
        if user:
            user.update_profit()
            session.commit()
        return jsonify(success=True)
    return jsonify(success=False), 400


@app.route('/get_card_data', methods=['GET'])
def get_card_data_endpoint():
    user_id = request.args.get('user_id')
    card_type = request.args.get('card_type')
    
    user = session.query(User).filter_by(user_id=user_id).first()
    if user:
        card_data = get_card_data(user, card_type)
        return jsonify(card_data)
    else:
        return jsonify({'error': 'User not found'}), 404


@app.route('/friends')
def friends():
    user_id = request.args.get('user_id', 0)
    username = request.args.get('username', 'Guest')
    return render_template('friend.html', user_id=user_id, username=username)


@app.route('/earn')
def earn():
    user_id = request.args.get('user_id', 0)
    username = request.args.get('username', 'Guest')
    return render_template('task.html', user_id=user_id, username=username)


@app.route('/airdrop')
def airdrop():
    user_id = request.args.get('user_id', 0)
    username = request.args.get('username', 'Guest')
    return render_template('airdrop.html', user_id=user_id, username=username)


@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory('../src', filename)


@app.route('/assets/<path:filename>')
def assets_files(filename):
    return send_from_directory('../src/assets', filename)



@app.route('/user/<username>')
def user(username):
    user_id = request.args.get('user_id', 0)  
    user = get_user(user_id)  

    if user:
        level_thresholds = [
            0,          # Уровень 1
            5000,       # Уровень 2
            25000,      # Уровень 3
            100000,     # Уровень 4
            1000000,    # Уровень 5
            2000000,    # Уровень 6
            10000000,   # Уровень 7
            50000000,   # Уровень 8
            1000000000, # Уровень 9
            10000000000# Уровень 10
        ]

        current_level = user.level
        if current_level < len(level_thresholds):
            next_level_coins = level_thresholds[current_level] - level_thresholds[current_level - 1]
        else:
            next_level_coins = "Max level"

        return render_template(
            'index.html',
            username=user.username,
            user_id=user.user_id,
            coins=user.coins,
            profit_per_tap=user.profit_per_tap,
            profit_per_hour=user.profit_per_hour,
            level=user.level,
            next_level_coins=next_level_coins
        )
    else:
        return render_template(
            'index.html',
            username=username,
            user_id=0,
            coins=0,
            profit_per_tap=1,
            profit_per_hour=0,
            level=1,
            next_level_coins=5000
        )


@app.route('/user_data', methods=['GET'])
def user_data():
    user_id = request.args.get('user_id', 0)
    user = get_user(user_id)
    if user:
        profit_gained = accrue_profit_per_hour(user)
        level_thresholds = [
            0, 5000, 25000, 100000, 1000000,
            2000000, 10000000, 50000000, 1000000000, 10000000000
        ]

        if user.level < len(level_thresholds):
            next_level_coins = level_thresholds[user.level] - user.coins
        else:
            next_level_coins = "Max level"

        return jsonify(
            success=True,
            coins=user.coins,
            profit_per_tap=user.profit_per_tap,
            profit_per_hour=user.profit_per_hour,
            level=user.level,
            next_level_coins=next_level_coins,

            task_tg_done=user.task_tg_done,
            task_x_done=user.task_x_done,
            task_inst_done=user.task_inst_done,
            task_yt_done=user.task_yt_done,
            task_part_done=user.task_part_done,

            profit_gained=profit_gained,

            daily_day=user.daily_reward_day,
            daily_claimed=user.daily_reward_claimed,
            last_reward_claim_date=user.last_reward_claim_date.isoformat() if user.last_reward_claim_date else None
        )
    else:
        return jsonify(success=False, error="User not found"), 404



@app.route('/update_coins', methods=['POST'])
def update_coins():
    try:
        data = request.get_json()
        user_id = request.headers.get('User-ID')
        coins = data.get('coins')

        if not user_id or coins is None:
            return jsonify(success=False, error="Invalid data"), 400

        user_id = int(user_id)
        coins = int(coins)

        user = get_user(user_id)
        if user:
            level_thresholds = [
                0, 5000, 25000, 100000, 1000000,
                2000000, 10000000, 50000000, 1000000000, 10000000000
            ]

            new_level = next((i + 1 for i, threshold in enumerate(level_thresholds) if coins < threshold),
                             len(level_thresholds))

            if new_level > user.level:
                user.level = new_level

            update_user_coins(user_id, coins)

            return jsonify(success=True)
        else:
            return jsonify(success=False, error="User not found"), 404

    except Exception as e:
        return jsonify(success=False, error=str(e)), 500



@app.route('/update_profit_per_hour', methods=['POST'])
def update_profit_per_hour():
    try:
        data = request.get_json()
        user_id = request.headers.get('User-ID')
        profit_per_hour = data.get('profit_per_hour')

        if not user_id or profit_per_hour is None:
            return jsonify(success=False, error="Invalid data"), 400

        update_profit_per_hour(int(user_id), float(profit_per_hour))
        return jsonify(success=True)
    except Exception as e:
        return jsonify(success=False, error=str(e)), 500


@app.route('/invite')
def invite():
    referrer_id = request.args.get('referrer_id')
    if not referrer_id:
        return jsonify(success=False, error="Referrer ID is missing"), 400

    referrer = get_user(referrer_id)

    if not referrer:
        return jsonify(success=False, error="Referrer not found"), 404
    telegram_app_url = f"https://t.me/MMM_Coin_bot?start=referrer_{referrer_id}"

    return redirect(telegram_app_url)


@app.route('/invited_friends', methods=['GET'])
def invited_friends():
    user_id = request.args.get('user_id', 0)
    user = get_user(user_id)
    if user:
        referrals = user.friends_usernames.split(',') if user.friends_usernames else []
        return jsonify(success=True, referrals=[{"name": name} for name in referrals])
    else:
        return jsonify(success=False, error="User not found"), 404



@app.route('/award_referral_bonus', methods=['POST'])
def handle_referral_bonus():
    try:
        data = request.get_json()
        invitee_user_id = data.get('invitee_user_id')
        referrer_id = data.get('referrer_id')
        premium = data.get('premium', False)

        if not invitee_user_id or not referrer_id:
            return jsonify(success=False, error="Invalid data"), 400

        award_referral_bonus(invitee_user_id, referrer_id, premium)
        return jsonify(success=True)
    except Exception as e:
        return jsonify(success=False, error=str(e)), 500



async def check_premium_status(user_id):
    try:
        chat_member = await bot.get_chat_member(chat_id=user_id, user_id=user_id)
        premium_status = chat_member.user.is_premium if hasattr(chat_member.user, 'is_premium') else False
        print(f"User {user_id} premium status: {premium_status}")
        return premium_status
    except Exception as e:
        return False
    

@app.route('/claim_task_reward', methods=['POST'])
def claim_task_reward():
    try:
        data = request.get_json()
        user_id = int(data.get('user_id'))
        task = data.get('task')
        reward = int(data.get('reward', 0))

        user = get_user(user_id)
        if not user:
            return jsonify(success=False, message="User not found")

        attr_name = f"task_{task}_done"
        if not hasattr(user, attr_name):
            return jsonify(success=False, message="Invalid task")

        if getattr(user, attr_name):
            return jsonify(success=False, message="Reward already claimed")

        user.coins += reward
        setattr(user, attr_name, True)
        session.commit()

        return jsonify(success=True, coins=user.coins)
    except Exception as e:
        return jsonify(success=False, message=str(e))


@app.route('/claim_daily_reward', methods=['POST'])
def claim_daily_reward():
    try:
        data = request.get_json()
        user_id = int(data.get('user_id'))
        user = get_user(user_id)

        if not user:
            return jsonify(success=False, message="User not found")

        now = datetime.datetime.utcnow()
        last_claim = user.last_reward_claim_date or now - datetime.timedelta(days=1)
        days_since = (now.date() - last_claim.date()).days

        if days_since == 0:
            if user.daily_reward_claimed:
                pass
            else:
                reward = daily_reward_amount(user.daily_reward_day)
                user.coins += reward
                user.daily_reward_claimed = True
                session.commit()
                return jsonify(success=True, reward=reward, coins=user.coins)
        elif days_since == 1:
            user.daily_reward_day += 1
            if user.daily_reward_day > 7:
                user.daily_reward_day = 1
            user.daily_reward_claimed = False
            user.last_reward_claim_date = now
            session.commit()
            return jsonify(success=False, message="Новый день, открой награду", day=user.daily_reward_day)
        else:
            user.daily_reward_day = 1
            user.daily_reward_claimed = False
            user.last_reward_claim_date = now
            session.commit()
            return jsonify(success=False, message="Прогресс сброшен из-за пропуска", day=1)

    except Exception as e:
        return jsonify(success=False, message=str(e))


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
