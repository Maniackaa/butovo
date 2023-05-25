from config import dp, db
from aiogram import types



@dp.message_handler(commands='start')
async def startmsg(message: types.Message):
    mkp = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Меню')
    btn2 = types.KeyboardButton('Корзина')
    mkp.add(btn1).add(btn2)
    db.add_user(message.from_user.id)
    await message.answer('Поздравляем! Вы подписались на Vitae Healthy Cafe', reply_markup=mkp)

