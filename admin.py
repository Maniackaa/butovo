from config import dp, db, cities, bot, pat
from aiogram import types
from aiogram.dispatcher import FSMContext
from markups import admin_mkp, catadm_mkp, cancel_mkp, catgoodadm_mkp, citiescat_mkp, citiesgoods_mkp, subcatgoods_mkp, citiessubcat_mkp
from states import AddCat, AddGood, AddCityGood, AddSubCat, AddSubGood


@dp.message_handler(commands='admin')
async def admincmd(message: types.Message):
    await message.answer('Здравствуйте. Вы в админ-панеле', reply_markup=admin_mkp())


@dp.callback_query_handler(text='admin')
async def admincall(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer('Вы в админ-панеле', reply_markup=admin_mkp())

@dp.callback_query_handler(text='blydaadm')
async def blydaadmcall(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer('Выберите категорию:', reply_markup=catadm_mkp())

@dp.callback_query_handler(text='addcatadm')
async def addcatadmcall(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer('Введите название новой категории', reply_markup=cancel_mkp())
    await AddCat.CatName.set()

@dp.callback_query_handler(text='cancel', state=AddCat.CatName)
async def addcatcatnamecancel(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer('Отменено. Вы были возвращены в админ-панель', reply_markup=admin_mkp())
    await state.finish()

@dp.message_handler(state=AddCat.CatName)
async def addcatcatnamemsg(message: types.Message, state: FSMContext):
    db.add_cat(message.text)
    await message.answer('Категория успешно добавлена. Вы были вовращены в админ-панель', reply_markup=admin_mkp())
    await state.finish()


@dp.callback_query_handler(text_contains='catadm_')
async def catadmcall(call: types.CallbackQuery):
    catid = call.data.split('_')[1]
    catname = db.get_catname(int(catid))
    await call.message.delete()
    await call.message.answer(f'Категория: <code>{catname}</code>\nВыберите подкатегорию\товар', reply_markup=catgoodadm_mkp(int(catid)))

@dp.callback_query_handler(text_contains='citiescat_')
async def citiescatcall(call: types.CallbackQuery):
    catid = call.data.split('_')[1]
    catname = db.get_catname(int(catid))
    await call.message.delete()
    await call.message.answer(f'Категория: <code>{catname}</code>', reply_markup=citiescat_mkp(int(catid)))

@dp.callback_query_handler(text_contains='citycats_')
async def citycatscall(call: types.CallbackQuery):
    catid = call.data.split('_')[1]
    city = call.data.split('_')[2]
    db.updatecitycat(int(catid), city)
    catname = db.get_catname(int(catid))
    await call.message.delete()
    await call.message.answer(f'Категория: <code>{catname}</code>', reply_markup=citiescat_mkp(int(catid)))

@dp.callback_query_handler(text_contains='catadmdel_')
async def catadmdelcall(call: types.CallbackQuery):
    catid = call.data.split('_')[1]
    await call.message.delete()
    catname = db.get_catname(int(catid))
    mkp = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Да', callback_data=f'catadmdell_{catid}')
    btn2 = types.InlineKeyboardButton('Отменить', callback_data='admin')
    mkp.add(btn1, btn2)
    await call.message.answer(f'Вы действительно хотите удалить категорию "{catname}"', reply_markup=mkp)

@dp.callback_query_handler(text_contains='catadmdell_')
async def catadmdellcall(call: types.CallbackQuery):
    catid = call.data.split('_')[1]
    db.delcat(int(catid))
    await call.message.delete()
    await call.message.answer('Категория успешно удалена. Вы были возвращены в админ-панель', reply_markup=admin_mkp())


@dp.callback_query_handler(text_contains='addgoodadm_')
async def addgoodadmcall(call: types.CallbackQuery, state: FSMContext):
    catid = call.data.split('_')[1]
    await call.message.delete()
    await AddGood.CatId.set()
    async with state.proxy() as data:
        data['CatId'] = catid
    await AddGood.next()
    await call.message.answer('Введите название блюда:', reply_markup=cancel_mkp())

@dp.callback_query_handler(text='cancel', state=AddGood.Name)
@dp.callback_query_handler(text='cancel', state=AddGood.Desc)
@dp.callback_query_handler(text='cancel', state=AddGood.Photo)
@dp.callback_query_handler(text='cancel', state=AddGood.Price)
async def canceladdgoodcall(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer('Отменено. Вы были возвращены в админ-панель', reply_markup=admin_mkp())
    await state.finish()

@dp.message_handler(state=AddGood.Name)
async def addgoodnamemsg(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Name'] = message.text
    await message.answer(f'Введите описание к <code>{message.text}</code>', reply_markup=cancel_mkp())
    await AddGood.next()

@dp.message_handler(state=AddGood.Desc)
async def addgooddescmsg(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Desc'] = message.text
    goodname = data['Name']
    await message.answer(f'Введите цену для <code>{goodname}</code>\nЦелым числом или через точку. Пример: <code>149.99</code>', reply_markup=cancel_mkp())
    await AddGood.next()


@dp.message_handler(state=AddGood.Price)
async def addgoodpricemsg(message: types.Message, state: FSMContext):
    try:
        price = float(message.text)
        async with state.proxy() as data:
            data['Price'] = price
        mkp = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('Пропустить', callback_data='skip')
        btn2 = types.InlineKeyboardButton('Отменить', callback_data='cancel')
        mkp.add(btn1).add(btn2)
        await message.answer('Отправьте фотографию блюда или нажмите "Пропустить"', reply_markup=mkp)
        await AddGood.next()
    except:
        await message.answer('Введите цену целым числом или через точку. Пример: <code>149.99</code>', reply_markup=cancel_mkp())


@dp.callback_query_handler(text='skip', state=AddGood.Photo)
async def skipaddgoodphoto(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    async with state.proxy() as data:
        data['Photo'] = 'None'
    catid = data['CatId']
    name = data['Name']
    desc = data['Desc']
    price = data['Price']
    photo = data['Photo']
    db.add_goodcat(int(catid), name, desc, price, photo)
    await call.message.answer('Блюдо успешно добавлено! Вы были возвращены в админ-панель', reply_markup=admin_mkp())
    await state.finish()


@dp.message_handler(content_types='photo', state=AddGood.Photo)
async def addgoodphotoctphoto(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        pass
    catid = data['CatId']
    name = data['Name']
    desc = data['Desc']
    price = data['Price']
    file_info = await bot.get_file(message.photo[-1].file_id)
    filename = file_info.file_path.split('/')[-1]
    await bot.download_file(file_info.file_path, f'{pat}/{filename}')
    photo = filename
    db.add_goodcat(int(catid), name, desc, price, photo)
    await message.answer('Блюдо успешно добавлено! Вы были возвращены в админ-панель', reply_markup=admin_mkp())
    await state.finish()

@dp.callback_query_handler(text_contains='goodadm_')
async def goodadmcall(call: types.CallbackQuery):
    goodid = call.data.split('_')[1]
    await call.message.delete()
    goodinfo = db.get_goodadm(int(goodid))
    mkp = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('🏠 Города', callback_data=f'goodcadm_{goodid}')
    btn2 = types.InlineKeyboardButton('🗑 Удалить', callback_data=f'delgooda_{goodid}')
    btn3 = types.InlineKeyboardButton('Админ-панель', callback_data='admin')
    mkp.add(btn1).add(btn2).add(btn3)
    if goodinfo[2] == 'None':
        await call.message.answer(f'<code>{goodinfo[0]}</code>\n\n{goodinfo[1]}', reply_markup=mkp)
    else:
        await call.message.answer_photo(open(f'{pat}/{goodinfo[2]}', 'rb'), caption=f'<code>{goodinfo[0]}</code>\n\n{goodinfo[1]}', reply_markup=mkp)

@dp.callback_query_handler(text_contains='delgooda_')
async def delgoodacall(call: types.CallbackQuery):
    goodid = call.data.split('_')[1]
    goodinfo = db.get_goodadm(int(goodid))
    await call.message.delete()
    mkp = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Да', callback_data=f'delgoodad_{goodid}')
    btn2 = types.InlineKeyboardButton('Отменить', callback_data=f'goodadm_{goodid}')
    mkp.add(btn1).add(btn2)
    await call.message.answer(f'Вы действительно хотите удалить блюдо "{goodinfo[0]}"', reply_markup=mkp)

@dp.callback_query_handler(text_contains='delgoodad_')
async def delgoodadcall(call: types.CallbackQuery):
    goodid = call.data.split('_')[1]
    db.delgood(int(goodid))
    await call.message.delete()
    await call.message.answer('Успешно удалено! Вы были возвращены в админ-панель', reply_markup=admin_mkp())
    

@dp.callback_query_handler(text_contains='goodcadm_')
async def goodcadmcall(call: types.CallbackQuery):
    goodid = call.data.split('_')[1]
    goodinfo = db.get_goodadm(int(goodid))
    await call.message.delete()
    await call.message.answer(f'Города, где отображается <code>{goodinfo[0]}</code>:', reply_markup=citiesgoods_mkp(int(goodid)))

@dp.callback_query_handler(text_contains='citygoodsdel_')
async def citygoodsdelcall(call: types.CallbackQuery):
    goodid = call.data.split('_')[1]
    city = call.data.split('_')[2]
    await call.message.delete()
    goodinfo = db.get_goodadm(int(goodid))
    db.delcity_good(int(goodid), city)
    await call.message.answer(f'Города, где отображается <code>{goodinfo[0]}</code>:', reply_markup=citiesgoods_mkp(int(goodid)))


@dp.callback_query_handler(text_contains='citygoods_')
async def citygoodscall(call: types.CallbackQuery, state: FSMContext):
    goodid = call.data.split('_')[1]
    city = call.data.split('_')[2]
    cityname = cities[f'{city}']
    goodinfo = db.get_goodadm(int(goodid))
    await AddCityGood.GoodId.set()
    async with state.proxy() as data:
        data['GoodId'] = goodid
    await AddCityGood.next()
    async with state.proxy() as data:
        data['City'] = city
    await call.message.delete()
    await call.message.answer(f'Введите цену блюда "{goodinfo[0]}" для города {cityname}:', reply_markup=cancel_mkp())

@dp.callback_query_handler(state=AddCityGood.City, text='cancel')
async def canceladdcitygoodcall(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer('Отменено. Вы были возвращены в меню', reply_markup=admin_mkp())
    await state.finish()

@dp.message_handler(state=AddCityGood.City)
async def addcitygoodcitymsg(message: types.Message, state: FSMContext):
    try:
        price = float(message.text)
        async with state.proxy() as data:
            pass
        goodid = data['GoodId']
        city = data['City']
        db.addcity_good(int(goodid), city, price)
        await state.finish()
        goodinfo = db.get_goodadm(int(goodid))
        await message.answer(f'Города, где отображается <code>{goodinfo[0]}</code>:', reply_markup=citiesgoods_mkp(int(goodid)))
    except:
        await message.answer('Введите цену целым числом или через точку. Например <code>149.99</code>')



@dp.callback_query_handler(text_contains='subcatadmadd_')
async def subcatadmaddcall(call: types.CallbackQuery, state: FSMContext):
    catid = call.data.split('_')[1]
    await AddSubCat.CatId.set()
    async with state.proxy() as data:
        data['CatId'] = catid
    await call.message.delete()
    await call.message.answer('Введите название подкатегории:', reply_markup=cancel_mkp())
    await AddSubCat.next()

@dp.callback_query_handler(text='cancel', state=AddSubCat.Name)
async def canceladdsubcatcall(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer('Отменено. Вы были возвращены в админ-панель', reply_markup=admin_mkp())
    await state.finish()

@dp.message_handler(state=AddSubCat.Name)
async def addsubcatnamemsg(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Name'] = message.text
    catid = data['CatId']
    catname = db.get_catname(int(catid))
    mkp = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Да', callback_data='go')
    btn2 = types.InlineKeyboardButton('Отменить', callback_data='cancel')
    mkp.add(btn1).add(btn2)
    await message.answer(f'Вы действительно хотите добавить подкатегорию "<code>{message.text}</code>"\nВ категорию {catname}', reply_markup=mkp)

@dp.callback_query_handler(text='go', state=AddSubCat.Name)
async def addsubcatnamegocall(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        pass
    catid = data['CatId']
    name = data['Name']
    db.add_subcat(int(catid), name)
    await call.message.delete()
    await call.message.answer('Подкатегория успешно добавлена! Вы были возвращены в админ-панель', reply_markup=admin_mkp())
    await state.finish()

@dp.callback_query_handler(text_contains='subcattadm_')
async def subcattadmcall(call: types.CallbackQuery):
    subcatid = call.data.split('_')[1]
    subcatname = db.get_subcatname(int(subcatid))
    await call.message.delete()
    await call.message.answer(f'Подкатегория <code>{subcatname}</code>', reply_markup=subcatgoods_mkp(int(subcatid)))


@dp.callback_query_handler(text_contains='subcattadmdel_')
async def subcattadmdelcall(call: types.CallbackQuery):
    subcatid = call.data.split('_')[1]
    subcatname = db.get_subcatname(int(subcatid))
    await call.message.delete()
    mkp = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Да', callback_data=f'subcatttadmdel_{subcatid}')
    btn2 = types.InlineKeyboardButton('Отменить', callback_data='admin')
    mkp.add(btn1).add(btn2)
    await call.message.answer(f'Вы действительно хотите удалить подкатегорию <code>{subcatname}</code>', reply_markup=mkp)


@dp.callback_query_handler(text_contains='subcatttadmdel_')
async def subcatttadmdelcall(call: types.CallbackQuery):
    subcatid = call.data.split('_')[1]
    db.del_subcat(int(subcatid))
    await call.message.delete()
    await call.message.answer('Подкатегория успешно удалена! Вы были возвращены в админ-панель', reply_markup=admin_mkp())


@dp.callback_query_handler(text_contains='citiessubcatttgood_')
async def citiessubcatttgoodcall(call: types.CallbackQuery):
    subcatid = call.data.split('_')[1]
    subcatname = db.get_subcatname(int(subcatid))
    await call.message.delete()
    await call.message.answer(f'Города где отображается подкатегория <code>{subcatname}</code>', reply_markup=citiessubcat_mkp(int(subcatid)))


@dp.callback_query_handler(text_contains='citysubcats_')
async def citysubcatscall(call: types.CallbackQuery):
    subcatid = call.data.split('_')[1]
    city = call.data.split('_')[2]
    db.changecitysubcat(int(subcatid), city)
    subcatname = db.get_subcatname(int(subcatid))
    await call.message.delete()
    await call.message.answer(f'Города где отображается подкатегория <code>{subcatname}</code>', reply_markup=citiessubcat_mkp(int(subcatid)))

@dp.callback_query_handler(text_contains='addgoodsubadm_')
async def addgoodsubadmcall(call: types.CallbackQuery, state: FSMContext):
    subcatid = call.data.split('_')[1]
    await call.message.delete()
    await AddSubGood.SubcatId.set()
    async with state.proxy() as data:
        data['SubcatId'] = subcatid
    await AddSubGood.next()
    subcatname = db.get_subcatname(int(subcatid))
    await call.message.answer(f'Подкатегория <code>{subcatname}</code>\nВведите название товара', reply_markup=cancel_mkp())

@dp.callback_query_handler(text='cancel', state=AddSubGood.Name)
@dp.callback_query_handler(text='cancel', state=AddSubGood.Price)
@dp.callback_query_handler(text='cancel', state=AddSubGood.Desc)
@dp.callback_query_handler(text='cancel', state=AddSubGood.Photo)
async def canceladdsubgoodcall(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer('Отменено. Вы были возвращены в меню', reply_markup=admin_mkp())
    await state.finish()

@dp.message_handler(state=AddSubGood.Name)
async def addsubgoodnamemsg(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Name'] = message.text
    subcatid = data['SubcatId']
    subcatname = db.get_subcatname(int(subcatid))
    await AddSubGood.next()
    await message.answer(f'Подкатегория <code>{subcatname}</code>\nВведите описание блюда', reply_markup=cancel_mkp())

@dp.message_handler(state=AddSubGood.Desc)
async def addsubgooddescmsg(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Desc'] = message.text
    subcatid = data['SubcatId']
    subcatname = db.get_subcatname(int(subcatid))
    await AddSubGood.next()
    await message.answer(f'Подкатегория <code>{subcatname}</code>\nВведите цену блюда целым числом или через точку. Пример: <code>149.99</code>', reply_markup=cancel_mkp())

@dp.message_handler(state=AddSubGood.Price)
async def addsubgoodpricemsg(message: types.Message, state: FSMContext):
    try:
        price = float(message.text)
        async with state.proxy() as data:
            data['Price'] = price
        subcatid = data['SubcatId']
        subcatname = db.get_subcatname(int(subcatid))
        await AddSubGood.next()
        mkp = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('Пропустить', callback_data='skip')
        btn2 = types.InlineKeyboardButton('Отменить', callback_data='cancel')
        mkp.add(btn1).add(btn2)
        await message.answer(f'Подкатегория <code>{subcatname}</code>\nОтправьте фото или нажмите "Пропустить"', reply_markup=mkp)
    except:
        await message.answer('Введите цену блюда целым числом или через точку. Пример: <code>149.99</code>', reply_markup=cancel_mkp())


@dp.callback_query_handler(text='skip', state=AddSubGood.Photo)
async def addsubgoodphotoskipcall(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['Photo'] = 'None'
    subcatid = data['SubcatId']
    name = data['Name']
    desc = data['Desc']
    price = data['Price']
    photo = data['Photo']
    db.add_goodsubcat(int(subcatid), name, desc, price, photo)
    await call.message.delete()
    await call.message.answer('Блюдо успешно добавлено! Вы были возвращены в админ-панель', reply_markup=admin_mkp())
    await state.finish()

@dp.message_handler(content_types='photo', state=AddSubGood.Photo)
async def addsubgoodphotoctphoto(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        pass
    subcatid = data['SubcatId']
    name = data['Name']
    desc = data['Desc']
    price = data['Price']
    file_info = await bot.get_file(message.photo[-1].file_id)
    filename = file_info.file_path.split('/')[-1]
    await bot.download_file(file_info.file_path, f'{pat}/{filename}')
    photo = filename
    db.add_goodsubcat(int(subcatid), name, desc, price, photo)
    await message.answer('Блюдо успешно добавлено! Вы были возвращены в админ-панель', reply_markup=admin_mkp())
    await state.finish()