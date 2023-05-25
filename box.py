from config import dp, db, bot, admins
from aiogram import types
from aiogram.dispatcher import FSMContext
from markups import cancel_mkp
from states import OformOrder


@dp.message_handler(text='Корзина')
async def boxmsg(message: types.Message):
    box = db.get_userbox(message.from_user.id)
    if len(box) == 0:
        await message.answer('Ваша корзина пуста')
    else:
        step = 1
        text = ''
        price = 0
        for i in box:
            good_info = db.get_gooduser(i[0])
            if good_info == None:
                pass
            elif good_info[3] == '0':
                pass
            else:
                text = f'{text}{step}. {good_info[0]} | Цена: {good_info[3]}\n'
                price = float(price)+float(good_info[3])
                step=step+1
        text=f'{text}\nСумма: {price}'
        mkp = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('Оформить заказ', callback_data='oform')
        btn2 = types.InlineKeyboardButton('Очистить корзину', callback_data='clearbox')
        mkp.add(btn1).add(btn2)
        await message.answer(text, reply_markup=mkp)


@dp.callback_query_handler(text='clearbox')
async def clearboxcall(call: types.CallbackQuery):
    await call.message.delete()
    mkp = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Меню')
    btn2 = types.KeyboardButton('Корзина')
    mkp.add(btn1).add(btn2)
    db.clearbox(call.from_user.id)
    await call.message.answer('Корзина успешно очищена!\n  Нажмите МЕНЮ, чтобы продолжить выбор блюд\n  Нажмите КОРЗИНА, чтобы оформить заказ', reply_markup=mkp)



@dp.callback_query_handler(text='oform')
async def oformcall(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer('Введите ваше имя:', reply_markup=cancel_mkp())
    await OformOrder.Name.set()

@dp.callback_query_handler(text='cancel', state=OformOrder.Name)
@dp.callback_query_handler(text='cancel', state=OformOrder.Phone)
@dp.callback_query_handler(text='cancel', state=OformOrder.Time)
async def canceloformorder(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    mkp = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Меню')
    btn2 = types.KeyboardButton('Корзина')
    mkp.add(btn1).add(btn2)
    await call.message.answer('Оформление заказа отменено', reply_markup=mkp)
    await state.finish()

@dp.message_handler(state=OformOrder.Name)
async def oformordernamemsg(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Name'] = message.text
    await message.answer('Введите номер телефона для связи', reply_markup=cancel_mkp())
    await OformOrder.next()

@dp.message_handler(state=OformOrder.Phone)
async def oformorderphone(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Phone'] = message.text
    await message.answer('К какому времени приготовить ваш заказ?', reply_markup=cancel_mkp())
    await OformOrder.next()

@dp.message_handler(state=OformOrder.Time)
async def oformordertimemsg(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Time'] = message.text
    name = data['Name']
    phone = data['Phone']
    time = data['Time']
    box = db.get_userbox(message.from_user.id)
    step = 1
    text = ''
    price = 0
    for i in box:
        good_info = db.get_gooduser(i[0])
        if good_info == None:
            pass
        elif good_info[3] == '0':
            pass
        else:
            text = f'{text}{step}. {good_info[0]} | Цена: {good_info[3]}\n'
            price = float(price)+float(good_info[3])
            step=step+1
    text=f'{text}\nСумма: {price}'
    mkp = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Подтвердить', callback_data='oform1')
    btn2 = types.InlineKeyboardButton('Отменить', callback_data='cancel')
    mkp.add(btn1).add(btn2)
    await message.answer(f'Ваш заказ:\n{text}\n<b>Имя</b>: {name}\n<b>Телефон</b>: {phone}\n<b>Время</b>: {time}', reply_markup=mkp)

@dp.callback_query_handler(text='oform1', state=OformOrder.Time)
async def oformcall(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        pass
    name = data['Name']
    phone = data['Phone']
    time = data['Time']
    await call.message.delete()
    await call.message.answer('Заказ успешно оформлен!')
    box = db.get_userbox(call.from_user.id)
    step = 1
    text = ''
    price = 0
    for i in box:
        good_info = db.get_gooduser(i[0])
        if good_info == None:
            pass
        elif good_info[3] == '0':
            pass
        else:
            text = f'{text}{step}. {good_info[0]} | Цена: {good_info[3]}\n'
            price = float(price)+float(good_info[3])
            step=step+1
    text=f'{text}\nСумма: {price}\n\n<b>Имя</b>: {name}\n<b>Номер телефона</b>: {phone}\n<b>Время</b>: {time}'
    db.clearbox(call.from_user.id)
    await state.finish()
    for admin in admins:
        try:
            await bot.send_message(admin, f'Новый заказ!\n\n{text}')
        except:
            pass
    