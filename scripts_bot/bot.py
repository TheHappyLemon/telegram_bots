import logging
import aiofiles
from MySQLdb import _mysql
from aiogram import Bot, Dispatcher, executor, types
from constants import *
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from prettytable import PrettyTable

async def handle_sub_query(callback_query : types.CallbackQuery, query : str, onlyData = False):
    db = _mysql.connect(host="localhost", user=usr,
                        password=pswd, database=dbase)
    db.query(query)
    query_res = db.store_result()
    query_res = query_res.fetch_row(maxrows=0, how=1)
    print("\nrec1")
    for row in query_res:
        command = str(row['sub_query'], "utf-8")
        print("\nrec1. command = ", command)
        if command.startswith("SELECT IF"):
            # recursion
            await handle_sub_query(callback_query, command, onlyData)
        elif command.startswith("SELECT"):
            # terminal 
            answ = await get_data(command, onlyData)
            await bot.send_message(callback_query.from_user.id, answ)
        else:
            await bot.send_message(callback_query.from_user.id, command, parse_mode='MarkdownV2')

async def get_custom_column(tg_id : int, column : str = 'last_input'):
    query_get = f"SELECT {column} FROM USERS WHERE tg_id = {tg_id}"
    idea_name = await get_column(query_get)
    idea_name = idea_name[0]
    return idea_name

async def parse_command(callback_query: types.CallbackQuery, command : str, status_out : str):
    if status_out != None:
        pos = command.find(param)
        status_out = status_out.split(",")
        i = 0
        tmp = ""
        while pos > 0:
            if status_out[i] == 'tg_id':
                tmp = str(callback_query.from_user.id)
            elif status_out[i] == 'last_input':
                tmp = await get_column(f"SELECT last_input FROM USERS WHERE tg_id = {callback_query.from_user.id} LIMIT 1")
                tmp = tmp[0]
            command = command.replace(param, tmp, 1)
            pos = command.find(param)
            i = i + 1
    return command

async def get_nested_keyboard(callback_query: types.CallbackQuery):
    try:
        code = callback_query.data
        db = _mysql.connect(host="localhost", user=usr,
                            password=pswd, database=dbase)
        await reset_status(str(callback_query.from_user.id))
        #await reset_last_input(code)
        print(code, "pressed")
        # Get label to write
        q = f"""SELECT label, command, status_inp, status_out, onlyData FROM BUTTON_INF WHERE btn_id = (SELECT btn_inf FROM BUTTONS WHERE btn_name='{code}') LIMIT 1"""
        print(q)
        db.query(q)
        results = db.store_result()
        results = results.fetch_row(maxrows=0, how=1)
        print(results)
        label = results[0]['label']
        command = results[0]['command']
        status_inp = results[0]['status_inp']
        status_out = results[0]['status_out']
        onlyData = results[0]['onlyData']
        if label != None:
            label = label.decode('utf-8')
        if command != None:
            command = command.decode('utf-8')
        if status_inp != None:
            status_inp = status_inp.decode('utf-8')
        if status_out != None:
            status_out = status_out.decode('utf-8')
        if onlyData != None:
            onlyData = onlyData.decode('utf-8')
        if onlyData == "1":
            onlyData = True
        else:
            onlyData = False
        print(f"\ncommand = {command}\n")
        # Get keyboard
        if code.startswith("back"):
            q = f"""SELECT DATA, btn_name, isParent FROM BUTTONS WHERE keyboardId=(SELECT keyboardId FROM BUTTONS WHERE ID=(SELECT parentId FROM BUTTONS WHERE btn_name = '{code}')) ORDER BY ordr ASC;"""
        else:
            q = f"SELECT DATA, btn_name, isParent FROM BUTTONS WHERE parentId=(SELECT ID FROM BUTTONS WHERE btn_name='{code}') ORDER BY ordr ASC"
        db.query(q)
        results = db.store_result()
        results = results.fetch_row(maxrows=0, how=1)
        db.close()
        print(f"\nbutton {code} children = {results}\n")
        queries = []
        if len(results) == 0:
            # if it is a Regular button
            command = await parse_command(callback_query, command, status_out)
            print('\n', "command = ", command)
            if command.startswith("SELECT IF"):
                await handle_sub_query(callback_query, command)
            elif command.startswith("SELECT"):
                answ = await get_data(command, onlyData)
                print("\nreceived:")
                print(answ)
                #await bot.send_message(callback_query.from_user.id, answ)
                await bot.send_message(callback_query.from_user.id, answ, parse_mode='MarkdownV2')
            else:
                # handle special commands with statuses
                queries.append(f"UPDATE USERS SET sts_chat = '{status_inp}' WHERE tg_id = {callback_query.from_user.id};")
                await insert_data(queries)
                await bot.send_message(callback_query.from_user.id, command, parse_mode='MarkdownV2')
        else:
            # button to another keyboard
            if status_inp != None:
                queries.append(f"UPDATE USERS SET sts_chat = '{status_inp}' WHERE tg_id = {callback_query.from_user.id};")
                await insert_data(queries)
                await bot.send_message(callback_query.from_user.id, command, parse_mode='MarkdownV2')
            else:
                if command != None:
                    # Reset last input on back button
                    command = await parse_command(callback_query, command, status_out)
                    queries = []
                    if command.startswith("UPDATE"):
                        queries.append(command)
                        await insert_data(queries)
                keyboard = InlineKeyboardMarkup(row_width=2)
                for row in results:
                    data = row['DATA'].decode('utf-8')
                    btn_name = row['btn_name'].decode('utf-8')
                    button = InlineKeyboardButton(text=data, callback_data=btn_name)
                    keyboard.add(button)
                await bot.send_message(callback_query.from_user.id, label, reply_markup=keyboard)
    except Exception as e:
        await bot.send_message(callback_query.from_user.id, f"An error occured when handling your request!\nError message: {str(e)}\n\nContact an adminitrator :)")
            

# Initial
logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
dp.register_callback_query_handler(get_nested_keyboard)

async def get_keyboard(message: types.Message, keyboardId : int = 0):
    await handle_user(message.from_user.id, message.from_user.username)
    db = _mysql.connect(host="localhost", user=usr,
                        password=pswd, database=dbase)
    db.query(f"SELECT DATA, btn_name FROM BUTTONS WHERE keyboardId={keyboardId} ORDER BY ordr ASC")
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

async def get_data(query: str, onlyData: bool = False):
    db = _mysql.connect(host="localhost", user=usr,
                        password=pswd, database=dbase)
    db.query(query)
    query_res = db.store_result()
    query_res = query_res.fetch_row(maxrows=0, how=1)
    table = PrettyTable()
    result_dict = {}
    # make a dict where key is every column from query and value is list of all values from all rows
    for key in query_res[0].keys():
        result_dict[key] = ["Empty" if d[key] == None else str(d[key], 'utf-8') for d in query_res]
    # add each column with values to prettytable
    for column in result_dict:
        table.add_column(column, result_dict[column])
    table.align = "l"
    table_string = table.get_string()
    # add code blocks, so telegram does not lose formatting.
    table_string = "```\n" + table_string + "\n```"
    return table_string


# async def get_data(query: str, onlyData: bool = False):
#     db = _mysql.connect(host="localhost", user=usr,
#                         password=pswd, database=dbase)
#     str_res = ""
#     db.query(query)
#     query_res = db.store_result()
#     query_res = query_res.fetch_row(maxrows=0, how=1)
#     i = 0
#     for query_row in query_res:
#         str_row = str(i + 1) + "\) "
#         for column in query_row:
#             data = "NULL" if query_row[column] == None else str(
#                 query_row[column], "utf-8")
#             data = await parse_msg(data, True, True)
#             if not onlyData:
#                 str_row = str_row + "*" + await parse_msg(column, True, True) + "*" + " : "
#             str_row = str_row + data + " "
#         str_res = str_res + str_row + "\n"
#         i = i + 1
#     if str_res == "":
#         str_res = "EMPTY"
#     db.close()
#     return str_res


async def get_column(query: str):
    db = _mysql.connect(host="localhost", user=usr,
                        password=pswd, database=dbase)
    db.query(query)
    query_res = db.store_result()
    query_res = query_res.fetch_row(maxrows=0, how=1)
    i = 0
    list_res = []
    for query_row in query_res:
        for column in query_row:
            list_res.append(str(query_row[column], "utf-8"))
    db.close()
    return list_res


async def insert_data(queries: list):
    db = _mysql.connect(host="localhost", user=usr,
                        password=pswd, database=dbase)
    for query in queries:
        print("executing", query)
        db.query(query)
    db.commit()  # commit the changes made to the database
    db.close()


async def handle_user(tg_id: int, name: str):
    answ = await get_column(f"SELECT tg_id FROM USERS WHERE tg_id = {tg_id} LIMIT 1;")
    if len(answ) == 0:
        queries = []
        queries.append(
            f"INSERT INTO USERS (tg_id, name) VALUES ({tg_id}, '{name}');")
        await insert_data(queries)


async def reset_status(tg_id: str):
    answ = await get_column(f"SELECT sts_chat FROM USERS WHERE tg_id = {tg_id} LIMIT 1;")
    if len(answ) == 0:
        print("NO STATUS")
    elif answ[0] != "IDLE":
        queries = []
        queries.append(
            f"UPDATE USERS SET sts_chat = 'IDLE' WHERE tg_id = {tg_id};")
        await insert_data(queries)

#async def reset_last_input(code : str):


@dp.message_handler(content_types=types.ContentType.PHOTO)
async def save_img(message: types.Message):
    await handle_user(message.from_user.id, message.from_user.username)
    answ = await get_column(f"SELECT sts_chat FROM USERS WHERE tg_id = {message.from_user.id}")
    img_name = await get_custom_column(message.from_user.id, column='img_name')
    img_name_out = await parse_msg(img_name, force = True)
    if answ[0] == "IMAG_IMG":
        idea_name = await get_custom_column(message.from_user.id)
        query_get = f"SELECT id FROM IDEAS WHERE user_id = {message.from_user.id} AND name = '{idea_name}'"
        idea_id   = await get_column(query_get)
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
        queries = []
        queries.append(
            f"INSERT INTO IMAGES (img_path, idea_id, name) VALUES ('{path}', {idea_id[0]}, '{img_name}');")
        queries.append(
            f"UPDATE USERS SET sts_chat = 'IDLE' WHERE tg_id = {message.from_user.id};")
        queries.append(
            f"UPDATE USERS SET img_name = NULL WHERE tg_id = {message.from_user.id};")
        await insert_data(queries)
        print(f"Image *{img_name_out}* saved succesfully\!")
        msg = f"Image *{img_name_out}* saved succesfully\!"
    else:
        msg = "To save an image go to *Idea \- Modify Idea \- Manage images \- Add image*"    
    print(msg)
    await bot.send_message(message.from_user.id, msg , parse_mode='MarkdownV2')


async def parse_msg(msg: str, force: bool = False, slash: bool = False):
    if slash:
        # escapes slash with a slash
        msg = msg.replace('\\', '\\\\')
    if force:
        for char in Markdown2_ch_all:
            msg = msg.replace(char, '\\' + char)
    else:
        for char in Markdown2_ch:
            msg = msg.replace(char, '\\' + char)
    return msg


@dp.message_handler()
async def echo(message: types.Message):
    try:
        await handle_user(message.from_user.id, message.from_user.username)
        answ = await get_column(f"SELECT sts_chat FROM USERS WHERE tg_id = {message.from_user.id}")
        if len(answ) == 0:
            await message.answer("No status, something went wrong\!", reply_markup=keyboard, parse_mode='MarkdownV2')
            return
        keyboard = None
        queries = []
        # IDEA BUTTON STATUSES
        if answ[0] == "IDEA_CRE":
            idea_name_out = await parse_msg(message.text.lower().strip(), force=True)
            idea_name_in  = message.text.lower().strip()
            query_get = f"SELECT id FROM IDEAS WHERE LOWER(name) = '{idea_name_in}' AND user_id = {message.from_user.id} AND sts <> 9 LIMIT 1;"
            answ = await get_column(query_get)
            if (len(answ)) == 0:
                queries.append(
                    f"INSERT INTO IDEAS (user_id, name) VALUES ({message.from_user.id}, '{idea_name_in}');")
                queries.append(
                    f"UPDATE USERS SET sts_chat = 'IDLE' WHERE tg_id = {message.from_user.id};")
                msg = f"Idea *{idea_name_out}* created\!"
            else:
                msg = f"You already have an idea named *{message.text}*\n\nChoose another *name*"
        elif answ[0] == "IDEA_MOD":
            idea_name_out = await parse_msg(message.text.lower().strip(), force=True)
            idea_name_in  = message.text.lower().strip()
            query_get = f"SELECT name FROM IDEAS WHERE LOWER(name) = '{idea_name_in}' AND user_id  = {message.from_user.id} AND sts <> 9 LIMIT 1;"
            answ = await get_column(query_get)
            if len(answ) == 0:
                msg = f"You do not have an idea named *{idea_name_out}*"
            else:
                queries.append(
                    f"UPDATE USERS SET last_input = '{answ[0]}' WHERE tg_id = {message.from_user.id};")
                queries.append(
                    f"UPDATE USERS SET sts_chat = 'IDLE' WHERE tg_id = {message.from_user.id};")
                msg = f"Idea *{idea_name_out}* is choosen to be modified\!"        
                keyboard = await get_keyboard(message=message, keyboardId=4)
        elif answ[0] == "IDEA_DEL":
            idea_name_out = await parse_msg(message.text.lower().strip(), force=True)
            idea_name_in  = message.text.lower().strip()
            query_get = f"SELECT id FROM IDEAS WHERE LOWER(name) = '{idea_name_in}' AND user_id  = {message.from_user.id} AND sts <> 9 LIMIT 1;"
            answ = await get_column(query_get)
            if (len(answ)) == 0:
                msg = f"You do not have an idea named *{idea_name_out}*"
            else:
                queries.append(
                    f"UPDATE IDEAS set sts = 9 WHERE LOWER(name) = '{idea_name_in}' AND user_id = {message.from_user.id} LIMIT 1;")
                queries.append(
                    f"UPDATE USERS SET sts_chat = 'IDLE' WHERE tg_id = {message.from_user.id};")
                msg = f"Idea *{idea_name_out}* deleted\!"
        # SETTINGS BUTTON STATUSES
        elif answ[0] == "ME_INP":
            name_out = await parse_msg(message.text.strip(), force=True)
            name_in = message.text.strip()
            answ = await get_column(f"SELECT tg_id FROM USERS WHERE name = '{name_in}'")
            if len(answ) == 0:
                queries.append(
                    f"UPDATE USERS SET name = '{name_in}' WHERE tg_id = {message.from_user.id};")
                queries.append(
                    f"UPDATE USERS SET sts_chat = 'IDLE' WHERE tg_id = {message.from_user.id};")
                msg = f"Nice to meet you, *{name_out}*\!"
            else:
                msg = f"Username, *{name_in}* is already taken\!\nTry something else."
        # MODIFY IDEA BUTTON STATUSES
        elif answ[0] == "MODI_NME":
            idea_new_name_in  = message.text.strip().lower()
            idea_new_name_out = await parse_msg(idea_name_in, force=True)
            idea_name = await get_custom_column(message.from_user.id)
            query_get = f"SELECT id FROM IDEAS WHERE LOWER(name) = '{idea_new_name_in}' AND user_id  = {message.from_user.id} AND sts <> 9 LIMIT 1;"
            answ = await get_column(query_get)
            if len(answ) == 0:
                queries.append(
                    f"UPDATE IDEAS set name = '{idea_new_name_in}' WHERE LOWER(name) = '{idea_name}' AND user_id = {message.from_user.id} LIMIT 1;")
                queries.append(
                    f"UPDATE USERS SET sts_chat = 'IDLE' WHERE tg_id = {message.from_user.id};")
                msg = f"Done\!\nIdea *{idea_name}* has been renamed to *{idea_new_name_out}*"
            else:
                msg = f"You already have an idea named *{idea_new_name_out}*"
        elif answ[0] == "MODI_DES":
            decr_new_in  = message.text.strip().lower()
            idea_name = await get_custom_column(message.from_user.id)
            idea_name_out = await parse_msg(idea_name, True)
            queries.append(
                    f"UPDATE IDEAS set descr = '{decr_new_in}' WHERE LOWER(name) = '{idea_name}' AND user_id = {message.from_user.id} LIMIT 1;")
            queries.append(
                    f"UPDATE USERS SET sts_chat = 'IDLE' WHERE tg_id = {message.from_user.id};")
            msg = f"Done\!\nDescription of idea *{idea_name_out}* has been changed\!"
        elif answ[0] == "MODI_PRC":
            # TODO VALIDATE price
            price_new_in  = message.text.strip().lower()
            price_new_out = await parse_msg(price_new_in, force=True)
            idea_name = await get_custom_column(message.from_user.id)
            idea_name_out = await parse_msg(idea_name, True)
            queries.append(
                f"UPDATE IDEAS set price = {price_new_in} WHERE LOWER(name) = '{idea_name}' AND user_id = {message.from_user.id} LIMIT 1;")
            queries.append(
                f"UPDATE USERS SET sts_chat = 'IDLE' WHERE tg_id = {message.from_user.id};")
            msg = f"Done\!\nPrice of idea *{idea_name_out}* is now *{price_new_out}*\!"
        elif answ[0] == "MODI_ORI":
            origin_new_in  = message.text.strip().lower()
            origin_new_out = await parse_msg(origin_new_in, force=True)
            idea_name = await get_custom_column(message.from_user.id)
            idea_name_out = await parse_msg(idea_name, True)
            queries.append(
                f"UPDATE IDEAS set origin = '{origin_new_in}' WHERE LOWER(name) = '{idea_name}' AND user_id = {message.from_user.id} LIMIT 1;")
            queries.append(
                f"UPDATE USERS SET sts_chat = 'IDLE' WHERE tg_id = {message.from_user.id};")
            msg = f"Done\!\nOrigin of idea *{idea_name_out}* is now *{origin_new_out}*\!"
        # SET PRIVACY BUTTON STATUSES
        elif answ[0] == "ACCS_CHG":
            acces_new_in  = message.text.strip().lower()
            acces_new_out = await parse_msg(acces_new_in, force=True)
            idea_name = await get_custom_column(message.from_user.id)
            print("last input = ", idea_name)
            idea_name_out = await parse_msg(idea_name, True)
            if acces_new_in in accs_options:
                queries.append(
                    f"UPDATE IDEAS SET isPublic = {accs_options[acces_new_in]} WHERE user_id = {message.from_user.id} AND name = '{idea_name}' LIMIT 1")
                queries.append(
                    f"UPDATE USERS SET sts_chat = 'IDLE' WHERE tg_id = {message.from_user.id};")
                msg = f"Acces changed\!\nIdea *{idea_name_out}* is now *{acces_new_out}*"
            else:
                msg = f"Bad input in *{acces_new_out}*"
        elif answ[0] == "ACCS_RMV":
            user_name_in  = message.text.strip().lower()
            user_name_out = await parse_msg(user_name_in, force=True)
            idea_name = await get_custom_column(message.from_user.id)
            idea_name_out = await parse_msg(idea_name, True)
            query_get = f"SELECT id FROM USERS WHERE name = {user_name_in}"
            idea_id   = await get_column(f"SELECT id FROM IDEAS WHERE user_id = {message.from_user.id} AND name = '{idea_name}'")
            idea_id   = idea_id[0] 
            answ_1 = await get_column(query_get)
            if len(answ_1) == 0:
                msg = f"User named *{user_name_out}* does not exist"
            else:
                query_get = f"SELECT user_id FROM IDEAS_INF WHERE idea_id = {idea_id} AND user_id = {answ_1[0]}"
                answ_2 = await get_column(query_get)
                if len(answ_2) == 0:
                    queries.append(
                        f"INSERT INTO IDEAS_INF (user_id, idea_id) VALUES({answ_1[0]}, {idea_id})")
                    queries.append(
                        f"UPDATE USERS SET sts_chat = 'IDLE' WHERE tg_id = {message.from_user.id};")
                else:
                    msg = f"User named *{user_name_out}* is already restricted from idea *{idea_name_out}*\!"
        # FRIENDS BUTTON STATUSES
        elif answ[0] == "FRND_ADD":
            friend_name_in = message.text.strip()
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
                    queries.append(
                        f"UPDATE USERS SET sts_chat = 'IDLE' WHERE tg_id = {message.from_user.id};")
                    query_get = f"SELECT sts FROM FR_REQUESTS WHERE user_from = {message.from_user.id} AND user_to = {friend_id}"
                    answ = await get_column(query_get)
                    if len(answ) == 0:
                        queries.append(
                            f"INSERT INTO FR_REQUESTS (user_from, user_to) VALUES ({message.from_user.id}, {friend_id})")
                        msg = f"Request was sent to *{friend_name_out}* succesfully\!"
                    else:
                        if answ[0] == "0":
                            msg = f"User *{friend_name_out}* still have not answered to your previous request\!"
                        elif answ[0] == "5":
                            queries.append(
                                f"UPDATE FR_REQUESTS SET sts = 0 WHERE (user_from = {message.from_user.id} AND user_to = {friend_id})")
                            msg = f"User *{friend_name_out}* rejected your previous request\!\nBut another one is sent succesfully\!"
                else:
                    msg = f"You and user *{friend_name_out}* are already friends\!"
        elif answ[0] == "FRND_RMV":
            # check if such user exists
            friend_name_in = message.text.strip()
            friend_name_out = await parse_msg(message.text.strip(), force=True)
            query_get = f"SELECT tg_id FROM USERS WHERE name = '{friend_name_in}' LIMIT 1"
            answ = await get_column(query_get)
            if len(answ) == 0:
                msg = f"User with name *{friend_name_out}* does not exist\!"
            else:
                query_get = f"SELECT user_id, friend_id FROM FRIENDS WHERE (user_id = {message.from_user.id} AND friend_id = {answ[0]}) OR (user_id = {answ[0]} AND friend_id = {message.from_user.id})"
                db = _mysql.connect(host="localhost", user=usr,
                                    password=pswd, database=dbase)
                db.query(query_get)
                query_res = db.store_result()
                query_res = query_res.fetch_row(maxrows=0, how=1)
                if len(query_res) == 0:
                    msg = f"You arent friends with *{friend_name_out}* anyways\!"
                else:
                    for row in query_res:
                        usr_id = str(row['user_id'], "utf-8")
                        frd_id = str(row['friend_id'], "utf-8")
                        queries.append(
                            f"DELETE FROM FRIENDS WHERE user_id = {usr_id} AND friend_id = {frd_id}")
                    queries.append(
                        f"UPDATE USERS SET sts_chat = 'IDLE' WHERE tg_id = {message.from_user.id};")
                    msg = f"You and user *{friend_name_out}* are not friends anymore\!"
        # MY REQUESTS BUTTON STATUSES
        elif answ[0] == "FRND_ACC" or answ[0] == "FRND_REJ":
            friend_name_in = message.text.strip()
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
                    queries.append(
                        f"UPDATE USERS SET sts_chat = 'IDLE' WHERE tg_id = {message.from_user.id};")
                    if answ[0] == "FRND_ACC":
                        queries.append(
                            f"INSERT INTO FRIENDS(user_id, friend_id) VALUES({message.from_user.id}, {friend_id})")
                        queries.append(
                            f"DELETE FROM FR_REQUESTS WHERE (user_to = {message.from_user.id} AND user_from = {friend_id})")
                        msg = f"Request *ACCEPTED*\!\nYou and user *{friend_name_out}* are friends now\!"
                    elif answ[0] == "FRND_REJ":
                        queries.append(
                            f"UPDATE FR_REQUESTS SET sts = 5 WHERE (user_to = {message.from_user.id} AND user_from = {friend_id})")
                        msg = f"Request *REJECTED*"\
        # IDEA IMAGES BUTTON STATUSES
        elif answ[0] == "IMAG_SEE":
            img_name_in = message.text.strip()
            img_name_out = await parse_msg(img_name_in, force=True)
            idea_name = await get_custom_column(message.from_user.id)
            query_get = f"SELECT img_path FROM IMAGES WHERE name = '{img_name_in}' AND idea_id = (SELECT id FROM IDEAS WHERE user_id = {message.from_user.id} AND name = '{idea_name}') AND sts <> 9 LIMIT 1"
            answ = await get_column(query_get)
            if len(answ) == 0:
                msg = f"Image named *{img_name_out}* not found\!"
            else:
                queries.append(
                    f"UPDATE USERS SET sts_chat = 'IDLE' WHERE tg_id = {message.from_user.id};")
                async with aiofiles.open(answ[0], 'rb') as f:
                    photo_bytes = await f.read()
                    await bot.send_photo(chat_id=message.from_user.id, photo=photo_bytes)
                msg = f"Image named *{img_name_out}*"
        elif answ[0] == "IMAG_ADD":
            img_name_in = message.text.strip()
            img_name_out = await parse_msg(img_name_in, force=True)
            idea_name = await get_custom_column(message.from_user.id)
            query_get = f"SELECT img_path FROM IMAGES WHERE name = '{img_name_in}' AND idea_id = (SELECT id FROM IDEAS WHERE user_id = {message.from_user.id} AND name = '{idea_name}') AND sts <> 9 LIMIT 1"
            answ = await get_column(query_get)
            print(query_get)
            print(answ)
            if len(answ) == 0:
                msg = f"Good\nNow provide the image\."
                queries.append(f"UPDATE USERS set sts_chat = 'IMAG_IMG' WHERE tg_id = {message.from_user.id}")

                queries.append(
                    f"UPDATE USERS SET img_name = '{img_name_in}' WHERE tg_id = {message.from_user.id};")
            else:
                msg = f"You already have image named *{img_name_out}*"
        elif answ[0] == "IMAG_DEL":
            img_name_in = message.text.strip()
            img_name_out = await parse_msg(img_name_in, force=True)
            idea_name = await get_custom_column(message.from_user.id)
            query_get = f"SELECT id FROM IDEAS WHERE user_id = {message.from_user.id} AND name = '{idea_name}'"
            idea_id   = await get_column(query_get)
            idea_id   = idea_id[0] 
            query_get = f"SELECT img_path FROM IMAGES WHERE name = '{img_name_in}' AND idea_id = {idea_id} AND sts <> 9 LIMIT 1"
            answ = await get_column(query_get)
            if len(answ) == 0:
                msg = f"Image named *{img_name_out}* not found\!"
            else:
                msg = f"Image named *{img_name_out}* deleted\!"
                queries.append(f"UPDATE IDEAS set sts = 9 WHERE id = {idea_id} LIMIT 1")
                queries.append(
                    f"UPDATE USERS SET sts_chat = 'IDLE' WHERE tg_id = {message.from_user.id};")
        elif answ[0] == "IMAG_IMG":
            # actual save in function: 'save_img' 
            msg = f"That's not an image"
        # DEFAULT STATUS HANDLER
        elif answ[0] == "IDLE":
            keyboard = await get_keyboard(message, keyboardId=0)
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
    except Exception as e:
        await bot.send_message(message.from_user.id, f"An error occured when handling your request!\n{str(e)}\nContact an adminitrator :)")
        

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
