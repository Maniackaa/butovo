from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from database import DB



# admins = [5686116279]
admins = [270392340, 834559485]

pat = '/root/bot/images'

db = DB('botblyda', 'postgres', '123321', 'localhost')


cities = {
    'vladimir': 'Владимир',
    'skolkovo': 'Сколково',
    'vidnoe': 'Видное',
    'sovhoz': 'Совхоз им. Ленина',
    'miti': 'Мытищи',
    'domod': 'Домодедово',
    'moscow': 'Москва (Текстильщики)',
    'pavelec': 'Павелецкая',
    'visota': 'Высота',
    'butovo': 'Бутово'
}


bot = Bot(token='6135886049:AAHYcN_77ZKxc0iDURSPzdkledWFsgD8DI4', parse_mode='html')
# bot = Bot(token='5669481090:AAHXyO-JyxVoDZ7RB6shxmrIlzGCveS60mA', parse_mode='html')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


# print(db.get_order_price(int(5))[-1])
