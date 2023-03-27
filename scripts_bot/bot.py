import logging
import aiofiles
from MySQLdb import _mysql
from aiogram import Bot, Dispatcher, executor, types
from constants import *
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

async def get_nested_keyboard(callback_query: types.CallbackQuery):
    code = callback_query.data
    db  = _mysql.connect(host="localhost", user=usr,
                        password=pswd, database=dbase)
    await reset_status(str(callback_query.from_user.id))
    print(code, "pressed")
    # Get label to write
    q = f"""SELECT label, command, status, onlyData FROM BUTTON_INF WHERE ID = (SELECT btn_inf FROM BUTTONS WHERE btn_name='{code}') LIMIT 1"""
    print(q)
    db.query(q)
    results = db.store_result()
    results = results.fetch_row(maxrows=0, how=1)
    print(results)
    label = results[0]['label']
    command = results[0]['command']
    status = results[0]['status']
    onlyData = results[0]['onlyData']
    if label != None:
        label = label.decode('utf-8')    
    if command != None:
        command = command.decode('utf-8')
    if status != None:
        status = status.decode('utf-8')
    if onlyData != None:
        onlyData = onlyData.decode('utf-8')  
    if onlyData == "1":
        onlyData = True
    else:
        onlyData = False 
    print(command)
    # Get keyboard
    if code.startswith("back"):
        q = f"""SELECT DATA, btn_name, isParent FROM BUTTONS WHERE keyboardId=(SELECT keyboardId FROM BUTTONS WHERE ID=(SELECT parentId FROM BUTTONS WHERE btn_name = '{code}'));"""
    else:
        q = f"SELECT DATA, btn_name, isParent FROM BUTTONS WHERE parentId=(SELECT ID FROM BUTTONS WHERE btn_name='{code}')"
    db.query(q)
    results = db.store_result()
    results = results.fetch_row(maxrows=0, how=1)
    print()
    print(results)
    if len(results) == 0:
        # if it is a Regular button
        if command.startswith("SELECT"):
            if status != None:
                pos = command.find(param)
                print(status)
                status = status.split(",")
                print(status)
                i = 0
                tmp = ""
                while pos > 0:
                    if status[i] == 'tg_id':
                        tmp = str(callback_query.from_user.id)
                    command = command.replace(param, tmp, 1)
                    pos = command.find(param)
                    i = i + 1
            db.close()
            answ = await get_data(command, onlyData)
            print(answ)
            await bot.send_message(callback_query.from_user.id, answ, parse_mode='MarkdownV2')
        else:
            # handle special commands with statuses
            print(command)
            queries = []
            queries.append(f"UPDATE USERS SET sts_chat = '{status}' WHERE tg_id = {callback_query.from_user.id};")
            await insert_data(queries)
            await bot.send_message(callback_query.from_user.id, command)

            print(command, status)
    else:
        # button to another keyboard
        print("keeeeeeeeeek")
        keyboard = InlineKeyboardMarkup(row_width=2)
        for row in results:
            data = row['DATA'].decode('utf-8')
            btn_name = row['btn_name'].decode('utf-8')
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
    
@dp.message_handler(commands=['get_image'])
async def get_image(message: types.Message):
    # This handler function listens for the /get_image command and 
    # expects an image ID to be provided in the format /get_image <image_id>.
    await handle_user(str(message.from_user.id), message.from_user.username)
    try:
        image_id = int(message.text.split()[1])
    except IndexError:
        await message.answer("Please provide an image *ID*", parse_mode='MarkdownV2')
        return
    except ValueError:
        await message.answer("Invalid image *ID*", parse_mode='MarkdownV2')
        return
    path = await get_column(f"SELECT img_path FROM IMAGES WHERE ID = {image_id}")
    print(path)
    if len(path) == 0:
        await message.answer("Image *not found*", parse_mode='MarkdownV2')
        return
    async with aiofiles.open(path[0], 'rb') as f:
        photo_bytes = await f.read()
        await bot.send_photo(chat_id=message.from_user.id, photo=photo_bytes)
    # with open(path[0], 'rb') as f:
        # img = f.read()
    # await bot.send_photo(chat_id=message.from_user.id, photo=img)

async def get_data(query : str, onlyData : bool = False):  
    db  = _mysql.connect(host="localhost", user=usr,
                        password=pswd, database=dbase)
    str_res = ""
    db.query(query)
    query_res = db.store_result()
    query_res = query_res.fetch_row(maxrows=0, how = 1)
    i = 0
    for query_row in query_res:
        str_row = str(i + 1) + "\) "
        for column in query_row:
            data = "NULL" if query_row[column] == None else str(query_row[column], "utf-8")
            data = await parse_msg(data, True)
            if not onlyData:
                str_row = str_row + "*" + await parse_msg(column, True) + "*" + " : "
            str_row = str_row + data + " "
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

async def insert_data(queries : list):
    db  = _mysql.connect(host="localhost", user=usr,
                        password=pswd, database=dbase)   
    for query in queries:
        print("executing", query)
        db.query(query)
    db.commit()  # commit the changes made to the database
    db.close() 

async def handle_user(tg_id: str, name: str):
    answ = await get_data(f"SELECT * FROM USERS WHERE tg_id = {tg_id} LIMIT 1;")
    if answ == "EMPTY":
        queries = []
        queries.append(f"INSERT INTO USERS (tg_id, name) VALUES ({tg_id}, '{name}');")
        await insert_data(queries)

async def reset_status(tg_id: str):
    answ = await get_column(f"SELECT sts_chat FROM USERS WHERE tg_id = {tg_id} LIMIT 1;")
    if len(answ) == 0:
        print("NO STATUS")
    elif answ[0] != "IDLE":
        queries = []
        queries.append(f"UPDATE USERS SET sts_chat = 'IDLE' WHERE tg_id = {tg_id};")
        await insert_data(queries)
        
    

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
    queries = []
    queries.append(f"INSERT INTO IMAGES (img_path, idea_id) VALUES ('{path}', 1);")    
    await insert_data(queries)

async def parse_msg(msg : str, force : bool = False):
    if force:
        for char in Markdown2_ch_all:
            msg = msg.replace(char, '\\' + char)
    else:
        for char in Markdown2_ch:
            msg = msg.replace(char, '\\' + char)
    return msg


@dp.message_handler()
async def echo(message: types.Message):
    await handle_user(str(message.from_user.id), message.from_user.username)
    answ = await get_column(f"SELECT sts_chat FROM USERS WHERE tg_id = {message.from_user.id}")
    if len(answ) == 0:
        await message.answer("No status, something went wrong\!", reply_markup=keyboard, parse_mode='MarkdownV2')
        return
    keyboard = None
    queries = []
    if answ[0] == "IDEA_CRE":
        query_get = f"SELECT id FROM IDEAS WHERE LOWER(name) = '{message.text.lower()}' AND user_id  = (SELECT ID FROM USERS WHERE tg_id = {message.from_user.id} AND sts <> 9 LIMIT 1);"
        answ = await get_column(query_get)
        if (len(answ)) == 0:
            queries.append(f"INSERT INTO IDEAS (user_id, name) VALUES ((SELECT ID FROM USERS WHERE tg_id = {message.from_user.id} LIMIT 1), '{message.text}');")
            queries.append(f"UPDATE USERS SET sts_chat = 'IDLE' WHERE tg_id = {message.from_user.id};")
            msg = f"Idea {message.text} created\!"
        else:
            msg = f"You already have an idea named *{message.text}*\n\nChoose another *name*"
    elif answ[0] == "IDEA_MOD":
        pass
    elif answ[0] == "IDEA_DEL":
        query_get = f"SELECT id FROM IDEAS WHERE LOWER(name) = '{message.text.lower()}' AND user_id  = (SELECT ID FROM USERS WHERE tg_id = {message.from_user.id} AND sts <> 9 LIMIT 1);"
        answ = await get_column(query_get)
        if (len(answ)) == 0:
            msg = f"You do not have an idea named *{message.text}*" 
        else:
            queries.append(f"UPDATE IDEAS set sts = 9 WHERE LOWER(name) = '{message.text.lower()}' AND user_id  = (SELECT ID FROM USERS WHERE tg_id = {message.from_user.id} LIMIT 1);")
            queries.append(f"UPDATE USERS SET sts_chat = 'IDLE' WHERE tg_id = {message.from_user.id};")
            msg = f"Idea *{message.text}* deleted\!"
    elif answ[0] == "ME_INP":
        queries.append(f"UPDATE USERS SET name = '{message.text}' WHERE tg_id = {message.from_user.id};")
        queries.append(f"UPDATE USERS SET sts_chat = 'IDLE' WHERE tg_id = {message.from_user.id};")
        msg = f"Nice to meet you, *{message.text}*\!"
    elif answ[0] == "IDLE":
        keyboard = await get_start_keyboard(message)
        msg = ("I'm not a chat bot:\(\nUse *buttons*, please:")
    else:
        msg = await parse_msg("This function is currently *under construction*\nOur engineers are woorking *as hard as possible*, to get this thing going")
    await message.answer(msg, reply_markup=keyboard, parse_mode='MarkdownV2')
    i = 0
    print()
    for q in queries:
        print(i + 1, q)
        i = i + 1
    print()
    await insert_data(queries)
    #if answ[0] != "IDLE":
        #await insert_data(queries)
        #await message.answer(msg, parse_mode='MarkdownV2')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
