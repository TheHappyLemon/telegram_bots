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
    q = f"""SELECT label, command, status, onlyData FROM BUTTON_INF WHERE btn_id = (SELECT btn_inf FROM BUTTONS WHERE btn_name='{code}') LIMIT 1"""
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
        q = f"""SELECT DATA, btn_name, isParent FROM BUTTONS WHERE keyboardId=(SELECT keyboardId FROM BUTTONS WHERE ID=(SELECT parentId FROM BUTTONS WHERE btn_name = '{code}')) ORDER BY ordr ASC;"""
    else:
        q = f"SELECT DATA, btn_name, isParent FROM BUTTONS WHERE parentId=(SELECT ID FROM BUTTONS WHERE btn_name='{code}') ORDER BY ordr ASC"
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
                print(command)
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
            await bot.send_message(callback_query.from_user.id, command, parse_mode='MarkdownV2')
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
    await handle_user(message.from_user.id, message.from_user.username)   
    db  = _mysql.connect(host="localhost", user=usr,
                        password=pswd, database=dbase)    
    db.query("SELECT DATA, btn_name FROM BUTTONS WHERE keyboardId=0 ORDER BY ordr ASC")
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
    await handle_user(message.from_user.id, message.from_user.username)
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

async def handle_user(tg_id: int, name: str):
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
    await handle_user(message.from_user.id, message.from_user.username)
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
    await handle_user(message.from_user.id, message.from_user.username)
    answ = await get_column(f"SELECT sts_chat FROM USERS WHERE tg_id = {message.from_user.id}")
    if len(answ) == 0:
        await message.answer("No status, something went wrong\!", reply_markup=keyboard, parse_mode='MarkdownV2')
        return
    keyboard = None
    queries = []
    # IDEA BUTTON STATUSES
    if answ[0] == "IDEA_CRE":
        idea_name = await parse_msg(message.text.lower().strip(), force=True)
        query_get = f"SELECT id FROM IDEAS WHERE LOWER(name) = '{idea_name}' AND user_id = {message.from_user.id} AND sts <> 9 LIMIT 1;"
        answ = await get_column(query_get)
        if (len(answ)) == 0:
            queries.append(f"INSERT INTO IDEAS (user_id, name) VALUES ({message.from_user.id}, '{idea_name}');")
            queries.append(f"UPDATE USERS SET sts_chat = 'IDLE' WHERE tg_id = {message.from_user.id};")
            msg = f"Idea {idea_name} created\!"
        else:
            msg = f"You already have an idea named *{message.text}*\n\nChoose another *name*"
    elif answ[0] == "IDEA_DEL":
        idea_name = await parse_msg(message.text.lower().strip(), force=True)
        query_get = f"SELECT id FROM IDEAS WHERE LOWER(name) = '{idea_name}' AND user_id  = {message.from_user.id} AND sts <> 9 LIMIT 1;"
        answ = await get_column(query_get)
        if (len(answ)) == 0:
            msg = f"You do not have an idea named *{idea_name}*" 
        else:
            queries.append(f"UPDATE IDEAS set sts = 9 WHERE LOWER(name) = '{idea_name}' AND user_id = {message.from_user.id} LIMIT 1;")
            queries.append(f"UPDATE USERS SET sts_chat = 'IDLE' WHERE tg_id = {message.from_user.id};")
            msg = f"Idea *{idea_name}* deleted\!"
    # SETTINGS BUTTON STATUSES
    elif answ[0] == "ME_INP":
        name = await parse_msg(message.text.strip(), force=True)
        answ = await get_column(f"SELECT tg_id FROM USERS WHERE name = '{name}'")
        if len(answ) == 0:
            queries.append(f"UPDATE USERS SET name = '{name}' WHERE tg_id = {message.from_user.id};")
            queries.append(f"UPDATE USERS SET sts_chat = 'IDLE' WHERE tg_id = {message.from_user.id};")
            msg = f"Nice to meet you, *{name}*\!"
        else:
            msg = f"Username, *{name}* is already taken\!\nTry something else."
    # MODIFY IDEA BUTTON STATUSES
    elif answ[0] == "MODI_NME":
        pass
    elif answ[0] == "MODI_DES":
        pass
    elif answ[0] == "MODI_PRC":
        pass
    elif answ[0] == "MODI_ORI":
        pass
    # SET PRIVACY BUTTON STATUSES
    elif answ[0] == "ACCS_CHG":
        data = message.text.split()
        idea_name_out = await parse_msg(data[0], force=True)
        idea_name_in = data[0]
        query_get = f"SELECT ID FROM IDEAS WHERE name = '{idea_name_in}' LIMIT 1"
        answ = await get_column(query_get)
        if len(answ) == 0:
            msg = f"You do not have an idea named *{idea_name_out}*"
        else:
            acces = data[1].lower()
            if acces in accs_options:
                queries.append(f"UPDATE IDEAS SET isPublic = {accs_options[acces]} WHERE id = {answ[0]}")
                queries.append(f"UPDATE USERS SET sts_chat = 'IDLE' WHERE tg_id = {message.from_user.id};")
                msg = f"Acces changed\!\nIdea *{idea_name_out}* is now *{acces}*"
            else:
                msg = f"Bad input in *{acces}*"
    elif answ[0] == "ACCS_RMV":
        pass
    elif answ[0] == "ACCS_SEE":
        # not tested
        idea_name_out = await parse_msg(message.text.lower().strip(), force=True)
        idea_name_in  = message.text.lower().strip()
        query_get = f"SELECT isPublic FROM IDEAS WHERE user_id = {message.from_user.id} AND LOWER(name) = '{idea_name_in}'"
        answ = await get_column(query_get)
        if len(answ) == 0:
            msg = f"You do not have an idea named *{idea_name_out}*"
        else:
            if answ[0] == "1":
                msg = f"Idea is *public*\.\n*Everyone* can see it\."
            else:
                msg = f"Idea is *private*\. Only following friends can see it:\n"
                query_get = f"""SELECT tg_id, name from USERS 
                    WHERE tg_id IN (SELECT friend_id FROM FRIENDS WHERE user_id = {message.from_user.id}) AND 
                    tg_id NOT IN (SELECT user_id FROM IDEAS_INF WHERE idea_id = 
                    (SELECT id FROM IDEAS WHERE user_id = {message.from_user.id} AND LOWER(name) = '{idea_name_in}'));"""
                answ = await get_data(query_get)
                msg = msg + answ
                queries.append(f"UPDATE USERS SET sts_chat = 'IDLE' WHERE tg_id = {message.from_user.id};")
    # FRIENDS BUTTON STATUSES
    elif answ[0] == "FRND_ADD":
        friend_name_in  = message.text.strip()
        friend_name_out = await parse_msg(message.text.strip(), force=True)
        query_get = f"SELECT tg_id FROM USERS WHERE name = '{friend_name_in}' LIMIT 1"
        answ = await get_column(query_get)
        if len(answ) == 0:
            msg = f"User with name *{friend_name_out}* does not exist"
        else:
            friend_id = answ[0]
            query_get = f"SELECT user_id FROM FRIENDS WHERE (user_id = {message.from_user.id} AND friend_id = {friend_id}) OR (user_id = {friend_id} AND friend_id = {message.from_user.id})"
            answ = await get_column(query_get)
            if len(answ) == 0:
                queries.append(f"UPDATE USERS SET sts_chat = 'IDLE' WHERE tg_id = {message.from_user.id};")
                query_get = f"SELECT sts FROM FR_REQUESTS WHERE user_from = {message.from_user.id} AND user_to = {friend_id}"
                answ = await get_column(query_get)
                if len(answ) == 0:
                    queries.append(f"INSERT INTO FR_REQUESTS (user_from, user_to) VALUE ({message.from_user.id}, {friend_id})")
                    msg = f"Request was sent to *{friend_name_out}* succesfully\!"
                else:
                    if answ[0] == "0":
                        msg = f"User *{friend_name_out}* still have not answered to your previous request\!"
                    elif answ[0] == "5":
                        queries.append(f"UPDATE FR_REQUESTS SET sts = 0 WHERE (user_from = {message.from_user.id} AND user_to = {friend_id})")
                        msg = f"User *{friend_name_out}* rejected your previous request\!\nBut another one is sent succesfully\!"
            else:
                msg = f"You and user *{friend_name_out}* are already friends\!"
    elif answ[0] == "FRND_RMV":
        # check if such user exists
        friend_name_in  = message.text.strip()
        friend_name_out = await parse_msg(message.text.strip(), force=True)
        query_get = f"SELECT tg_id FROM USERS WHERE name = '{friend_name_in}' LIMIT 1"
        answ = await get_column(query_get)
        if len(answ) == 0:
            msg = f"User with name *{friend_name_out}* does not exist\!"
        else:
            query_get = f"SELECT user_id, friend_id FROM FRIENDS WHERE (user_id = {message.from_user.id} AND friend_id = {answ[0]}) OR (user_id = {answ[0]} AND friend_id = {message.from_user.id})"
            db  = _mysql.connect(host="localhost", user=usr,
                        password=pswd, database=dbase)  
            db.query(query_get)
            query_res = db.store_result()
            query_res = query_res.fetch_row(maxrows=0, how=1)
            if len(query_res) == 0:
                msg = f"You arent friends with *{friend_name_out}* anyways\!"
            else:
                for row in query_res:
                    usr_id = str(row['user_id']  , "utf-8")
                    frd_id = str(row['friend_id'], "utf-8")
                    queries.append(f"DELETE FROM FRIENDS WHERE user_id = {usr_id} AND friend_id = {frd_id}")
                queries.append(f"UPDATE USERS SET sts_chat = 'IDLE' WHERE tg_id = {message.from_user.id};")
                msg = f"You and user *{friend_name_out}* are not friends anymore\!"
    # MY REQUESTS BUTTON STATUSES
    elif answ[0] == "FRND_ACC" or answ[0] == "FRND_REJ":
        friend_name_in  = message.text.strip()
        friend_name_out = await parse_msg(message.text.strip(), force=True)
        query_get = f"SELECT tg_id FROM USERS WHERE name = '{friend_name_in}' LIMIT 1"
        answ_1 = await get_column(query_get)
        if len(answ_1) == 0:
            msg = f"User *{friend_name_out}* does not exist\!"
        else:
            friend_id = answ_1[0]
            query_get = f"SELECT sts FROM FR_REQUESTS WHERE user_to = {message.from_user.id} AND user_from = {friend_id} LIMIT 1"
            answ_1 = await get_column(query_get)
            if len(answ_1) == 0 or answ_1[0] != "0":
                msg = f"You do not have a request from user  *{friend_name_out}* \!"
            else:
                queries.append(f"UPDATE USERS SET sts_chat = 'IDLE' WHERE tg_id = {message.from_user.id};")
                if answ[0] == "FRND_ACC":
                    queries.append(f"INSERT INTO FRIENDS(user_id, friend_id) VALUES({message.from_user.id}, {friend_id})")
                    queries.append(f"DELETE FROM FR_REQUESTS WHERE (user_to = {message.from_user.id} AND user_from = {friend_id})")
                    msg = f"Request *ACCEPTED*\!\nYou and user *{friend_name_out}* are friends now\!"
                elif answ[0] == "FRND_REJ":
                    queries.append(f"UPDATE FR_REQUESTS SET sts = 5 WHERE (user_to = {message.from_user.id} AND user_from = {friend_id})")
                    msg = f"Request *REJECTED*"
    # DEFAULT STATUS HANDLER
    elif answ[0] == "IDLE":
        keyboard = await get_start_keyboard(message)
        #msg = "Type following: *idea_name*"
        msg = ("I'm not a chat bot:\(\nUse *buttons*, please:")
    else:
        msg = await parse_msg("This function is currently *under construction*\nOur engineers are woorking *as hard as possible*, to get this thing going")
    print('msg: ', msg)
    await message.answer(msg, reply_markup=keyboard, parse_mode='MarkdownV2')
    i = 0
    print()
    for q in queries:
        print(i + 1, q)
        i = i + 1
    print()
    await insert_data(queries)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
