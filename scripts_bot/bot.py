import logging
from MySQLdb import _mysql
from aiogram import Bot, Dispatcher, executor, types
from constants import *

# Initial
logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp  = Dispatcher(bot)
db  = _mysql.connect(host="localhost", user=usr,
                     password=pswd, database=dbase)

@dp.message_handler(commands=['help'])
async def send_welcome(message: types.Message):
    res = "Hi! I'm WishListBot!\nPowered by artkuc 😎\nHere are my commands:\n"
    res = res + "1) /help - help itself\n"
    res = res + "2) /users - list all users\n"
    res = res + "3) /ideas - list all ideas\n"
    res = res + "4) /friends - list all friends\n"
    await message.reply(res)

async def get_data(query : str):
    str_res = ""
    db.query(query)
    query_res = db.store_result()
    query_res = query_res.fetch_row(maxrows=0, how = 1)
    i = 0
    for query_row in query_res:
        str_row = str(i + 1) + ") " 
        for column in query_row:
            str_row = str_row + column + ":" + str(query_row[column], "utf-8") + " "
        str_res = str_res + str_row + "\n"
        i = i + 1
    if str_res == "":
        str_res = "EMPTY"
    return str_res

@dp.message_handler(commands=['users'])
async def get_users(message: types.Message):
    answ = await get_data("""SELECT * FROM USERS""")
    await message.answer(answ)

@dp.message_handler(commands=['ideas'])
async def get_ideas(message: types.Message):
    answ = await get_data("""SELECT * FROM IDEAS""")
    await message.answer(answ)

@dp.message_handler(commands=['friends'])
async def get_friends(message: types.Message):
    answ = await get_data("""SELECT * FROM FRIENDS""")
    await message.answer(answ)

@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)       
