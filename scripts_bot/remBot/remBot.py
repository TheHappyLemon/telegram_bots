from re import sub
from remUtils import *
from aiogram import Bot, Dispatcher, types, executor
from remUtils import *
from datetime import date

from time import sleep
import random
import string
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ChatActions
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import traceback

@dp.message_handler(commands=['ping'])
async def ping(message: types.Message):
    usr_id = message.from_user.id
    if message.from_user.id != chat:
        return
    await send_msg(message.from_user.id, f"Alive! {usr_id}")

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await handle_user(message)
    usr_id = message.from_user.id
    queries = []
    queries.append(f"UPDATE USERS SET sts_chat      = 'IDLE' WHERE tg_id = {usr_id};")
    queries.append(f"UPDATE USERS SET last_keyboard = 0      WHERE tg_id = {usr_id};")
    await insert_data(queries)
    keyboard  = await get_keyboard(group_id=0, user_id = usr_id)
    await send_new_static_msg(usr_id, default_keyboard_text, keyboard)
    await delete_all_messages(usr_id)

@dp.message_handler(commands=['clear'])
async def delete_messages(message: types.Message):
    await handle_user(message)
    await bot.send_chat_action(message.from_user.id, ChatActions.TYPING)
    await delete_all_messages(message.chat.id)
    
async def calculate_yearly(bot : Bot):
    # calcualte only events that are irregular
    response = await calculate_events([1])
    response = "This is result from yearly event calculation!:\n\n" + response
    await send_msg(chat, response)

async def recalculate(bot : Bot):
    # This function checks if a regular event that needs to be rescheduled, was not and reschedules it.
    # This function also reschedules all continious event if needed
    response = await calculate_events([0,2])
    if  response > "":
        response = "Daily recalculation result:\n\n" + response
        await send_msg(chat, response)

async def remind(bot : Bot, to_reschedule : bool):
    '''

    msgs structure:
    {
        'day_id':{
            'msg' : 'message text',
            'users': [user_id_1, user_id_2 ... ]
        },
        ...
    }
    '''
    days = await get_query("SELECT * FROM DAYS LEFT JOIN link ON DAYS.id = link.id1 WHERE link.format = 'days' AND link.opt = 'look' ORDER BY day")
    msgs = {}
    today = await get_today()
    tomorrow = today + timedelta(days=1)
    week = today + timedelta(days=7)
    for day in days:
        if day['day'] == None:
            continue
        to_delete = True if day['delIfInPast'] == 'yes' else False
        answ = await check_day(day, to_reschedule, today, tomorrow, week)
        if answ > "":
            if msgs.get(day['id']) == None:
                msgs[day['id']] = {}
                msgs[day['id']]['msg'] = answ
                msgs[day['id']]['users'] = []
            msgs[day['id']]['users'].append(day['usr_id'])
    for event in msgs:
        for usr_id in msgs[event]['users']:
            await send_msg(usr_id, msgs[event]['msg'])


@dp.message_handler()
async def echo(message: types.Message):
    usr_id = message.from_user.id
    await handle_user(message)
    user_sts = await get_query(f"SELECT sts_chat, last_keyboard FROM USERS WHERE tg_id = {usr_id}")
    user_sts = user_sts[0]
    querries = []
    input = await escape_mysql(message.text.strip().lower())
    # input = await parse_msg(message.text.strip().lower())
    keyboard = None
    sts_chat = user_sts['sts_chat']
    clear_chat = True
    try:
        if sts_chat in ["EVENTS_ADD_R", "EVENTS_ADD_I", "EVENTS_ADD_C"]:
            keyboard = await get_keyboard(group_id=user_sts['last_keyboard'], user_id = usr_id)
            msg = "Event created!\n\nTo modify its parameters, press button 'Modify data'\nTo modify its acces parameters, press 'Modify acces'"
            if sts_chat == "EVENTS_ADD_R":
                querries.append(f"INSERT INTO DAYS(name, who) VALUES('{input}', {usr_id})")
            elif sts_chat == "EVENTS_ADD_I":
                querries.append(f"INSERT INTO DAYS(name, format, who) VALUES('{input}', 1, {usr_id})")
            elif sts_chat == "EVENTS_ADD_C":
                querries.append(f"INSERT INTO DAYS(name, format, who) VALUES('{input}', 2, {usr_id})")
            await insert_data(querries)
            day = await get_query(f"SELECT id FROM DAYS WHERE name = '{input}' AND who = {usr_id}")
            day = day[0]
            querries.clear()
            if sts_chat == "EVENTS_ADD_I":
                querries.append(f"INSERT INTO WEEKDAY_prm (day_id) VALUES({day['id']})")
            elif sts_chat == "EVENTS_ADD_C":
                vToday = await get_today()
                querries.append(f"INSERT INTO CONTINIOUSDAY_prm (day_id, day_start) VALUES({day['id']}, '{vToday.strftime('''%Y-%m-%d''')}')")
                querries.append(f"UPDATE DAYS SET day = '{vToday.strftime('''%Y-%m-%d''')}' WHERE id = {day['id']}")
            querries.append(f"INSERT INTO link(usr_id, id1, opt, format) VALUES({usr_id}, {day['id']}, 'look', 'days');")
            querries.append(f"INSERT INTO link(usr_id, id1, opt, format) VALUES({usr_id}, {day['id']}, 'modify', 'days');")
        elif sts_chat == "MODIFY_DEL":
            if await isYes(message.text.strip().lower()):
                querries.append(f"DELETE FROM DAYS WHERE id = (SELECT event_id FROM USERS WHERE tg_id = {usr_id})")
                keyboard = await get_keyboard(group_id=1, user_id = usr_id)
                msg = "Event DELETED succesfully!"
            else:
                msg = "Event NOT deleted"
                keyboard = await get_keyboard(group_id=user_sts['last_keyboard'], user_id = usr_id)
        elif sts_chat == "MODIFY_DESC":
            querries.append(f"UPDATE DAYS SET descr = '{input}' WHERE id = (SELECT event_id FROM USERS WHERE tg_id = {usr_id})")
            keyboard = await get_keyboard(group_id=2, user_id = usr_id)
            msg = "Description updated succesfully"
        elif sts_chat == "MODIFY_AMT":
            keyboard = await get_keyboard(group_id=2, user_id = usr_id)
            try:
                int(input)
                querries.append(f"UPDATE DAYS SET period_am = {input} WHERE id = (SELECT event_id FROM USERS WHERE tg_id = {usr_id})")
                msg = "Period amount updated succesfully"
            except ValueError:
                msg = "Whooops an error ocured:\n\n" + "Period amount should be an integer!"
            except Exception as e:
                msg = "Whooops an error ocured:\n\n" + str(e)
        elif sts_chat == 'INVITE_SEND_LOOK' or sts_chat == 'INVITE_SEND_MODF':
            if sts_chat == 'INVITE_SEND_LOOK':
                warn = 'subscribed to this event'
                inv  = "'subscriber'"
                opt = "'look'"
            elif sts_chat  == "INVITE_SEND_MODF":
                warn = 'redactor of this event'
                inv  = "'redactor'"
                opt = "'modify'"
            usr_to = await get_query(f"SELECT tg_id FROM USERS WHERE name = '{input}'")
            keyboard = await get_keyboard(group_id=user_sts['last_keyboard'], user_id = usr_id)
            if len(usr_to) == 0:
                msg = f"Invitation not send:\nUser {input} not found."
            else:
                usr_to = usr_to[0]['tg_id']
                is_listening = await get_query(f"SELECT id FROM link WHERE usr_id = {usr_to} AND id1 = (SELECT event_id FROM USERS WHERE tg_id = {usr_id}) AND format = 'days' AND opt = {opt}")
                if len(is_listening) != 0:
                    msg = f" Invitation not send\n\nUser is already {warn}."
                else:
                    event_answ = await get_query(f"SELECT * FROM DAYS WHERE id = (SELECT event_id FROM USERS WHERE tg_id = {usr_id})")
                    event_answ = event_answ[0]
                    querries.append(f"INSERT INTO DAYS_invites(usr_from, usr_to, day_id, type) VALUES({usr_id}, {usr_to}, {event_answ['id']}, {opt})")
                    await insert_data(querries)
                    querries.clear()
                    # Notify user that he received an invitation
                    notification = await get_day_info(day=event_answ, frmt=0)
                    notification = f"User {message.from_user.username} has sent you a {inv} invitation!\n\n" + notification
                    notification = notification + "\n\nGo to 'My invitaions' to accept or reject this invitation."
                    await send_msg(usr_to, notification)
                    msg = f"Invitation sent to user {input}"
                    clear_chat = False

        elif sts_chat == "MODIFY_NAME":
            keyboard = await get_keyboard(group_id=user_sts['last_keyboard'], user_id = usr_id)
            is_taken = await get_query(f"SELECT tg_id FROM USERS WHERE name = '{input}'")
            if len(is_taken) != 0:
                msg = f"Error:\n\nUsername '{input}' is already taken!"
                querries.append(f"UPDATE USERS SET sts_chat = 'IDLE' WHERE tg_id = {usr_id}")
            else:
                querries.append(f"UPDATE USERS SET last_input = '{input}'")
                await insert_data(querries)
                await confirm_choice(usr_id, input, 5)
                return
        elif sts_chat == "FEEDBACK_LEAVE":
            whn = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            querries.append(f"INSERT INTO FEEDBACK (data, user_id, whn) VALUES ('{input}', {usr_id}, '{whn}')")   
            querries.append(f"UPDATE USERS SET sts_chat = 'IDLE' WHERE tg_id = {usr_id}")
            msg = f"Feedback saved!\n\nThanks for information!"
            keyboard = await get_keyboard(group_id=user_sts['last_keyboard'], user_id = usr_id)
        elif sts_chat == "FEEDBACK_ANSW":
            feedback_id = await get_query(f"SELECT last_input FROM USERS WHERE tg_id = {usr_id}")
            feedback_id = feedback_id[0]['last_input']
            keyboard = await get_keyboard(group_id=user_sts['last_keyboard'], user_id = usr_id)
            if feedback_id == None:
                msg = f"Something went wrong... Try again"
            else:
                feedback_id = int(feedback_id)
                querries.append(f"UPDATE FEEDBACK SET answer = '{input}' WHERE id = {feedback_id}")
                querries.append(f"UPDATE FEEDBACK SET sts    = 2         WHERE id = {feedback_id}")
                msg = f"Answer saved!"
                # Notification
                feedback_sender = await get_query(f"SELECT user_id, whn FROM FEEDBACK WHERE id = {feedback_id}")
                feedback_sender = feedback_sender[0]
                clear_chat = False
                await send_msg(feedback_sender['user_id'], f"Notification:\n\nFeedback that you left on '{feedback_sender['whn']}' was replied to! Go to My settings -> print feedback. Now it has status 'answered'")
        else:
            msg = "Aaaaargh, unknown command"
        await insert_data(querries)
        await edit_message(usr_id, msg, keyboard)
        if clear_chat:
            await delete_all_messages(usr_id)
    except  Exception as e:
        print(e)
        traceback.print_exc()
        msg = f"Oooops, an error ocured:\n\n{str(e)}"
        await edit_message(usr_id, msg, keyboard)
    finally:
        pass
        #await edit_message(usr_id, msg, keyboard)
        #await delete_all_messages(usr_id)


async def on_startup(dp : Dispatcher):
    scheduler.add_job(remind, 'cron', hour='8', minute='00', timezone='Europe/Kiev', args=(bot, False,))
    scheduler.add_job(remind, 'cron', hour='18', minute='00', timezone='Europe/Kiev', args=(bot, True,))
    # scheduler.add_job(remind, 'cron', second = '*', args=(bot, False))
    scheduler.add_job(calculate_yearly, 'cron', year='*', month='1', day='1', week='*', day_of_week='*', hour='15', minute='0', second='0', timezone='Europe/Kiev', args=(bot,))
    scheduler.add_job(recalculate, 'cron', hour='4', minute='00', timezone='Europe/Kiev', args=(bot,))

if __name__ == '__main__':
    scheduler.start()
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
