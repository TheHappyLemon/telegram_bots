from re import sub
from remUtils import *
from aiogram import Bot, Dispatcher, types, executor
from remUtils import *
from datetime import date

@dp.message_handler(commands=['print'])
async def get_menu(message: types.Message):
    if not await check_usr(message.from_user.id, message):
        return    
    days = await get_query("SELECT * FROM DAYS ORDER BY day")
    msg = f"There are {len(days)} events:\n\n"
    for day in days:
        row = "* " + f"{day['day']}: {day['descr']}."
        if day['period_am'] != None and day['period'] != None:
            row = row + f" Repeat every {day['period_am']} {day['period']}."
        else:
            row = row + f" Don`t repeat."
        row = row + f" (id:{day['id']})"
        msg = msg + row + "\n\n"
    await send_msg(to=message.from_user.id, msg=msg)


@dp.message_handler(commands=['add'])
async def add_event(message: types.Message):
    if not await check_usr(message.from_user.id, message):
        return    
    if message.text.count('"') > 2:
        await send_msg(to=message.from_user.id, msg="Error: You should only use double quotes to enquote event description. Otherwise I can`t work 😭")
        return
    elif message.text.count('"') < 2:
        await send_msg(to=message.from_user.id, msg="Error: You must use double quotes to enquote event description. Otherwise I can`t work 😭")
        return
    message.text = sub(r'"(.*?)"', replace_spaces, message.text)
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
    args[1] = args[1].replace(delim, ' ')
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
    msg = "I can answer to following 4 commands:"
    msg = msg + "\n" + "1) /check - If a message is written, then I am working, if not then I`m down."
    msg = msg + "\n" + "2) /print - Prints out information about all events in a database."
    msg = msg + "\n" + "3) /delete <id> - <id> is an integer which uniquely identifies an event in a database. Deleted event can not be recovered. You can obtains events id from /print command."
    msg = msg + "For example, if I want to delete event with id 777, I have to write following command:"
    msg = msg + '\n\n' + "/delete 777"
    msg = msg + "\n\n" + '4) /add <date> <"description of an event"> <period> <period_amount> - Schedules a new event in a database. <date> is the events date (should be in yyyy-mm-dd format), <description> - long text about event'
    msg = msg + ", <period> (year,month,week,day) is needed if you want event to be repeated after this period, <period_amount> - how many 'periods' should pass until event is repeated"
    msg = msg + " <period> and <period_amount> can be omitted. For example, if I want to schedule event called 'Giga day' on 22 april 2023 and it happens every year, I must write following:"
    msg = msg + '\n\n' + '/add 2023-04-22 "Giga day" year 1' + '\n\n' + 'But if this event happens only once, I must write:'
    msg = msg + '\n\n' + '/add 2023-04-22 "Giga day"'
    msg = msg + '\n\n' + 'By the way, I dont have implemented "edit" button, so to change an event, simply delete the old one and create another one with correct information 😉'
    await send_msg(to=message.from_user.id, msg=msg)

@dp.message_handler(commands=['check'])
async def handle_check_command(message: types.Message):
    if not await check_usr(message.from_user.id, message):
        return
    await message.reply("Alive!" + " " + str(message.from_user.id))

async def remind(bot : Bot, reschedule : bool):
    days = await get_query("SELECT * FROM DAYS ORDER BY day")
    for day in days:
        answ = await check_day(day, reschedule)
        if answ > "":
            await bot.send_message(chat, answ)    

async def on_startup(dp : Dispatcher):
    scheduler.add_job(remind, 'cron', hour='8', minute='00', args=(bot, False,))
    scheduler.add_job(remind, 'cron', hour='18', minute='00', args=(bot, True,))

if __name__ == '__main__':
    scheduler.start()
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
