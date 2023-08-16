import logging
import asyncio
import calendar
from MySQLdb import _mysql
from aiogram import Bot, Dispatcher, types, executor
from remConstants import *
from datetime import datetime, date, timedelta

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)   

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

@dp.message_handler(commands=['check'])
async def handle_check_command(message: types.Message):
    await message.reply("Alive!" + " " + str(message.from_user.id))

if __name__ == '__main__':
    #executor.start_polling(dp, skip_updates=True)
    #loop = asyncio.get_event_loop()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(remind())
    loop.run_until_complete(close())
