import logging
import asyncio
import calendar
import re
from MySQLdb import _mysql
from aiogram import Bot, Dispatcher, types, executor
from remConstants import *
from datetime import datetime, date, timedelta

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)   

async def send_msg(to : int, msg : str):
    # maximum length of a telegram message is 4096 symbols. if msg is too big:
    # 1 - find last newline in given interval (from <i> to <i + max_len>)
    # 2 - create chunk from <i> to <\n pos>
    # 3 - <i> = <\n pos + 1>
    # repeat until <i> is less than length of a message
    msg_list = []
    if len(msg) >= MAX_MESSAGE_LENGTH:
        i = 0
        while i < len(msg):
            left = i
            right = i + MAX_MESSAGE_LENGTH
            line = msg[left:right]
            # this regex searches for the first newline from right side of a string
            # i got it from chatgpt, because both rfind and find for some reason returned -1 even though
            # in operator returned True... Super weird, but this works
            match = re.search(r"\n(?=[^\n]*$)", line)
            if match:
                n = match.start() + left # match is in line but i need to get from whole msg
            else:
                n = -1
            if n != -1:
                line = msg[left:n+1]
                i = n + 1
            msg_list.append(line)
    else:
        msg_list.append(msg)
    for chunk in msg_list:
        #print(chunk)
        if not(chunk == "" or chunk == '\n'):
            #print("mrdown mode = ", mode)
            await bot.send_message(to, chunk)

async def check_usr(from_id : int, message : types.Message):
    if not from_id in users:
        await message.reply("Sorry, this is a family bot, strangers are not allowed.\n\nHave a nice day!")
        return False
    return True
        

async def is_valid_date(date_string):
    try:
        # Attempt to parse the date string using datetime.strptime
        datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        return False

async def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year,month)[1])
    return date(year, month, day)

async def get_query(query: str):
    db = _mysql.connect(host="localhost", user=usr,
                        password=pswd, database=dbase)
    db.query(query)
    query_res = db.store_result()
    query_res = query_res.fetch_row(maxrows=0, how=1)
    i = 0
    list_res = []
    for query_row in query_res:
        for column in query_row:
            try:
                query_row[column] = str(query_row[column], "utf-8")
            except TypeError:
                query_row[column] = None
        list_res.append(query_row)
    db.close()
    return list_res

async def insert_data(queries: list):
    db = _mysql.connect(host="localhost", user=usr,
                        password=pswd, database=dbase)
    for query in queries:
        db.query(query)
    db.commit()  # commit the changes made to the database
    db.close()

async def get_today():
    # was needed for tests mainly
    #return datetime.strptime("2023-07-09", "%Y-%m-%d").date()
    return date.today()
    
async def reschedule(day : dict) -> None:
    if day["period"] == None or int(day["period_am"]) == None:
        # if these fields are not provided event does not need to be rescheduled
        await insert_data([f"DELETE FROM DAYS WHERE id = {day['id']}"])
        return
    vDate = datetime.strptime(day['day'], "%Y-%m-%d").date()
    period = day["period"]
    amount = int(day["period_am"])
    if period == "year":
        try:
            vDate = vDate.replace(year = vDate.year + amount)
        except ValueError:
            # exception for 'visokosniy' year (29 february transfers to 1 march)
            vDate = vDate + (date(vDate.year + amount, 1, 1) - date(vDate.year, 1, 1))
    elif period == "week":
        vDate = vDate + timedelta(days=7)
    elif period == "day":
        vDate = vDate + timedelta(days=1)
    elif period == "month":
        vDate = await add_months(vDate, 1)   
    querris = []
    querris.append(f'UPDATE DAYS SET day = DATE("{vDate.strftime("%Y-%m-%d")}") WHERE id = {day["id"]}')
    await insert_data(querris)

async def check_day(day : dict) -> bool:
    # actually i also need to adjust timezones
    # but i dont care
    # return "" if no need to remind or string with reminder itself
    date = datetime.strptime(day['day'], "%Y-%m-%d").date()
    today = await get_today()
    tomorrow = today + timedelta(days=1)
    week = today + timedelta(days=7)
    if date == tomorrow:
        return f"Attention!\n\nTomorrow is {day['descr']}"
    elif date == week:
        return f"Attention!\n\nIn 7 days there is {day['descr']}"
    elif date == today:
        await reschedule(day)
        return f"Attention!\n\nToday is {day['descr']}"
    else:
        return ""

async def remind():
    days = await get_query("SELECT * FROM DAYS ORDER BY day")
    for day in days:
        answ = await check_day(day)
        if answ > "":
            await bot.send_message(chat, answ)    

async def close():
    session = await bot.get_session()
    await session.close()

@dp.message_handler(commands=['print'])
async def get_menu(message: types.Message):
    if not await check_usr(message.from_user.id, message):
        return    
    days = await get_query("SELECT * FROM DAYS ORDER BY day")
    msg = f"There are {len(days)} events:\n\n"
    for day in days:
        row = f"{day['day']}: {day['descr']}."
        if day['period_am'] != None and day['period'] != None:
            row = row + f" Repeat after {day['period_am']} {day['period']}."
        else:
            row = row + f" Don`t repeat."
        row = row + f" (id:{day['id']})"
        msg = msg + row + "\n"
    await send_msg(to=message.from_user.id, msg=msg)

@dp.message_handler(commands=['add'])
async def add_event(message: types.Message):
    if not await check_usr(message.from_user.id, message):
        return    
    # date description period(optional) period_am(optional)
    args = message.get_args().split()
    if len(args) != 2 and len(args) != 4:
        await send_msg(to=message.from_user.id, msg="Error: Add command accept 2 (date, description) or 4(date, description, period, period amount) arguments.")
        return
    if not await is_valid_date(args[0]):
        await send_msg(to=message.from_user.id, msg=f"Bad date provided. Date should be in format yyyy-mm-dd. For example todays date should be written as {date.today().strftime('%Y-%m-%d')}.")
        return
    if args[1] == "":
        await send_msg(to=message.from_user.id, msg=f"Description can not be empty.")
        return
    if len(args) > 2:
        if not args[2] in periods:
            await send_msg(to=message.from_user.id, msg=f"Bad period provided. Only {', '.join(periods)} are allowed.")
            return
        try:
            int(args[3])
        except ValueError:
            await send_msg(to=message.from_user.id, msg=f"Period amount should be an integer.")
            return
    query = "INSERT INTO DAYS (day, descr"
    if len(args) == 2:
        query = f"INSERT INTO DAYS (day, descr) VALUES('{args[0]}', '{args[1]}')"
    else:
        query = f"INSERT INTO DAYS (day, descr, period, period_am) VALUES('{args[0]}', '{args[1]}', '{args[2]}', '{args[3]}')"
    querris = []
    querris.append(query)
    await insert_data(querris)
    await send_msg(to=message.from_user.id, msg=f"Done! Event was scheduled.")

@dp.message_handler(commands=['delete'])
async def add_event(message: types.Message):
    if not await check_usr(message.from_user.id, message):
        return    
    args = message.get_args().split()
    if len(args) != 1:
        await send_msg(to=message.from_user.id, msg=f"You should provide only one arguments: id of an event.")
        return
    try:
        int(args[0])
    except ValueError:
        await send_msg(to=message.from_user.id, msg=f"Id should be an integer!")
        return
    query = f"DELETE FROM DAYS WHERE id = {args[0]} LIMIT 1"
    querris = []
    querris.append(query)
    await insert_data(querris)
    await send_msg(to=message.from_user.id, msg=f"Done! Event was deleted from database.")

@dp.message_handler(commands=['help'])
async def add_event(message: types.Message):
    if not await check_usr(message.from_user.id, message):
        return
    msg = "I can answer to following commands:"
    msg = msg + "\n" + "1) /check - If a message is written, then I am working, if not then I`m down."
    msg = msg + "\n" + "2) /prints - Prints out information about all events in a database."
    msg = msg + "\n" + "3) /delete id - id is an integer which uniquely identifies an event in a database. Deleted event can not be recovered."
    msg = msg + "\n" + "4) /add date description period period_amount - Schedules a new event in a database. date is the events date, description - long text about event"
    msg = msg + ", period (year,month,week,day) is needed if you want event to be repeated after this period, period_amount - how many 'periods' should pass until event is repeated"
    msg = msg + " period and period_amount can be omitted"
    await send_msg(to=message.from_user.id, msg=msg)

@dp.message_handler(commands=['check'])
async def handle_check_command(message: types.Message):
    if not await check_usr(message.from_user.id, message):
        return
    await message.reply("Alive!" + " " + str(message.from_user.id))

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
    #loop = asyncio.new_event_loop()
    #asyncio.set_event_loop(loop)
    #loop.run_until_complete(remind())
    #loop.run_until_complete(close())
