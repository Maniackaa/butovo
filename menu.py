from config import dp, db, pat
from aiogram import types
from markups import usermenu_mkp, usercatgoods_mkp, usersubcatgoods_mkp


@dp.message_handler(text='Меню')
async def menumsg(message: types.Message):
    await message.answer('Выберите раздел:', reply_markup=usermenu_mkp())


@dp.callback_query_handler(text_contains='catuser_')
async def catusercall(call: types.CallbackQuery):
    catid = call.data.split('_')[1]
    await call.message.delete()
    await call.message.answer('Выберите раздел:', reply_markup=usercatgoods_mkp(int(catid)))


@dp.callback_query_handler(text_contains='gooduser_')
async def goodusercall(call: types.CallbackQuery):
    goodid = call.data.split('_')[1]
    await call.message.delete()
    good_info = db.get_gooduser(int(goodid))
    mkp = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('В корзину', callback_data=f'boxadd_{goodid}')
    mkp.add(btn1)
    if good_info[2] == 'None':
        await call.message.answer(f'<b>{good_info[0]}</b>\n{good_info[1]}\n<b>Стоимость</b>: {good_info[3]}p', reply_markup=mkp)
    else:
        await call.message.answer_photo(open(f'{pat}/{good_info[2]}', 'rb'), caption=f'<b>{good_info[0]}</b>\n{good_info[1]}\n<b>Стоимость</b>: {good_info[3]}p', reply_markup=mkp)

@dp.callback_query_handler(text_contains='subcattuser_')
async def subcattusercall(call: types.CallbackQuery):
    subcatid = call.data.split('_')[1]
    await call.message.delete()
    await call.message.answer('Выберите раздел:', reply_markup=usersubcatgoods_mkp(int(subcatid)))

@dp.callback_query_handler(text_contains='boxadd_')
async def boxaddcall(call: types.CallbackQuery):
    goodid = call.data.split('_')[1]
    await call.message.delete()
    good_info = db.get_gooduser(int(goodid))
    mkp = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Меню')
    btn2 = types.KeyboardButton('Корзина')
    mkp.add(btn1).add(btn2)
    db.add_box(call.from_user.id, int(goodid))
    await call.message.answer(f'Блюдо <b>{good_info[0]}</b> добавлено в корзину\n  Нажмите МЕНЮ, чтобы продолжить выбор блюд\n  Нажмите КОРЗИНА, чтобы оформить заказ', reply_markup=mkp)
    