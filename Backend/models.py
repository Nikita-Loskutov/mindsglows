from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Boolean
from sqlalchemy import DateTime
import datetime
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, unique=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    coins = Column(Integer, default=0)
    level = Column(Integer, default=1)
    ref_link = Column(String, unique=True)
    invited_friends = Column(Integer, default=0)
    friends_usernames = Column(String)
    profit_per_hour = Column(Integer, default=0)
    profit_per_tap = Column(Integer, default=1)
    level_token = Column(Integer, default=0)
    level_staking = Column(Integer, default=0)
    level_genesis = Column(Integer, default=0)
    level_ledger = Column(Integer, default=0)
    level_echeleon = Column(Integer, default=0)
    level_quantum = Column(Integer, default=0)
    level_multitap = Column(Integer, default=1)


    task_tg_done = Column(Boolean, default=False)
    task_x_done = Column(Boolean, default=False)
    task_inst_done = Column(Boolean, default=False)
    task_yt_done = Column(Boolean, default=False)
    task_part_done = Column(Boolean, default=False)


    daily_reward_day = Column(Integer, default=1)  # текущий день от 1 до 7
    daily_reward_claimed = Column(Boolean, default=False)  # забрал ли награду сегодня
    last_reward_claim_date = Column(DateTime, default=datetime.datetime.utcnow)

    last_profit_update = Column(DateTime, default=datetime.datetime.utcnow)


    def update_profit(self):
        from db_utils import CARD_DATA


        self.profit_per_hour = 0


        if self.level_token > 0:
            self.profit_per_hour += sum([CARD_DATA['token'][i]['profit'] for i in range(self.level_token)])
        if self.level_staking > 0:
            self.profit_per_hour += sum([CARD_DATA['staking'][i]['profit'] for i in range(self.level_staking)])
        if self.level_genesis > 0:
            self.profit_per_hour += sum([CARD_DATA['genesis'][i]['profit'] for i in range(self.level_genesis)])
        if self.level_echeleon > 0:
            self.profit_per_hour += sum([CARD_DATA['echeleon'][i]['profit'] for i in range(self.level_echeleon)])
        if self.level_ledger > 0:
            self.profit_per_hour += sum([CARD_DATA['ledger'][i]['profit'] for i in range(self.level_ledger)])
        if self.level_quantum > 0:
            self.profit_per_hour += sum([CARD_DATA['quantum'][i]['profit'] for i in range(self.level_quantum)])


        self.profit_per_tap = CARD_DATA['multitap'][self.level_multitap - 1]['profit'] if self.level_multitap > 0 else 0

    def __repr__(self):
        return (f"<User(user_id={self.user_id}, username='{self.username}', coins={self.coins}, "
                f"level={self.level}, profit_per_hour={self.profit_per_hour}, "
                f"profit_per_tap={self.profit_per_tap})>")


DATABASE_URL = 'sqlite:///users.db'
engine = create_engine(DATABASE_URL, echo=True)  #В РЕЛИЗЕ ОТКЛЮЧИТЬ
Base.metadata.create_all(engine)


Session = sessionmaker(bind=engine)
session = Session()

if __name__ == "__main__":
    print("Существующие пользователи:")
    users = session.query(User).all()
    for user in users:
        print(user)