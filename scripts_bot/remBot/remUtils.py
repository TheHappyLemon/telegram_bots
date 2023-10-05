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

async def parse_msg(msg: str, slash : bool = True):
    if slash:
        # escapes slash with a slash
        msg = msg.replace('\\', '\\\\')
    for char in Markdown_ch_all:
        msg = msg.replace(char, '\\' + char)
    return msg

async def send_msg(to : int, msg : str, parse_mode : str = None, disable_web_page_preview : bool = True):
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
    querries = []
    for chunk in msg_list:
        if not(chunk == "" or chunk == '\n'):
            sent_msg = await bot.send_message(to, chunk, parse_mode=parse_mode, disable_web_page_preview=disable_web_page_preview)
            sent_msg_id = sent_msg.message_id
            query = f"INSERT INTO DAYS_messages(chat_id, msg_id) VALUES({to}, {sent_msg_id})"
            querries.append(query)
    await insert_data(querries)
    return sent_msg

async def handle_user(message : types.Message):
    tg_id  = message.from_user.id
    name   = message.from_user.username
    msg_id = message.message_id
    answ = await get_query(f"SELECT tg_id FROM USERS WHERE tg_id = {tg_id} LIMIT 1;")
    if len(answ) == 0:
        if name == None:
            name = str(tg_id)
        queries = []
        queries.append(f"INSERT INTO USERS (tg_id, name) VALUES ({tg_id}, '{name}');")
        await insert_data(queries)
    queries = [f"INSERT INTO DAYS_messages(chat_id, msg_id) VALUES({tg_id}, {msg_id})"]
    await insert_data(queries)

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

async def check_day(day : dict, to_reschedule : bool, today : date, tomorrow : date, week : date) -> str:
    # actually i also need to adjust timezones
    # but i dont care
    # return "" if no need to remind or string with reminder itself
    date = datetime.strptime(day['day'], "%Y-%m-%d").date()
    if date == tomorrow:
        return f"Tomorrow is {day['descr']}"
    elif date == week:
        return f"In 7 days there is {day['descr']}"
    elif date == today:
        if to_reschedule:
            await reschedule(day)
        return f"Today is {day['descr']}"
    return ""

async def calculate_events(formats : list, ids : list = []):
    # 0 - regular events
    # 1 - irregular events
    response = ""
    queris = []
    if 0 in formats:
        # if some events were not rescheduled by mistake.
        # For example, bot was offline
        days = await get_query("SELECT * FROM DAYS WHERE format = 0")
        vToday = await get_today()
        for day in days:
            if day['day'] == None:
                continue
            if len(ids) > 0 and day['id'] not in ids:
                continue
            vDate = datetime.strptime(day['day'], "%Y-%m-%d").date()
            if vDate < vToday:
                response = response + f"{day['descr']} (id:{day['id']}) was rescheduled, becuase {str(vToday)} (today) is bigger than {day['day']}\n\n"
                await reschedule(day)
    if 1 in formats:
        queris = []
        days = await get_query("SELECT * FROM DAYS INNER JOIN WEEKDAY_prm ON DAYS.id = WEEKDAY_prm.day_id WHERE format = 1 ORDER BY day;")
        for day in days:
            if len(ids) > 0 and day['id'] not in ids:
                continue
            row = "* Event " + f"{day['descr']} "
            if day['format'] == '1':
                v_date = find_day_in_month(datetime.now().year, int(day['month']), int(day['weekday']), int(day['occurence']))
                queris.append(f"UPDATE DAYS SET day = '{v_date}' WHERE id = {day['id']}")
                row = row + f" is scheduled on {v_date}\n\n"
                response = response + row
    if len(queris) > 0:
        await insert_data(queris)
    return response

def find_day_in_month(year, month, day_of_week, occurrence):
    # day_of_week = [0, 1, 2, 3, 4, 5, 6]
    # occurence [1, 2, 3, 4, 5]
    # check input parameters
    if day_of_week not in days_of_week:
        return None
    if occurrence > 5 or occurrence < 1:
        return None
    day = 1
    weekday = date(year, month, day).weekday()
    # calculate first day_of_week in a month
    while weekday != day_of_week:
        day = day + 1
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
