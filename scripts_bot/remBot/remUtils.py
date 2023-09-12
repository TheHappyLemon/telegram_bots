import logging
import calendar
import re

from MySQLdb import _mysql
from aiogram import Bot, Dispatcher, types
from remConstants import *
from datetime import datetime, date, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
scheduler = AsyncIOScheduler()
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
        if not(chunk == "" or chunk == '\n'):
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

async def check_day(day : dict, reschedule : bool) -> str:
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
        if reschedule:
            await reschedule(day)
        return f"Attention!\n\nToday is {day['descr']}"
    else:
        return ""

def find_day_in_month(year, month, day_of_week, occurrence):
    # day_of_week = [0, 1, 2, 3, 4, 5, 6]
    # occurence [1, 2, 3, 4, 5]
    # check input parameters
    print(f"trying to found {occurrence} {day_of_week} in month {month} in year {year}")
    if day_of_week not in days_of_week:
        return None
    if occurrence > 5 or occurrence < 1:
        return None
    day = 1
    weekday = date(year, month, day).weekday()
    print("weekday = ",weekday)
    # calculate first day_of_week in a month
    while weekday != day_of_week:
        day = day + 1
        print(f"day = {day}")
        weekday = date(year, month, day).weekday()
    # find day_of_week number <occurence>
    # occurence - 1, because we are already on the first week
    day = day + (7 * (occurrence - 1))
    try:
        res_date = date(year, month, day)
    except ValueError:
        return None
    return res_date.strftime('%Y-%m-%d')

def replace_spaces(match):
    return match.group(0).replace(' ', delim)
