from config import db
from aiogram import types


def admin_mkp():
    mkp = types.InlineKeyboardMarkup()

    btn1 = types.InlineKeyboardButton('Блюда', callback_data='blydaadm')
    mkp.add(btn1)
    return mkp


def catadm_mkp():
    catlist = db.get_categoriesadm()
    mkp = types.InlineKeyboardMarkup(row_width=2)
    for cat in catlist:
        mkp.insert(types.InlineKeyboardButton(cat[1], callback_data=f'catadm_{cat[0]}'))
    mkp.add(types.InlineKeyboardButton('➕ Добавить категорию', callback_data='addcatadm'))
    mkp.add(types.InlineKeyboardButton('🔙 Вернуться', callback_data='admin'))
    return mkp


def catgoodadm_mkp(catid):
    subcatgoods = db.get_catgoods(catid)
    mkp = types.InlineKeyboardMarkup(row_width=2)
    for i in subcatgoods:
        if i[2] == 'good':
            mkp.insert(types.InlineKeyboardButton(i[1], callback_data=f'{i[2]}adm_{i[0]}'))
        else:
            mkp.insert(types.InlineKeyboardButton(i[1], callback_data=f'{i[2]}tadm_{i[0]}'))
    mkp.add(types.InlineKeyboardButton('✅ Добавить блюдо', callback_data=f'addgoodadm_{catid}'))
    mkp.add(types.InlineKeyboardButton('➕ Добавить подкатегорию', callback_data=f'subcatadmadd_{catid}'))
    mkp.add(types.InlineKeyboardButton('🏠Города', callback_data=f'citiescat_{catid}'))
    mkp.add(types.InlineKeyboardButton('🗑 Удалить категорию', callback_data=f'catadmdel_{catid}'))
    mkp.add(types.InlineKeyboardButton('Админ-панель', callback_data='admin'))
    return mkp

def subcatgoods_mkp(subcatid):
    subcatgoods = db.get_subcatgoods(int(subcatid))
    mkp = types.InlineKeyboardMarkup(row_width=2)
    for i in subcatgoods:
        mkp.insert(types.InlineKeyboardButton(i[1], callback_data=f'goodadm_{i[0]}'))
    mkp.add(types.InlineKeyboardButton('➕ Добавить блюдо', callback_data=f'addgoodsubadm_{subcatid}'))
    mkp.add(types.InlineKeyboardButton('🏠Города', callback_data=f'citiessubcatttgood_{subcatid}'))
    mkp.add(types.InlineKeyboardButton('🗑 Удалить подкатегорию', callback_data=f'subcattadmdel_{subcatid}'))
    mkp.add(types.InlineKeyboardButton('Админ-панель', callback_data='admin'))
    return mkp

def cancel_mkp():
    mkp = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Отменить', callback_data='cancel')
    mkp.add(btn1)
    return mkp

def citiessubcat_mkp(subcatid):
    cities_list = db.get_citiessubcat(int(subcatid))

    vladimir = cities_list[0]
    skolkovo = cities_list[1]
    vidnoe = cities_list[2]
    sovhoz = cities_list[3]
    mitish = cities_list[4]
    domod = cities_list[5]
    moscow = cities_list[6]
    pavelec = cities_list[7]
    visota = cities_list[8]

    mkp = types.InlineKeyboardMarkup()
    if vladimir == '0':
        mkp.add(types.InlineKeyboardButton('❌ Владимир', callback_data=f'citysubcats_{subcatid}_vladimir'))
    else:
        mkp.add(types.InlineKeyboardButton('✅ Владимир', callback_data=f'citysubcats_{subcatid}_vladimir'))
    if skolkovo == '0':
        mkp.add(types.InlineKeyboardButton('❌ Сколково', callback_data=f'citysubcats_{subcatid}_skolkovo'))
    else:
        mkp.add(types.InlineKeyboardButton('✅ Сколково', callback_data=f'citysubcats_{subcatid}_skolkovo'))
    if vidnoe == '0':
        mkp.add(types.InlineKeyboardButton('❌ Видное', callback_data=f'citysubcats_{subcatid}_vidnoe'))
    else:
        mkp.add(types.InlineKeyboardButton('✅ Видное', callback_data=f'citysubcats_{subcatid}_vidnoe'))
    if sovhoz == '0':
        mkp.add(types.InlineKeyboardButton('❌ Совхоз Ленина', callback_data=f'citysubcats_{subcatid}_sovhoz'))
    else:
        mkp.add(types.InlineKeyboardButton('✅ Совхоз Ленина', callback_data=f'citysubcats_{subcatid}_sovhoz'))
    if mitish == '0':
        mkp.add(types.InlineKeyboardButton('❌ Мытищи', callback_data=f'citysubcats_{subcatid}_miti'))
    else:
        mkp.add(types.InlineKeyboardButton('✅ Мытищи', callback_data=f'citysubcats_{subcatid}_miti'))
    if domod == '0':
        mkp.add(types.InlineKeyboardButton('❌ Домодедово', callback_data=f'citysubcats_{subcatid}_domod'))
    else:
        mkp.add(types.InlineKeyboardButton('✅ Домодедово', callback_data=f'citysubcats_{subcatid}_domod'))
    if moscow == '0':
        mkp.add(types.InlineKeyboardButton('❌ Москва', callback_data=f'citysubcats_{subcatid}_moscow'))
    else:
        mkp.add(types.InlineKeyboardButton('✅ Москва', callback_data=f'citysubcats_{subcatid}_moscow'))
    if pavelec == '0':
        mkp.add(types.InlineKeyboardButton('❌ Павелецкая', callback_data=f'citysubcats_{subcatid}_pavelec'))
    else:
        mkp.add(types.InlineKeyboardButton('✅ Павелецкая', callback_data=f'citysubcats_{subcatid}_pavelec'))
    if visota == '0':
        mkp.add(types.InlineKeyboardButton('❌ Высота', callback_data=f'citysubcats_{subcatid}_visota'))
    else:
        mkp.add(types.InlineKeyboardButton('✅ Высота', callback_data=f'citysubcats_{subcatid}_visota'))
    mkp.add(types.InlineKeyboardButton('Вернуться', callback_data=f'subcattadm_{subcatid}'))
    return mkp

def citiescat_mkp(catid):
    cities_list = db.get_citiescat(int(catid))

    vladimir = cities_list[0]
    skolkovo = cities_list[1]
    vidnoe = cities_list[2]
    sovhoz = cities_list[3]
    mitish = cities_list[4]
    domod = cities_list[5]
    moscow = cities_list[6]
    pavelec = cities_list[7]
    visota = cities_list[8]

    mkp = types.InlineKeyboardMarkup()
    if vladimir == 'no':
        mkp.add(types.InlineKeyboardButton('❌ Владимир', callback_data=f'citycats_{catid}_vladimir'))
    else:
        mkp.add(types.InlineKeyboardButton('✅ Владимир', callback_data=f'citycats_{catid}_vladimir'))
    if skolkovo == 'no':
        mkp.add(types.InlineKeyboardButton('❌ Сколково', callback_data=f'citycats_{catid}_skolkovo'))
    else:
        mkp.add(types.InlineKeyboardButton('✅ Сколково', callback_data=f'citycats_{catid}_skolkovo'))
    if vidnoe == 'no':
        mkp.add(types.InlineKeyboardButton('❌ Видное', callback_data=f'citycats_{catid}_vidnoe'))
    else:
        mkp.add(types.InlineKeyboardButton('✅ Видное', callback_data=f'citycats_{catid}_vidnoe'))
    if sovhoz == 'no':
        mkp.add(types.InlineKeyboardButton('❌ Совхоз Ленина', callback_data=f'citycats_{catid}_sovhoz'))
    else:
        mkp.add(types.InlineKeyboardButton('✅ Совхоз Ленина', callback_data=f'citycats_{catid}_sovhoz'))
    if mitish == 'no':
        mkp.add(types.InlineKeyboardButton('❌ Мытищи', callback_data=f'citycats_{catid}_miti'))
    else:
        mkp.add(types.InlineKeyboardButton('✅ Мытищи', callback_data=f'citycats_{catid}_miti'))
    if domod == 'no':
        mkp.add(types.InlineKeyboardButton('❌ Домодедово', callback_data=f'citycats_{catid}_domod'))
    else:
        mkp.add(types.InlineKeyboardButton('✅ Домодедово', callback_data=f'citycats_{catid}_domod'))
    if moscow == 'no':
        mkp.add(types.InlineKeyboardButton('❌ Москва', callback_data=f'citycats_{catid}_moscow'))
    else:
        mkp.add(types.InlineKeyboardButton('✅ Москва', callback_data=f'citycats_{catid}_moscow'))
    if pavelec == 'no':
        mkp.add(types.InlineKeyboardButton('❌ Павелецкая', callback_data=f'citycats_{catid}_pavelec'))
    else:
        mkp.add(types.InlineKeyboardButton('✅ Павелецкая', callback_data=f'citycats_{catid}_pavelec'))
    if visota == 'no':
        mkp.add(types.InlineKeyboardButton('❌ Высота', callback_data=f'citycats_{catid}_visota'))
    else:
        mkp.add(types.InlineKeyboardButton('✅ Высота', callback_data=f'citycats_{catid}_visota'))
    mkp.add(types.InlineKeyboardButton('Вернуться', callback_data=f'catadm_{catid}'))
    return mkp


def citiesgoods_mkp(goodid):
    cities_list = db.getcities_good(int(goodid))
    vladimir = cities_list[0]
    skolkovo = cities_list[1]
    vidnoe = cities_list[2]
    sovhoz = cities_list[3]
    mitish = cities_list[4]
    domod = cities_list[5]
    moscow = cities_list[6]
    pavelec = cities_list[7]
    visota = cities_list[8]
    mkp = types.InlineKeyboardMarkup()

    if vladimir == '0':
        mkp.add(types.InlineKeyboardButton('❌ Владимир', callback_data=f'citygoods_{goodid}_vladimir'))
    else:
        mkp.add(types.InlineKeyboardButton(f'✅ Владимир | {vladimir}', callback_data=f'citygoodsdel_{goodid}_vladimir'))
    if skolkovo == '0':
        mkp.add(types.InlineKeyboardButton('❌ Сколково', callback_data=f'citygoods_{goodid}_skolkovo'))
    else:
        mkp.add(types.InlineKeyboardButton(f'✅ Сколково | {skolkovo}', callback_data=f'citygoodsdel_{goodid}_skolkovo'))
    if vidnoe == '0':
        mkp.add(types.InlineKeyboardButton('❌ Видное', callback_data=f'citygoods_{goodid}_vidnoe'))
    else:
        mkp.add(types.InlineKeyboardButton(f'✅ Видное | {vidnoe}', callback_data=f'citygoodsdel_{goodid}_vidnoe'))
    if sovhoz == '0':
        mkp.add(types.InlineKeyboardButton('❌ Совхоз Ленина', callback_data=f'citygoods_{goodid}_sovhoz'))
    else:
        mkp.add(types.InlineKeyboardButton(f'✅ Совхоз Ленина | {sovhoz}', callback_data=f'citygoodsdel_{goodid}_sovhoz'))
    if mitish == '0':
        mkp.add(types.InlineKeyboardButton('❌ Мытищи', callback_data=f'citygoods_{goodid}_miti'))
    else:
        mkp.add(types.InlineKeyboardButton(f'✅ Мытищи | {mitish}', callback_data=f'citygoodsdel_{goodid}_miti'))
    if domod == '0':
        mkp.add(types.InlineKeyboardButton('❌ Домодедово', callback_data=f'citygoods_{goodid}_domod'))
    else:
        mkp.add(types.InlineKeyboardButton(f'✅ Домодедово | {domod}', callback_data=f'citygoodsdel_{goodid}_domod'))
    if moscow == '0':
        mkp.add(types.InlineKeyboardButton('❌ Москва', callback_data=f'citygoods_{goodid}_moscow'))
    else:
        mkp.add(types.InlineKeyboardButton(f'✅ Москва | {pavelec}', callback_data=f'citygoodsdel_{goodid}_moscow'))
    if pavelec == '0':
        mkp.add(types.InlineKeyboardButton('❌ Павелецкая', callback_data=f'citygoods_{goodid}_pavelec'))
    else:
        mkp.add(types.InlineKeyboardButton(f'✅ Павелецкая | {pavelec}', callback_data=f'citygoodsdel_{goodid}_pavelec'))
    if visota == '0':
        mkp.add(types.InlineKeyboardButton('❌ Высота', callback_data=f'citygoods_{goodid}_visota'))
    else:
        mkp.add(types.InlineKeyboardButton(f'✅ Высота | {pavelec}', callback_data=f'citygoodsdel_{goodid}_visota'))
    mkp.add(types.InlineKeyboardButton('Админ-панель', callback_data='admin'))
    return mkp

def usermenu_mkp():
    mkp = types.InlineKeyboardMarkup(row_width=2)
    catlist = db.get_usercats()
    for cat in catlist:
        mkp.insert(types.InlineKeyboardButton(cat[1], callback_data=f'catuser_{cat[0]}'))
    return mkp

def usercatgoods_mkp(catid):
    subcatgoods_list = db.get_usercatgoods(catid)
    mkp = types.InlineKeyboardMarkup(row_width=2)
    for subcat in subcatgoods_list:
        if subcat[2] == 'good':
            mkp.insert(types.InlineKeyboardButton(subcat[1], callback_data=f'gooduser_{subcat[0]}'))
        else:
            mkp.insert(types.InlineKeyboardButton(subcat[1], callback_data=f'subcattuser_{subcat[0]}'))
    return mkp

def usersubcatgoods_mkp(subcatid):
    subcatgoods_list = db.get_usersubcatgoods(subcatid)
    mkp = types.InlineKeyboardMarkup(row_width=2)
    for subcat in subcatgoods_list:
        mkp.insert(types.InlineKeyboardButton(subcat[1], callback_data=f'gooduser_{subcat[0]}'))
    return mkp