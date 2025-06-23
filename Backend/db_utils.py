from models import session, User

from models import session, User
import datetime


def add_user(user_id, username, ref_link=None, referrer_id=None):
    try:
        existing_user = get_user(user_id)
        if existing_user:
            print(f"User {username} already exists in the database.")
            return existing_user

        user = User(user_id=user_id, username=username, ref_link=ref_link)
        session.add(user)
        session.commit()
        if referrer_id:
            update_invited_friends(referrer_id, user_id)

        return user
    except Exception as e:
        session.rollback()
        return None

def update_invited_friends(referrer_id, invitee_user_id):
    try:
        referrer = get_user(referrer_id)
        invitee = get_user(invitee_user_id)
        if referrer and invitee:
            referrer.invited_friends += 1
            if referrer.friends_usernames:
                referrer.friends_usernames += f",{invitee.username}"
            else:
                referrer.friends_usernames = invitee.username
            session.commit()
        else:
            print(f"Referrer or invitee not found.")
    except Exception as e:
        session.rollback()
        print(f"Error updating invited friends: {e}")

def award_referral_bonus(invitee_user_id, referrer_id, premium=False):
    try:
        invitee = get_user(invitee_user_id)
        referrer = get_user(referrer_id)
        if invitee and referrer:
            bonus = 0
            if premium: 
                bonus = 25000
                invitee.coins += bonus
                referrer.coins += bonus
            else: 
                bonus = 5000
                invitee.coins += bonus
                referrer.coins += bonus
            session.commit()
        else:
            print("Invitee or referrer not found.")
    except Exception as e:
        session.rollback()
        print(f"Error awarding referral bonus: {e}")


def get_user(user_id):
    try:
        return session.query(User).filter_by(user_id=user_id).first()
    except Exception as e:
        print(f"Error fetching user with user_id={user_id}: {e}")
        return None


def update_user_coins(user_id, coins):
    try:
        user = get_user(user_id)
        if user:
            user.coins = coins
            session.commit()
        else:
            print(f"No user found with user_id={user_id}.")
    except Exception as e:
        session.rollback()

def update_profit_per_hour(user_id, profit):
    try:
        user = get_user(user_id)
        if user:
            user.profit_per_hour = profit
            session.commit()
        else:
            print(f"No user found with user_id={user_id}.")
    except Exception as e:
        session.rollback()

def update_profit_per_tap(user_id, profit):
    try:
        user = get_user(user_id)
        if user:
            user.profit_per_tap = profit
            session.commit()
        else:
            print(f"No user found with user_id={user_id}.")
    except Exception as e:
        session.rollback()


def daily_reward_amount(day):
    rewards = {
        1: 5000,
        2: 10000,
        3: 15000,
        4: 20000,
        5: 25000,
        6: 30000,
        7: 50000
    }
    return rewards.get(day, 0)


def accrue_profit_per_hour(user):
    import datetime
    now = datetime.datetime.utcnow()
    if not user.last_profit_update:
        user.last_profit_update = now
        session.commit()
        return 0
    hours_passed = int((now - user.last_profit_update).total_seconds() // 3600)
    if hours_passed > 0 and user.profit_per_hour > 0:
        profit = user.profit_per_hour * hours_passed
        user.coins += profit
        user.last_profit_update = now
        session.commit()
        return profit
    return 0


CARD_DATA = {
    'token': [
        {'cost': 100, 'profit': 10},
        {'cost': 70, 'profit': 15},
        {'cost': 100, 'profit': 20},
        {'cost': 140, 'profit': 25},
        {'cost': 190, 'profit': 35},
        {'cost': 270, 'profit': 45},
        {'cost': 375, 'profit': 58},
        {'cost': 525, 'profit': 75},
        {'cost': 735, 'profit': 100},
        {'cost': 1030, 'profit': 125},
        {'cost': 1440, 'profit': 160},
        {'cost': 2020, 'profit': 210},
        {'cost': 2825, 'profit': 275},
        {'cost': 3955, 'profit': 355},
        {'cost': 5540, 'profit': 465},
        {'cost': 7755, 'profit': 605},
        {'cost': 10860, 'profit': 785},
        {'cost': 15200, 'profit': 1020},
        {'cost': 21285, 'profit': 1325},
        {'cost': 29800, 'profit': 1725},
    ],
    'staking': [
        {'cost': 500, 'profit': 50},
        {'cost': 350, 'profit': 85},
        {'cost': 490, 'profit': 110},
        {'cost': 685, 'profit': 140},
        {'cost': 960, 'profit': 185},
        {'cost': 1300, 'profit': 240},
        {'cost': 1880, 'profit': 315},
        {'cost': 2635, 'profit': 400},
        {'cost': 3690, 'profit': 530},
        {'cost': 5165, 'profit': 680},
        {'cost': 7230, 'profit': 890},
        {'cost': 10120, 'profit': 1165},
        {'cost': 15170, 'profit': 1515},
        {'cost': 20840, 'profit': 1965},
        {'cost': 25750, 'profit': 2555},
        {'cost': 40880, 'profit': 3320},
        {'cost': 55435, 'profit': 4320},
        {'cost': 75210, 'profit': 5615},
        {'cost': 105690, 'profit': 7300},
        {'cost': 150370, 'profit': 9490},
    ],
    'genesis': [
        {'cost': 2500, 'profit': 250},
        {'cost': 1750, 'profit': 420},
        {'cost': 2500, 'profit': 550},
        {'cost': 3400, 'profit': 715},
        {'cost': 4800, 'profit': 900},
        {'cost': 6700, 'profit': 1200},
        {'cost': 9400, 'profit': 1600},
        {'cost': 15200, 'profit': 2000},
        {'cost': 20450, 'profit': 2600},
        {'cost': 25800, 'profit': 3500},
        {'cost': 35150, 'profit': 4500},
        {'cost': 50600, 'profit': 5800},
        {'cost': 70850, 'profit': 7600},
        {'cost': 100200, 'profit': 9800},
        {'cost': 140850, 'profit': 12800},
        {'cost': 200350, 'profit': 16600},
        {'cost': 280100, 'profit': 21600},
        {'cost': 380900, 'profit': 28000},
        {'cost': 550400, 'profit': 36500},
        {'cost': 745700, 'profit': 47450},
    ],
    'echeleon': [
        {'cost': 10000, 'profit': 1000},
        {'cost': 5000, 'profit': 1700},
        {'cost': 9800, 'profit': 2200},
        {'cost': 13700, 'profit': 2800},
        {'cost': 20200, 'profit': 3700},
        {'cost': 25900, 'profit': 4800},
        {'cost': 40600, 'profit': 6300},
        {'cost': 50700, 'profit': 8200},
        {'cost': 70800, 'profit': 10600},
        {'cost': 105300, 'profit': 13800},
        {'cost': 145600, 'profit': 17900},
        {'cost': 200500, 'profit': 23300},
        {'cost': 300500, 'profit': 30300},
        {'cost': 400900, 'profit': 39400},
        {'cost': 550600, 'profit': 51200},
        {'cost': 750800, 'profit': 66500},
        {'cost': 1100000, 'profit': 86500},
        {'cost': 1500600, 'profit': 112500},
        {'cost': 2150500, 'profit': 146200},
        {'cost': 3000000, 'profit': 190000},
    ],
    'ledger': [
        {'cost': 50000, 'profit': 5000},
        {'cost': 35000, 'profit': 8500},
        {'cost': 50000, 'profit': 10000},
        {'cost': 70500, 'profit': 14500},
        {'cost': 95000, 'profit': 18500},
        {'cost': 135500, 'profit': 24000},
        {'cost': 200000, 'profit': 31000},
        {'cost': 260500, 'profit': 40000},
        {'cost': 370000, 'profit': 53000},
        {'cost': 515500, 'profit': 68000},
        {'cost': 725500, 'profit': 89500},
        {'cost': 1015000, 'profit': 115500},
        {'cost': 1415450, 'profit': 150500},
        {'cost': 1985500, 'profit': 195500},
        {'cost': 2780000, 'profit': 255000},
        {'cost': 3890000, 'profit': 330000},
        {'cost': 5500000, 'profit': 430500},
        {'cost': 7500000, 'profit': 560500},
        {'cost': 10500000, 'profit': 730000},
        {'cost': 15000000, 'profit': 950000},
    ],
    'quantum': [
        {'cost': 250000, 'profit': 25000},
        {'cost': 175000, 'profit': 40000},
        {'cost': 245000, 'profit': 55000},
        {'cost': 343000, 'profit': 70000},
        {'cost': 480200, 'profit': 90000},
        {'cost': 670000, 'profit': 120000},
        {'cost': 945000, 'profit': 155000},
        {'cost': 1315000, 'profit': 205000},
        {'cost': 1845000, 'profit': 265000},
        {'cost': 2580000, 'profit': 345000},
        {'cost': 3615000, 'profit': 450000},
        {'cost': 5060000, 'profit': 580000},
        {'cost': 7085000, 'profit': 760000},
        {'cost': 9920000, 'profit': 985000},
        {'cost': 13890000, 'profit': 1250000},
        {'cost': 19445000, 'profit': 1665000},
        {'cost': 27225000, 'profit': 2150000},
        {'cost': 38115000, 'profit': 2800000},
        {'cost': 53350000, 'profit': 3650000},
        {'cost': 74700000, 'profit': 4750000},
    ],
    'multitap': [
        {'cost': 5000, 'profit': 1},
        {'cost': 7500, 'profit': 2},
        {'cost': 11250, 'profit': 3},
        {'cost': 16875, 'profit': 4},
        {'cost': 25310, 'profit': 5},
        {'cost': 37965, 'profit': 6},
        {'cost': 56950, 'profit': 7},
        {'cost': 85430, 'profit': 8},
        {'cost': 125140, 'profit': 9},
        {'cost': 190215, 'profit': 10},
        {'cost': 290320, 'profit': 11},
        {'cost': 430480, 'profit': 12},
        {'cost': 650720, 'profit': 13},
        {'cost': 970080, 'profit': 14},
        {'cost': 1460620, 'profit': 15},
        {'cost': 2190430, 'profit': 16},
        {'cost': 3285145, 'profit': 17},
        {'cost': 4925215, 'profit': 18},
        {'cost': 7390325, 'profit': 19},
        {'cost': 11005985, 'profit': 20},
    ]
}
   

def get_card_data(user, card_type):
    level_attr = f'level_{card_type}'
    current_level = getattr(user, level_attr, 0)
    card_data = CARD_DATA.get(card_type, [])
    if 0 <= current_level < len(card_data):
        data = card_data[current_level]
        data['level'] = current_level
        return data
    return {'cost': 0, 'profit': 0, 'level': current_level}



def update_card_level(user_id, card_type):
    user = session.query(User).filter_by(user_id=user_id).first()
    if user:
        level_attr = f'level_{card_type}'
        current_level = getattr(user, level_attr, 0)
        card_data = CARD_DATA.get(card_type, [])
        if current_level < len(card_data):
            cost = card_data[current_level]['cost']
            if user.coins >= cost:
                user.coins -= cost
                setattr(user, level_attr, current_level + 1)
                session.commit()
                return True
    return False



if __name__ == "__main__":

    user_id = 1
    username = "test_user"
    ref_link = "http://example.com/ref/1"


    add_user(user_id, username, ref_link)


    update_user_coins(user_id, 100)


    user = get_user(user_id)
    if user:
        print(user)

    card_type = 'token'
    if update_card_level(user_id, card_type):
        print(f"User {user_id}'s {card_type} level updated.")
    else:
        print(f"Failed to update {card_type} level for user {user_id}.")

    update_profit_per_hour(user_id, 50.0)
    update_profit_per_tap(user_id, 2.5)