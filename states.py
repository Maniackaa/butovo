from aiogram.dispatcher.filters.state import State, StatesGroup

class AddCat(StatesGroup):
    CatName = State()

class AddGood(StatesGroup):
    CatId = State()
    Name = State()
    Desc = State()
    Price = State()
    Photo = State()

class AddCityGood(StatesGroup):
    GoodId = State()
    City = State()

class AddSubCat(StatesGroup):
    CatId = State()
    Name = State()

class AddSubGood(StatesGroup):
    SubcatId = State()
    Name = State()
    Desc = State()
    Price = State()
    Photo = State()

class OformOrder(StatesGroup):
    Name = State()
    Phone = State()
    Time = State()
    Delivery = State()
    Pays = State()