import logging
import pathlib
from MySQLdb import _mysql
from aiogram import Bot, Dispatcher, executor, types
from constants import *

# Initial
logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp  = Dispatcher(bot)

@dp.message_handler(commands=['help'])
async def send_welcome(message: types.Message):
    res = "Hi! I'm WishListBot!\nPowered by artkuc 😎\nHere are my commands:\n"
    res = res + "1) /help - help itself\n"
    res = res + "2) /users - list all users\n"
    res = res + "3) /ideas - list all ideas\n"
    res = res + "4) /friends - list all friends\n"
    await message.reply(res)

async def get_data(query : str):  
    db  = _mysql.connect(host="localhost", user=usr,
                        password=pswd, database=dbase)
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
    db.close()
    return str_res

async def get_column(query : str):  
    db  = _mysql.connect(host="localhost", user=usr,
                        password=pswd, database=dbase)
    db.query(query)
    query_res = db.store_result()
    query_res = query_res.fetch_row(maxrows=0, how = 1)
    print(query_res)
    i = 0
    list_res = []
    for query_row in query_res:
        for column in query_row:
            list_res.append(str(query_row[column], "utf-8"))
    db.close()
    return list_res

async def insert_data(query : str):
    db  = _mysql.connect(host="localhost", user=usr,
                        password=pswd, database=dbase)   
    db.query(query)
    db.commit()  # commit the changes made to the database
    db.close() 

async def handle_user(tg_id: str, name: str):
    answ = await get_data(f"SELECT * FROM USERS WHERE tg_id = {tg_id} LIMIT 1;")
    if answ == "EMPTY":
        await insert_data(f"INSERT INTO USERS (tg_id, name, sts) VALUES ({tg_id}, '{name}', 0);")

@dp.message_handler(commands=['users'])
async def get_users(message: types.Message):
    await handle_user(str(message.from_user.id), message.from_user.username)
    answ = await get_data("""SELECT * FROM USERS""")
    await message.answer(answ)

@dp.message_handler(commands=['ideas'])
async def get_ideas(message: types.Message):
    await handle_user(str(message.from_user.id), message.from_user.username)
    answ = await get_data("""SELECT * FROM IDEAS""")
    await message.answer(answ)

@dp.message_handler(commands=['friends'])
async def get_friends(message: types.Message):
    await handle_user(str(message.from_user.id), message.from_user.username)
    answ = await get_data("""SELECT * FROM FRIENDS""")
    await message.answer(answ)

@dp.message_handler(commands=['me'])
async def get_me(message: types.Message):
    tg_id = str(message.from_user.id)
    await handle_user(str(message.from_user.id), message.from_user.username)
    answ = await get_data(f"SELECT ID, name FROM USERS WHERE tg_id = {tg_id} LIMIT 1;")
    await message.answer(answ)

@dp.message_handler(content_types=types.ContentType.PHOTO)
async def get_img(message: types.Message):
    tg_id = str(message.from_user.id)
    await handle_user(str(message.from_user.id), message.from_user.username)
    answ = await get_column("SELECT ID FROM IMAGES ORDER BY ID DESC LIMIT 1;")
    if len(answ) == 0:
        answ = "1"
    else:
        answ = str(int(answ[0]) + 1)
    print("new id for image:", answ)
    photo = message.photo[-1]
    path = photos + answ + ext
    await photo.download(destination_file=path)
    # At this point I just hope that photo was downloaded correctly, because
    # I dont know how to check it asynchronously
    # INSERT INTO IMAGES (path) VALUES ('/path/to/image.jpg');
    await insert_data(f"INSERT INTO IMAGES (img_path, idea_id) VALUES ('{path}', 1);")

@dp.message_handler()
async def echo(message: types.Message):
    print(type(message.from_user.id))
    print(message.from_user.id)
    await message.answer(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
