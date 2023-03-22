import logging
import aiofiles
from MySQLdb import _mysql
from aiogram import Bot, Dispatcher, executor, types
from constants import *
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext

async def get_nested_keyboard(callback_query: types.CallbackQuery):
    code = callback_query.data
    db  = _mysql.connect(host="localhost", user=usr,
                        password=pswd, database=dbase)
    if code.startswith("back"):
        q = f"""SELECT DATA, btn_name, label, isParent FROM BUTTONS WHERE keyboardId=(SELECT keyboardId FROM BUTTONS WHERE ID=(SELECT parentId FROM BUTTONS WHERE btn_name = '{code}'));"""
    else:
        q = f"SELECT DATA, btn_name, label, isParent FROM BUTTONS WHERE parentId=(SELECT ID FROM BUTTONS WHERE btn_name='{code}')"
    db.query(q)
    results = db.store_result()
    results = results.fetch_row(maxrows=0, how=1)
    if len(results) == 0:
        # Regular button
        q = f"""SELECT command FROM BUTTONS WHERE btn_name = '{code}' LIMIT 1;"""
        db.query(q)
        results = db.store_result()
        results = results.fetch_row(maxrows=0, how=1)
        q = results[0]['command'].decode('utf-8')
        if q.startswith("SELECT"):
            db.close()
            answ = await get_data(q)
            await bot.send_message(callback_query.from_user.id, answ)
    else:
        # button to another keyboard
        keyboard = InlineKeyboardMarkup(row_width=2)
        for row in results:
            data = row['DATA'].decode('utf-8')
            btn_name = row['btn_name'].decode('utf-8')
            label = row['label'].decode('utf-8')
            button = InlineKeyboardButton(text=data, callback_data=btn_name)
            keyboard.add(button)
        await bot.send_message(callback_query.from_user.id, label, reply_markup=keyboard)
        db.close()
     
    
# Initial
logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp  = Dispatcher(bot)
dp.register_callback_query_handler(get_nested_keyboard)

async def get_start_keyboard(message: types.Message):
    await handle_user(str(message.from_user.id), message.from_user.username)   
    db  = _mysql.connect(host="localhost", user=usr,
                        password=pswd, database=dbase)    
    db.query("SELECT DATA, btn_name FROM BUTTONS WHERE keyboardId=0")
    result = db.store_result()
    keyboard = InlineKeyboardMarkup(row_width=2)
    for row in result.fetch_row(maxrows=0, how=1):
        data = row['DATA'].decode('utf-8')
        btn_name = row['btn_name'].decode('utf-8')
        button = InlineKeyboardButton(text=data, callback_data=btn_name)
        keyboard.add(button)
    return keyboard
    

@dp.message_handler(commands=['help'])
async def send_welcome(message: types.Message):
    msg = "Hi! I'm WishListBot!\nPowered by artkuc 😎\nHere are my commands:\n"
    await handle_user(str(message.from_user.id), message.from_user.username)
    answ = await get_column("""SELECT data FROM HELP""")
    for i in range(len(answ)):
        msg = msg + str(i + 1) + ") " + answ[i] + "\n" 
    await message.answer(msg)

@dp.message_handler(commands=['get_image'])
async def get_image(message: types.Message):
    # This handler function listens for the /get_image command and 
    # expects an image ID to be provided in the format /get_image <image_id>.
    await handle_user(str(message.from_user.id), message.from_user.username)
    try:
        image_id = int(message.text.split()[1])
    except IndexError:
        await message.answer("Please provide an image ID")
        return
    except ValueError:
        await message.answer("Invalid image ID")
        return
    path = await get_column(f"SELECT img_path FROM IMAGES WHERE ID = {image_id}")
    print(path)
    if len(path) == 0:
        await message.answer("Image not found")
        return
    async with aiofiles.open(path[0], 'rb') as f:
        photo_bytes = await f.read()
        await bot.send_photo(chat_id=message.from_user.id, photo=photo_bytes)
    # with open(path[0], 'rb') as f:
        # img = f.read()
    # await bot.send_photo(chat_id=message.from_user.id, photo=img)

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
            data = "NULL" if query_row[column] == None else str(query_row[column], "utf-8")
            str_row = str_row + column + ":" + data + " "
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
    keyboard = await get_start_keyboard(message)
    await message.answer("I'm not a chat bot:(\nUse buttons, please:", reply_markup=keyboard)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
