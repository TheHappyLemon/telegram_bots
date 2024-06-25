from remUtils import *
from aiogram import Bot, Dispatcher, types, executor
from remUtils import *
from aiogram.types import ChatActions
from dateutil.relativedelta import relativedelta
import traceback

@dp.message_handler(content_types=[types.ContentType.DOCUMENT])
async def handle_document(message: types.Message):
    usr_id = message.from_user.id
    user_data = await get_query(f"SELECT sts_chat, name, language, last_keyboard, event_id FROM USERS WHERE tg_id = {usr_id}")
    # check if user exists
    if len(user_data) == 0:
        await start()
        return
    user_sts = user_data[0]['sts_chat']
    usr_name = user_data[0]['name']
    usr_lang = user_data[0]['language']
    event_id = user_data[0]['event_id']
    reply_markup = await get_keyboard(group_id=user_data[0]['last_keyboard'], user_id=usr_id)
    # Save message
    querries = []
    querries.append(f"INSERT INTO DAYS_messages(chat_id, msg_id) VALUES({usr_id}, {message.message_id})")
    file_name = message.document.file_name
    file_extension = file_name[file_name.rfind('.'):].lower()
    if user_sts == "EVENTS_ADD_CSV":
        # Check if the document is a CSV file
        if message.document.mime_type == 'text/csv':
            # Download the file
            path = f"{path_csv}/{usr_name}_import.csv"
            await message.document.download(destination_file=path)
            await process_csv(usr_id, path) 
    elif user_sts == "MODIFY_ADD_FILE":
        if file_extension not in ALLOWED_EXTENSIONS:
            await edit_message(usr_id, config.lang_instance.get_text(usr_lang, 'FILES.bad_type').replace('<bad>', file_extension).replace('<good>', ' '.join(ALLOWED_EXTENSIONS)), reply_markup)
            return
        new_file_name = await get_new_file_name(file_extension, event_id)
        file_name = await escape_mysql(file_name)
        await message.document.download(destination_file=new_file_name)
        querries.append(f"INSERT INTO DAYS_attachments(day_id, system_path, tg_file_id, tg_file_unique_id, real_name) VALUES({event_id}, '{new_file_name}', '{message.document.file_id}', '{message.document.file_unique_id}', '{file_name}')")
        await edit_message(usr_id, config.lang_instance.get_text(usr_lang, 'FILES.succes'), reply_markup)
    else:
        querries.append(f"UPDATE USERS SET sts_chat= 'IDLE' WHERE tg_id = {usr_id};")
        await edit_message(usr_id, config.lang_instance.get_text(usr_lang, 'FILES.unknown'), reply_markup)
    await insert_data(querries)

@dp.message_handler(commands=['ping'])
async def ping(message: types.Message):
    usr_id = message.from_user.id
    if message.from_user.id != int(chat):
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
    response = await calculate_events(formats=[1])
    response = "This is result from yearly event calculation!:\n\n" + response
    await send_msg(chat, response)

async def recalculate(delta_days : timedelta):
    # This function checks if a regular event that needs to be rescheduled, was not and reschedules it.
    # This function also reschedules all continious event if needed
    response = await calculate_events(formats=[0,2], delta_days=delta_days)
    if response > "":
        response = "Daily recalculation result:\n\n" + response
        await send_msg(chat, response)

async def calculate_dates(delta_days : int = 0):
    config.day_0 = await get_today() + timedelta(delta_days)
    config.day_1 = config.day_0 + timedelta(days=1)
    config.day_2 = config.day_0 + timedelta(days=2)
    config.day_3 = config.day_0 + timedelta(days=3)
    config.week_1 = config.day_0 + timedelta(weeks=1)
    config.week_2 = config.day_0 + timedelta(weeks=2)
    config.month_1 = config.day_0 + relativedelta(months=1)
    print(config.day_3)

async def check_day_new(day : dict) -> str:
    date = datetime.strptime(day['day'], "%Y-%m-%d").date()
    # I store path to text, because I dont know which language users use
    path = ""
    if day['when_date'] == '0 day':
        if date == config.day_0:
            path = 'DAYS_notifications.day_0'
    elif day['when_date'] == '1 day':
        if date == config.day_1:
            path = 'DAYS_notifications.day_1'
    elif day['when_date'] == '2 day':
        if date == config.day_2:
            path = 'DAYS_notifications.day_2'
    elif day['when_date'] == '3 day':
        if date == config.day_3:
            path = 'DAYS_notifications.day_3'
    elif day['when_date'] == '1 week':
        if date == config.week_1:
            path = 'DAYS_notifications.week_1'
    elif day['when_date'] == '2 week':
        if date == config.week_2:
            path = 'DAYS_notifications.week_2'
    elif day['when_date'] == '1 month':
        if date == config.month_1:
            path = 'DAYS_notifications.month_1'
    if path > "":
        return path, f"Attention! <text_whn> " + await get_day_info(day=day, frmt=1)
    return "", ""

async def remind_new():
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
    time_first = await get_today_time("%H : %M")
    days = await get_query(f'''
    SELECT DAYS.*, USERS.language, USERS.tg_id, DAYS_notifications.when_date
    FROM DAYS_notifications
    LEFT JOIN DAYS ON (DAYS.id = DAYS_notifications.day_id)
    LEFT JOIN link ON (link.id1 = DAYS_notifications.day_id)
    LEFT JOIN CONTINIOUSDAY_prm ON (CONTINIOUSDAY_prm.day_id = DAYS_notifications.day_id)
    LEFT JOIN USERS ON (link.usr_id = USERS.tg_id)
    WHERE when_time = '{time_first}'
    AND link.format = 'days' AND link.opt = 'look' ORDER BY day
    ''')
    msgs = {}
    for day in days:
        if day['day'] == None:
           continue
        path, answ = await check_day_new(day)
        if path != "":
            if msgs.get(day['id']) == None:
                msgs[day['id']] = {}
                msgs[day['id']]['msg'] = answ.replace('<text_whn>', config.lang_instance.get_text(day['language'], path))
                msgs[day['id']]['users'] = []
            msgs[day['id']]['users'].append(day['tg_id'])
    for event in msgs:
        for usr_id in msgs[event]['users']:
            await send_msg(usr_id, msgs[event]['msg'])

@dp.message_handler()
async def echo(message: types.Message):
    usr_id = message.from_user.id
    await handle_user(message)
    user_sts = await get_query(f"SELECT sts_chat, last_keyboard, language FROM USERS WHERE tg_id = {usr_id}")
    user_sts = user_sts[0]
    querries = []
    if user_sts != "MODIFY_AMT":
        # integer input
        input = await escape_mysql(message.text.strip().lower())
    keyboard = None
    sts_chat = user_sts['sts_chat']
    usr_lang = user_sts['language']
    clear_chat = True
    querries.append(f"UPDATE USERS SET sts_chat= 'IDLE' WHERE tg_id = {usr_id};")
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
        elif sts_chat == "MODIFY_DEL":
            if await isYes(message.text.strip().lower()):
                querries.append(f"DELETE FROM DAYS WHERE id = (SELECT event_id FROM USERS WHERE tg_id = {usr_id})")
                keyboard = await get_keyboard(group_id=1, user_id = usr_id)
                msg = "Event DELETED succesfully!"
            else:
                msg = "Event NOT deleted"
                keyboard = await get_keyboard(group_id=user_sts['last_keyboard'], user_id = usr_id)
        elif sts_chat == "MODIFY_E_NM":
            querries.append(f"UPDATE DAYS SET name = '{input}' WHERE id = (SELECT event_id FROM USERS WHERE tg_id = {usr_id})")
            keyboard = await get_keyboard(group_id=2, user_id = usr_id)
            msg = "Name updated succesfully"
        elif sts_chat == "MODIFY_DESC":
            querries.append(f"UPDATE DAYS SET descr = '{input}' WHERE id = (SELECT event_id FROM USERS WHERE tg_id = {usr_id})")
            keyboard = await get_keyboard(group_id=2, user_id = usr_id)
            msg = "Description updated succesfully"
        elif sts_chat == "MODIFY_AMT":
            keyboard = await get_keyboard(group_id=2, user_id = usr_id)
            try:
                if int(input) <= 0:
                    raise ValueError
                day_data = await get_query(f"SELECT * FROM DAYS INNER JOIN CONTINIOUSDAY_prm ON DAYS.id = CONTINIOUSDAY_prm.day_id WHERE DAYS.id = (SELECT event_id FROM USERS WHERE tg_id = {usr_id})")
                if len(day_data) > 0:
                    day_data = day_data[0]
                    if day_data["period"] != None:
                        day_data['day'] = await get_new_date(datetime.strptime(day_data['day'], "%Y-%m-%d").date(), day_data["period"], int(input))
                        await check_period(day_data['day'], day_data['day_start'], day_data['day_end'])
                querries.append(f"UPDATE DAYS SET period_am = {input} WHERE id = (SELECT event_id FROM USERS WHERE tg_id = {usr_id})")
                msg = "Period amount updated succesfully"
            except ValueError:
                msg = "Whooops an error ocured:\n\n" + "Period amount should be a positive integer!"
            except DateOutOfBounds as e:
                msg = "Can not set new period amount, because\n\n" + str(e)
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
                    author = await get_query(f"SELECT name FROM USERS WHERE tg_id = {usr_id}")
                    author = author[0]
                    author = await author_link(author['name'], usr_id)
                    notification = f" has sent you a {inv} invitation!\n\n" + notification
                    notification = notification + "\n\nGo to 'My invitaions' to accept or reject this invitation."
                    notification = await parse_msg(notification)
                    notification = f"User {author}" + notification
                    await send_notification(usr_to, system_name, "Notification", notification, "Markdown")
                    msg = f"Invitation sent to user {input}"
                    clear_chat = False

        elif sts_chat == "MODIFY_NAME":
            keyboard = await get_keyboard(group_id=user_sts['last_keyboard'], user_id = usr_id)
            is_taken = await get_query(f"SELECT tg_id FROM USERS WHERE name = '{input}'")
            if len(is_taken) != 0:
                msg = f"Error:\n\nUsername '{input}' is already taken!"
            else:
                querries.append(f"UPDATE USERS SET last_input = '{input}'")
                await insert_data(querries)
                await confirm_choice(usr_id, input, 5)
                return
        elif sts_chat == "FEEDBACK_LEAVE":
            whn = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            querries.append(f"INSERT INTO FEEDBACK (data, user_id, whn) VALUES ('{input}', {usr_id}, '{whn}')")   
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
                await send_notification(feedback_sender['user_id'], system_name, "Notification", f"Feedback that you left on '{feedback_sender['whn']}' was replied to! Go to My settings -> print feedback. Now it has status 'answered'")
        elif sts_chat == "FIND_BY_NAME":
            keyboard = await get_keyboard(group_id=user_sts['last_keyboard'], user_id = usr_id)
            hide_subscribed = True
            # just in case I decide to make a setting to allow see all records
            if hide_subscribed:
                query = f'''
                SELECT DAYS.*, USERS.*, WEEKDAY_prm.*, CONTINIOUSDAY_prm.*
                FROM DAYS
                LEFT JOIN USERS ON (DAYS.who = USERS.tg_id)
                LEFT JOIN WEEKDAY_prm ON (DAYS.id =  WEEKDAY_prm.day_id)
                LEFT JOIN CONTINIOUSDAY_prm ON (DAYS.id =  CONTINIOUSDAY_prm.day_id)
                WHERE DAYS.acces = 'public' AND DAYS.name LIKE '%{input}%'
                AND NOT EXISTS (SELECT 1 FROM link WHERE link.usr_id = {usr_id} AND link.id1 = DAYS.id AND link.opt = 'look' AND link.format = 'days')
                ORDER BY DAYS.day;
                '''
            else:
                query = f'''
                SELECT DAYS.*, USERS.*, WEEKDAY_prm.*, CONTINIOUSDAY_prm.*
                FROM DAYS
                LEFT JOIN USERS ON (DAYS.who = USERS.tg_id)
                LEFT JOIN WEEKDAY_prm ON (DAYS.id =  WEEKDAY_prm.day_id)
                LEFT JOIN CONTINIOUSDAY_prm ON (DAYS.id =  CONTINIOUSDAY_prm.day_id)
                WHERE DAYS.acces = 'public' AND DAYS.name LIKE '%{input}%'
                ORDER BY DAYS.day;
                '''
            days = await get_query(query)
            msg = config.lang_instance.get_text(usr_lang, 'PUBLIC.msg_res').replace('<total>', str(len(days)))
            reply_markup = InlineKeyboardMarkup()
            for day in days:
                row = await get_day_row_info(day)
                msg = msg + row + "\n\n"
                button = InlineKeyboardButton(text=str(day['USERS.name']) + ' - ' + day['name'], callback_data=f'PUB_EVNT_CHSN;{day["id"]};{day["name"]}')
                reply_markup.insert(button)
            reply_markup = await add_back_btn(12, reply_markup)
            await edit_message(usr_id, msg, reply_markup, "Markdown")
            return ""
        elif sts_chat == "FIND_BY_DESC":
            keyboard = await get_keyboard(group_id=user_sts['last_keyboard'], user_id = usr_id)
            hide_subscribed = True
            # just in case I decide to make a setting to allow see all records
            if hide_subscribed:
                query = f'''
                    SELECT DAYS.*, USERS.*, WEEKDAY_prm.*, CONTINIOUSDAY_prm.*
                    FROM DAYS
                    LEFT JOIN USERS ON (DAYS.who = USERS.tg_id)
                    LEFT JOIN WEEKDAY_prm ON (DAYS.id =  WEEKDAY_prm.day_id)
                    LEFT JOIN CONTINIOUSDAY_prm ON (DAYS.id =  CONTINIOUSDAY_prm.day_id)
                    WHERE DAYS.acces = 'public' AND DAYS.descr LIKE '%{input}%'
                    AND NOT EXISTS (SELECT 1 FROM link WHERE link.usr_id = {usr_id} AND link.id1 = DAYS.id AND link.opt = 'look' AND link.format = 'days')
                    ORDER BY DAYS.day;
                '''
            else:
                query = f'''
                    SELECT DAYS.*, USERS.*, WEEKDAY_prm.*, CONTINIOUSDAY_prm.*
                    FROM DAYS
                    LEFT JOIN USERS ON (DAYS.who = USERS.tg_id)
                    LEFT JOIN WEEKDAY_prm ON (DAYS.id =  WEEKDAY_prm.day_id)
                    LEFT JOIN CONTINIOUSDAY_prm ON (DAYS.id =  CONTINIOUSDAY_prm.day_id)
                    WHERE DAYS.acces = 'public' AND DAYS.descr LIKE '%{input}%'
                    ORDER BY DAYS.day;
                '''
            days = await get_query(query)
            msg = config.lang_instance.get_text(usr_lang, 'PUBLIC.msg_res').replace('<total>', str(len(days)))
            reply_markup = InlineKeyboardMarkup()
            for day in days:
                row = await get_day_row_info(day)
                msg = msg + row + "\n\n"
                button = InlineKeyboardButton(text=str(day['USERS.name']) + ' - ' + day['name'], callback_data=f'PUB_EVNT_CHSN;{day["id"]};{day["name"]}')
                reply_markup.insert(button)
            reply_markup = await add_back_btn(12, reply_markup)
            await edit_message(usr_id, msg, reply_markup, "Markdown")
            return ""
        else:
            msg = "Aaaaargh, unknown command"
            keyboard = await get_keyboard(group_id=user_sts['last_keyboard'], user_id = usr_id)
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
    # regular functions
    scheduler.add_job(remind_new, 'cron', minute='*/5', timezone='Europe/Kiev')
    scheduler.add_job(calculate_yearly, 'cron', year='*', month='1', day='1', week='*', day_of_week='*', hour='15', minute='0', second='0', timezone='Europe/Kiev', args=(bot,))
    # launch at 23 57 with arg 1 = timedelta(days), so reschedule dates on tommorow, so notification at 00:00 works correctly
    scheduler.add_job(recalculate, 'cron', hour='23', minute='57', timezone='Europe/Kiev', args=(timedelta(days=1),))
    scheduler.add_job(calculate_dates, 'cron', hour='23', minute='57', timezone='Europe/Kiev', args=(1,))
    # load languages
    langs = await get_query(f"SELECT lang, json FROM DAYS_langs")
    result_dict = {item['lang']: item['json'] for item in langs}
    config.lang_instance.initialize(result_dict)
    # global dates
    await calculate_dates(0)

if __name__ == '__main__':
    scheduler.start()
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
