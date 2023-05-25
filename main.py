from config import dp
from aiogram.utils import executor

import admin
import start
import menu
import box





if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)