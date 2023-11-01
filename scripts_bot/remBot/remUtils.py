import logging
import calendar
import re

from MySQLdb import _mysql
from aiogram import Bot, Dispatcher, types
from remConstants import *
from datetime import datetime, date, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.exceptions import *
import traceback

async def print_events(**kwargs):
    usr_id = kwargs['usr_id']
    days = await get_query(f'''
        SELECT DAYS.*, USERS.*, WEEKDAY_prm.*
        FROM DAYS
        LEFT JOIN link ON DAYS.id = link.id1 AND link.format = 'days' AND link.opt = 'look'
        LEFT JOIN USERS ON (DAYS.who = USERS.tg_id)
        LEFT JOIN WEEKDAY_prm ON (DAYS.id =  WEEKDAY_prm.day_id)
        WHERE link.usr_id = {usr_id}
        ORDER BY DAYS.day;
    ''')
    print(f'''
        SELECT DAYS.*, USERS.*
        FROM DAYS
        LEFT JOIN link ON DAYS.id = link.id1 AND link.format = 'days' AND link.opt = 'look'
        LEFT JOIN USERS ON (DAYS.who = USERS.tg_id)
        LEFT JOIN WEEKDAY_prm ON (DAYS.id =  WEEKDAY_prm.day_id)
        WHERE link.usr_id = {usr_id}
        ORDER BY DAYS.day;
    ''')
    #days = await get_query("SELECT * FROM DAYS LEFT JOIN USERS ON DAYS.who = USERS.tg_id ORDER BY day;")
    msg = f"There are {len(days)} events:\n\n"
    for day in days:
        if day['day'] is None:
            day['day'] = default_not_calc
        row = "* " + f"{day['day']}: {day['name']} - {day['descr']}."
        if day['format'] == '0':
            if day['period_am'] != None and day['period'] != None:
                row = row + f" Repeat every {day['period_am']} {day['period']}."
            else:
                row = row + f" Don`t repeat."
        else:
            if day['occurence'] == None:
                day['occurence'] = default_not_data
            else:
                day['occurence'] = occurrences[int(day['occurence'])]
            if day['weekday'] == None:  
                day['weekday'] = default_not_data
            else:
                day['weekday'] = weekdays[int(day['weekday'])]

            if day['month'] == None:
                day['month'] = default_not_data
            else:
                day['month'] = months[int(day['month'])]
            row = row + f" Occurs on every {day['occurence']} {day['weekday']} of {day['month']}"
        if day['name'] != None:
            author = f"[{day['USERS.name']}](tg://user?id={day['tg_id']})"
        else:
            author = 'UNKNOWN'
        row = await parse_msg(row)
        row = row + f" id = {day['id']}, author = {author}"
        msg = msg + row + "\n\n"
    reply_markup = await get_back_btn(keyboard_id=1)
    await edit_message(usr_id, msg, reply_markup, "Markdown")
    return ""

async def get_back_btn(keyboard_id : int):
    keyboard =InlineKeyboardMarkup()
    button = InlineKeyboardButton(text='Back', callback_data=f'BUTTON_PRESSED;{keyboard_id};{keyboard_id};{keyboard_id};IDLE')
    keyboard.add(button)
    return keyboard

async def add_regular(**kwargs):
    usr_id = kwargs['usr_id']
    reply_markup = await get_back_btn(keyboard_id=1)
    await edit_message(usr_id, "Enter new regular event name", reply_markup)
    return ""

async def add_irregular(**kwargs):
    usr_id = kwargs['usr_id']
    reply_markup = await get_back_btn(keyboard_id=1)
    await edit_message(usr_id, "Enter new irregular event name", reply_markup)
    return ""

async def change_date(**kwargs):
    usr_id = kwargs['usr_id']
    event_name = kwargs['event_name']
    reply_markup = await get_back_btn(keyboard_id=2)
    await edit_message(usr_id, f"Enter new date year for event {event_name}", reply_markup)
    return ""

async def change_date_month(**kwargs):
    usr_id = kwargs['usr_id'] 
    querries = [] 
    querries.append(f"UPDATE USERS SET sts_chat = 'MODIFY_DATE_MM' WHERE tg_id = {usr_id};")
    await insert_data(querries)
    reply_markup = await get_back_btn(keyboard_id=2)
    await edit_message(usr_id, f"Enter new date month", reply_markup)

async def change_date_day(**kwargs):
    usr_id = kwargs['usr_id'] 
    querries = [] 
    querries.append(f"UPDATE USERS SET sts_chat = 'MODIFY_DATE_DD' WHERE tg_id = {usr_id};")
    await insert_data(querries)
    reply_markup = await get_back_btn(keyboard_id=2)
    await edit_message(usr_id, f"Enter new date day", reply_markup)

async def change_date_date(**kwargs):
    usr_id = kwargs['usr_id'] 
    querries = []
    keyboard = await get_keyboard(2, usr_id)
    querries.append(f"UPDATE USERS SET sts_chat = 'IDLE' WHERE tg_id = {usr_id};")
    answ_date = await get_query(f"SELECT last_input FROM USERS WHERE tg_id = {usr_id}")
    answ_date = answ_date[0]['last_input']
    if not await is_valid_date(answ_date):
        msg = f"Although year, month and day are correct values, date '{answ_date}' is not a valid date."
    else:
        querries.append(f"UPDATE DAYS SET day = '{answ_date}' WHERE DAYS.id = (SELECT event_id FROM USERS WHERE tg_id = {usr_id})")
        msg = f"Date was changed succesfully to '{answ_date}'"
    await insert_data(querries)
    await edit_message(usr_id, msg, keyboard)
    await delete_all_messages(usr_id)

async def change_desc(**kwargs):
    usr_id = kwargs['usr_id']
    event_name = kwargs['event_name']
    reply_markup = await get_back_btn(keyboard_id=2)
    await edit_message(usr_id, f"Enter new description for event {event_name}", reply_markup)
    return ""

async def change_period(**kwargs):
    usr_id = kwargs['usr_id']
    event_name = kwargs['event_name']
    keyboard = InlineKeyboardMarkup()
    for period in periods:
        button = InlineKeyboardButton(text=period, callback_data=f'PERIOD_CHOOSEN;{period}')
        keyboard.add(button)
    button = InlineKeyboardButton(text='Back', callback_data=f'BUTTON_PRESSED;2;2;2;IDLE')
    keyboard.add(button)
    await edit_message(usr_id, f"Choose new period for event {event_name}", keyboard)
    return ""

async def change_weekday(**kwargs):
    usr_id = kwargs['usr_id']
    event_name = kwargs['event_name']
    event_id = kwargs['event_id']
    keyboard = InlineKeyboardMarkup()
    for wkd_key, wkd_val in weekdays.items():
        button = InlineKeyboardButton(text=wkd_val, callback_data=f'WEEKDAY_CHOOSEN;{wkd_key};{event_id}')
        keyboard.add(button)
    button = InlineKeyboardButton(text='Back', callback_data=f'BUTTON_PRESSED;2;2;2;IDLE')
    keyboard.add(button)
    await edit_message(usr_id, f"Choose new weekday for event {event_name}", keyboard)
    return ""

async def change_occurence(**kwargs):
    usr_id = kwargs['usr_id']
    event_name = kwargs['event_name']
    event_id = kwargs['event_id']
    keyboard = InlineKeyboardMarkup()
    for ocr_key, ocr_val in occurrences.items():
        button = InlineKeyboardButton(text=ocr_val, callback_data=f'OCCURENCE_CHOOSEN;{ocr_key};{event_id}')
        keyboard.add(button)
    button = InlineKeyboardButton(text='Back', callback_data=f'BUTTON_PRESSED;2;2;2;IDLE')
    keyboard.add(button)
    await edit_message(usr_id, f"Choose new occurence for event {event_name}", keyboard)
    return ""

async def change_month(**kwargs):
    usr_id = kwargs['usr_id']
    event_name = kwargs['event_name']
    event_id = kwargs['event_id']
    keyboard = InlineKeyboardMarkup()
    for mnt_key, mnt_val in months.items():
        button = InlineKeyboardButton(text=mnt_val, callback_data=f'MONTH_CHOOSEN;{mnt_key};{event_id}')
        keyboard.add(button)
    button = InlineKeyboardButton(text='Back', callback_data=f'BUTTON_PRESSED;2;2;2;IDLE')
    keyboard.add(button)
    await edit_message(usr_id, f"Choose new month for event {event_name}", keyboard)
    return ""

async def change_amount(**kwargs):
    usr_id = kwargs['usr_id']
    event_name = kwargs['event_name']
    reply_markup = await get_back_btn(keyboard_id=2)
    await edit_message(usr_id, f"Enter new period amount for event {event_name}", reply_markup)
    return ""

async def invite_send(**kwargs):
    usr_id   = kwargs['usr_id']
    reply_markup = await get_back_btn(keyboard_id=3)
    await edit_message(usr_id, f"Type user name you want to invite", reply_markup)

async def feedback_leave(**kwargs):
    usr_id   = kwargs['usr_id']
    reply_markup = await get_back_btn(keyboard_id=5)
    await edit_message(usr_id, f"Enter you feedback:", reply_markup)

async def feedback_see(**kwargs):
    usr_id = kwargs['usr_id']
    reply_markup = await get_back_btn(keyboard_id=6)
    feedbacks = await get_query(f"SELECT * FROM FEEDBACK LEFT JOIN USERS ON (FEEDBACK.user_id = USERS.tg_id) ORDER BY whn")
    if len(feedbacks) == 0:  
        await edit_message(usr_id, f"No feedback found", reply_markup)
        return ""
    msg = f"There is tota of {len(feedbacks)} feedbacks:\n\n"
    i = 1 
    for feedback in feedbacks:
        sts, additional = await get_feedback_text(feedback['sts'], feedback['answer'])
        author = await author_link(name = feedback['name'], tg_id = feedback['tg_id'])
        data = await parse_msg(feedback['data'])
        msg = msg + f"{i}) Feedback from {author}. status: '{sts}'. Left on {feedback['whn']}. Text: {data}. {additional}\n"
        i = i + 1
    # mark feedback as seen
    querries = [f"UPDATE FEEDBACK SET sts = 1 WHERE sts = 0"]
    await insert_data(querries)
    await edit_message(usr_id, msg, reply_markup, "Markdown")

async def feedback_print(**kwargs):
    usr_id = kwargs['usr_id']
    reply_markup = await get_back_btn(keyboard_id=5)
    feedbacks = await get_query(f"SELECT * FROM FEEDBACK WHERE user_id = {usr_id} ORDER BY whn")
    if len(feedbacks) == 0:  
        await edit_message(usr_id, f"You have not left any feedback", reply_markup)
        return ""
    msg = f"You have left {len(feedbacks)} feedbacks:\n\n"
    i = 1
    for feedback in feedbacks:
        additional = ""
        print(feedback)
        sts, additional = await get_feedback_text(feedback['sts'], feedback['answer'])
        print('additional =', additional)
        msg = msg + f"{i}) Status: '{sts}'. Left on {feedback['whn']}. Text: {feedback['data']}. {additional}\n"
        i = i + 1
    await edit_message(usr_id, msg, reply_markup)

async def invites_print(**kwargs):
    usr_id     = kwargs['usr_id']
    event_id   = kwargs['event_id']
    event_name = kwargs['event_name']
    reply_markup = await get_back_btn(keyboard_id=3)
    query = f'''
        SELECT d.sts, d.type, u1.name AS usr_from_name, u2.name AS usr_to_name
        FROM DAYS_invites d
        JOIN USERS u1 ON d.usr_from = u1.tg_id
        JOIN USERS u2 ON d.usr_to = u2.tg_id
        WHERE d.usr_from = {usr_id} AND d.day_id = {event_id};
    '''
    print(query)
    invites = await get_query(query)
    if len(invites) == 0:  
        await edit_message(usr_id, f"There are no invites for event {event_name}", reply_markup)
        return ""
    msg = f"There are {len(invites)} invitations for '{event_name}':\n\n"
    i = 1
    for invite in invites:
        if invite['type'] == 'look':
            action = 'listen to'
        elif invite['type'] == 'modify':
            action = 'become a redactor of'
        else:
            action = '<Unknown>'
        msg = msg + f"{i}) User '{invite['usr_to_name']}' was invited by '{invite['usr_from_name']}'. Status: '{invite['sts']}. Type: '{action}'\n"
        i = i + 1
    await edit_message(usr_id, msg, reply_markup)

async def pick_feedback_adm(**kwargs):
    usr_id = kwargs['usr_id']
    feedbacks = await get_query("SELECT * FROM FEEDBACK LEFT JOIN USERS ON (FEEDBACK.user_id = USERS.tg_id) ORDER BY whn")
    msg = f"Choose a feedback"
    keyboard = InlineKeyboardMarkup(row_width=3)
    for feedback in feedbacks:
        sts, additional = await get_feedback_text(feedback['sts'])
        txt = f"{feedback['name']} : status '{sts}', left on {feedback['whn']}"
        button = InlineKeyboardButton(text=txt, callback_data=f'FEEDBACK_CHOOSEN;{feedback["id"]}')
        keyboard.add(button)
    button = InlineKeyboardButton(text='Back', callback_data=f'BUTTON_PRESSED;6;6;6;IDLE')
    keyboard.add(button)
    await edit_message(usr_id, msg, keyboard)

async def pick_feedback_my(**kwargs):
    usr_id = kwargs['usr_id']
    feedbacks = await get_query(f"SELECT * FROM FEEDBACK WHERE user_id = {usr_id} ORDER BY sts")
    msg = f"Choose a feedback"
    keyboard = InlineKeyboardMarkup(row_width=3)
    for feedback in feedbacks:
        sts, additional = await get_feedback_text(feedback['sts'])
        txt = f"Status '{sts}', left on {feedback['whn']}"
        button = InlineKeyboardButton(text=txt, callback_data=f'FEEDBACK_CHOOSEN;{feedback["id"]}')
        keyboard.add(button)
    button = InlineKeyboardButton(text='Back', callback_data=f'BUTTON_PRESSED;5;5;5;IDLE')
    keyboard.add(button)
    await edit_message(usr_id, msg, keyboard)

async def pick_invitation(**kwargs):
    usr_id     = kwargs['usr_id']
    event_id   = kwargs['event_id']
    event_name   = kwargs['event_name']
    query = f'''
        SELECT d.sts, d.id, u1.name AS usr_from_name, u2.name AS usr_to_name
        FROM DAYS_invites d
        JOIN USERS u1 ON d.usr_from = u1.tg_id
        JOIN USERS u2 ON d.usr_to = u2.tg_id
        WHERE d.usr_from = {usr_id} AND d.day_id = {event_id};
    '''
    invites = await get_query(query)
    if len(invites) == 0:
        msg = f"Event {event_name} has 0 invitations"
        keyboard  = await get_back_btn(keyboard_id=3)
    else:
        msg = f"Choose an invitation"
        keyboard = InlineKeyboardMarkup(row_width=3)
        for invite in invites:
            txt = invite['usr_to_name'] + ' by ' + invite['usr_from_name'] + ' - ' + invite['sts']
            button = InlineKeyboardButton(text=txt, callback_data=f'INVITE_CHOOSEN;{invite["id"]}')
            keyboard.add(button)
        button = InlineKeyboardButton(text='Back', callback_data=f'BUTTON_PRESSED;3;3;3;IDLE')
        keyboard.add(button)
    await edit_message(usr_id, msg, keyboard)
    return ""

async def check_event_acces(usr_id : int, goal : str):
    event_acces = await get_query(f"SELECT id, name, acces FROM DAYS WHERE DAYS.id = (SELECT event_id FROM USERS WHERE tg_id = {usr_id})")
    event_acces = event_acces[0]['acces']
    return event_acces == goal

async def check_event_format(usr_id : int, goal : str):
    print(f"SELECT id, name, format FROM DAYS WHERE DAYS.id = (SELECT event_id FROM USERS WHERE tg_id = {usr_id})")
    event_format = await get_query(f"SELECT id, name, format FROM DAYS WHERE DAYS.id = (SELECT event_id FROM USERS WHERE tg_id = {usr_id})")
    event_format = event_format[0]['format']
    return event_format == goal

async def confirm_choice(usr_id : int, callback_data : str, group : int, msg : str = ""):
    keyboard = InlineKeyboardMarkup()
    for word in confirm_words:
        button = InlineKeyboardButton(text=word, callback_data=f'CONFIRM_CHOOSEN;{word};{callback_data}')
        keyboard.add(button)
    button = InlineKeyboardButton(text='Back', callback_data=f'BUTTON_PRESSED;{group};{group};{group};IDLE')
    keyboard.add(button)
    await edit_message(usr_id, msg + f"\n\nAre you sure?", keyboard)
    return ""

async def print_invitations_my(**kwargs):
    usr_id = kwargs['usr_id']
    query = f'''
    SELECT USERS.name AS u_name, DAYS.*, di.*
    FROM DAYS_invites di
    INNER JOIN USERS ON (USERS.tg_id = di.usr_from)
    INNER JOIN DAYS  ON (DAYS.id = di.day_id)
    WHERE di.usr_to = {usr_id} AND di.sts <> 'rejected' AND di.sts <> 'accepted'
    '''
    invites = await get_query(query)
    print(invites,'\n')
    print(invites)
    if len(invites) == 0:
        reply_markup = await get_back_btn(keyboard_id=7)
        await edit_message(usr_id, "You dont have any invites", reply_markup)
        return ""
    querries = []
    answ = ""
    msgs_new = []
    msgs_old = []
    for invite in invites:
        if invite['type'] == 'look':
            action = 'listen to'
        elif invite['type'] == 'modify':
            action = 'become a redactor of'
        else:
            action = '<Unknown>'
        msg = f"{invite['u_name']} invites you to {action} event '{invite['name']}'. It is scheduled on '{invite['day']}' and is about '{invite['descr']}'"
        if invite['sts'] == 'new':
            querries.append(f"UPDATE DAYS_invites SET sts = 'seen' WHERE id = {invite['di.id']}")
            msgs_new.append(msg)
        elif invite['sts'] == 'seen':
            msgs_old.append(msg)
    answ = ""
    if len(msgs_new) != 0:
        answ = f"You have  {len(msgs_new)} new invitations:"
        i = 1
        for msg in msgs_new:
            answ = answ + '\n\n' + f"{i}) " + msg
            i = i + 1
    if len(msgs_old) != 0:
        answ = answ + f"\n\nYou have {len(msgs_old)} old invitations:"
        i = 1
        for msg in msgs_old:
            answ = answ + '\n\n' + f"{i}) " + msg
            i = i + 1
    keyboard = await get_keyboard(7, usr_id)
    await insert_data(querries)
    await edit_message(usr_id, answ, keyboard)
    return ""

async def pick_invitation_my(**kwargs):
    usr_id = kwargs['usr_id']
    query = f'''
    SELECT USERS.name AS u_name, DAYS.*, di.*
    FROM DAYS_invites di
    INNER JOIN USERS ON (USERS.tg_id = di.usr_from)
    INNER JOIN DAYS  ON (DAYS.id = di.day_id)
    WHERE di.usr_to = {usr_id} AND di.sts <> 'rejected' AND di.sts <> 'accepted'
    '''
    invites = await get_query(query)
    keyboard = InlineKeyboardMarkup(row_width=3)
    for invite in invites:
        type = invite['type']
        if type == 'look':
            type = 'listen to'
        elif type == 'modify':
            type = 'become a redactor of'
        button = InlineKeyboardButton(text=invite['u_name'] + ' - ' + invite['name'] + ' - ' + type, callback_data=f"INVITATION_MY_CHOOSEN;{invite['di.id']};{invite['id']};{invite['type']}")
        keyboard.add(button)
    button = InlineKeyboardButton(text='Back', callback_data=f'BUTTON_PRESSED;7;7;7;IDLE')
    keyboard.add(button)
    await edit_message(usr_id, f"Choose an invitation:", keyboard)
    return ""

async def set_acces(usr_id : int, new_acces : str):
    await confirm_choice(usr_id, new_acces, 3)
    return ""

async def is_event_private(**kwargs):
    return await check_event_acces(kwargs['usr_id'], 'private')

async def is_event_public(**kwargs):
    return await check_event_acces(kwargs['usr_id'], 'public')

async def is_event_regular(**kwargs):
    return await check_event_format(kwargs['usr_id'], '0')

async def is_event_irregular(**kwargs):
    return await check_event_format(kwargs['usr_id'], '1')

async def make_private(**kwargs):
    await set_acces(kwargs['usr_id'], 'private')
    return ""

async def make_public(**kwargs):
    await set_acces(kwargs['usr_id'], 'public')
    return ""

async def change_name(**kwargs):
    reply_markup = await get_back_btn(keyboard_id=5)
    await edit_message(usr_id=kwargs['usr_id'], text="Input new name:", reply_markup=reply_markup)

async def invite_send_look(**kwargs):
    reply_markup = await get_back_btn(keyboard_id=8)
    await edit_message(usr_id=kwargs['usr_id'], text="Input user name you want to send invitation to", reply_markup=reply_markup)

async def invite_send_modify(**kwargs):
    reply_markup = await get_back_btn(keyboard_id=8)
    await edit_message(usr_id=kwargs['usr_id'], text="Input user name you want to become a redactor", reply_markup=reply_markup)

async def pick_subscriber(**kwargs):
    usr_id = kwargs['usr_id']
    event_name = kwargs['event_name']
    #  user can modify only event that he has acces to
    q = f'''
        SELECT USERS.*
        FROM link
        INNER JOIN USERS ON (link.usr_id = USERS.tg_id AND USERS.tg_id <> {usr_id})
        WHERE link.id1 = (SELECT event_id FROM USERS WHERE tg_id = {usr_id}) AND
        link.format = 'days' AND link.opt = 'look'
        ORDER BY USERS.name;
    '''
    subs = await get_query(q)
    keyboard = InlineKeyboardMarkup(row_width=3)
    if len(subs) > 0:
        msg = f"Choose user you want to unsubcribe from '{event_name}'"
        for sub in subs:
            button = InlineKeyboardButton(text=sub['name'], callback_data=f'SUBSCRIBER_CHOOSEN;{sub["tg_id"]}')
            keyboard.add(button)
    else:
        msg = f"Noone is subscribed to event '{event_name}'"
    button = InlineKeyboardButton(text='Back', callback_data=f'BUTTON_PRESSED;3;3;3;IDLE')
    keyboard.add(button)
    await edit_message(usr_id, msg, keyboard)
    return ""
    

async def acces_who(**kwargs):
    # who could listen to this event
    usr_id = kwargs['usr_id']
    event_name = kwargs['event_name']
    if await is_event_private(**kwargs):
        msg = f"Event '{event_name}' is private. Noone "
    else:
        msg = f"Event '{event_name}' is public. Everyone "
    msg = msg + "can find it through 'public events'"
    # check real listeners apart from
    listeners = await get_query(f'''
        SELECT USERS.*
        FROM link
        INNER JOIN USERS ON (link.usr_id = USERS.tg_id)
        WHERE link.id1 = (SELECT event_id FROM USERS WHERE tg_id = {usr_id}) AND
        link.format = 'days' AND link.opt = 'look'
        ORDER BY USERS.name;
    ''')
    msg = msg + "\n\nFollowing people listen to this event:\n"
    i = 1
    for listener in listeners:
        author = await author_link(name = listener['name'], tg_id = listener['tg_id'])
        msg    = msg + f"{i}) {author}\n"
        i = i + 1
    redactors = await get_query(f'''
        SELECT USERS.*
        FROM link
        INNER JOIN USERS ON (link.usr_id = USERS.tg_id)
        WHERE link.id1 = (SELECT event_id FROM USERS WHERE tg_id = {usr_id}) AND
        link.format = 'days' AND link.opt = 'modify'
        ORDER BY USERS.name;
    ''')
    msg = msg + "\nFollowing people can modify this event:\n"
    i = 1
    for redactor in redactors:
        author = await author_link(name = redactor['name'], tg_id = redactor['tg_id'])
        msg    = msg + f"{i}) {author}\n"
        i = i + 1
    #msg = await parse_msg(msg=msg)
    keyboard = await get_keyboard(group_id=3, user_id=usr_id)
    await edit_message(usr_id=usr_id, text=msg, reply_markup=keyboard, parse_mode="Markdown")
    return ""


async def delete_event(**kwargs):
    # Only users that have acces to event (link.opt = 'modify') should get here!
    # Therefore I dont check for it in this function
    usr_id = kwargs['usr_id']
    event_id = kwargs['event_id']
    await confirm_choice(usr_id, event_id, 2)
    return ""

async def pick_event_mod(**kwargs):
    usr_id = kwargs['usr_id']
    await pick_event(usr_id, 'modify')

async def pick_event_look(**kwargs):
    usr_id = kwargs['usr_id']
    await pick_event(usr_id, 'look')

async def pick_event(usr_id : int, opt : str):
    #  user can modify only event that he has acces to
    days = await get_query(f'''
        SELECT *
        FROM DAYS
        INNER JOIN link ON DAYS.id = link.id1 AND link.format = 'days' AND link.opt = '{opt}'
        WHERE link.usr_id = {usr_id}
        ORDER BY DAYS.day;
    ''')
    if len(days) == 0:
        msg = "You dont have right to modify any event"
        keyboard  = await get_back_btn(keyboard_id=0)
    else:
        msg = f"Choose event that you want to modify"
        keyboard = InlineKeyboardMarkup(row_width=3)
        for day in days:
            if day['day'] is None:
                day['day'] = default_not_calc
            button = InlineKeyboardButton(text=day['name'], callback_data=f'EVENT_CHOOSEN;{day["id"]};{opt}')
            keyboard.add(button)
        # callback_data = <TYPE> ; <nextkeyboard>or<function> ; <currentKeyboard> ; <group_num><sts_user>
        #data = "BUTTON_PRESSED" + ";" + data + ";" + button_json['group_num'] + ";" + last_keyboard + ";" + button_json['sts_user']
        button = InlineKeyboardButton(text='Back', callback_data=f'BUTTON_PRESSED;1;1;1;IDLE')
        keyboard.add(button)
    await edit_message(usr_id, msg, keyboard)
    return ""

async def get_help(**kwargs):
    usr_id = kwargs['usr_id']
    keyboard  = await get_back_btn(keyboard_id=0) # 
    await bot.send_document(usr_id, document=open(pdf_help, 'rb'))
    await bot.send_document(usr_id, document=open('./files/test.txt', 'rb'))
    # with open(pdf_help, 'rb') as pdf_file:
       # await bot.send_document(usr_id, pdf_file)
    await edit_message(usr_id, "Here you go!:\n\nHere is a manual 'help.pdf'", keyboard)

async def calc_force(**kwargs):
    usr_id = kwargs['usr_id']
    reply_markup = await get_back_btn(keyboard_id=6)
    response = await calculate_events([0,1], [])
    response = "Events were forcefully recaulculated:\n\n" +  response
    await edit_message(usr_id, response, reply_markup)
    return ""

async def print_jobs(**kwargs):
    usr_id = kwargs['usr_id']
    reply_markup = await get_back_btn(keyboard_id=6)
    f = open('jobs.txt', 'w')
    scheduler.print_jobs(out = f)
    f.flush()
    f.close()
    f = open('jobs.txt', 'r')
    text = f.read()
    await edit_message(usr_id, f"Jobs:\n\n{text}", reply_markup)
    return ""

async def handle_button_press(callback_query: types.CallbackQuery):
    # callback_data = <TYPE> ; <choosen_data> ; 
    # callback_data = <TYPE> ; <nextkeyboard>or<function> ; <currentKeyboard> ; <group_num><sts_user>
    # TODO in confirmation_choosen status CHECK for yes instntly, and then check every status, if yes -> handle sts, if no - action aborted + return
    try:
        callback_data = callback_query.data.split(";")
        action_type =  callback_data[0]
        usr_id = callback_query.from_user.id
        print(callback_data)
        queries = []
        # Load next keyboard that needs event name
        user_sts = await get_query(f"SELECT sts_chat FROM USERS WHERE tg_id = {usr_id}")
        user_sts = user_sts[0]['sts_chat']
        print(user_sts,  action_type)
        keyboard = None
        if action_type == "EVENT_CHOOSEN":
            if user_sts == 'EVENTS_PICK_U' or user_sts == 'EVENTS_PICK_R':
                day_data = await get_query(f"SELECT link.id, DAYS.name FROM link INNER JOIN DAYS ON (DAYS.id = link.id1) WHERE id1 = {callback_data[1]} AND opt = '{callback_data[2]}' AND link.format = 'days'")
                print('link =', day_data)
                msg = ""
                if len(day_data) == 1:
                    msg = "IMPORTANT!\n\nYou are the only " + ("subscriber" if callback_data[2] == 'look' else "redactor") + f" of event {day_data[0]['name']}"
                    msg = msg + '\nIf you continue, this event will be deleted!'
                await confirm_choice(usr_id, callback_data[1] + ";" + callback_data[2] + ";" + str(len(day_data) == 1), 1, msg)
            elif user_sts == 'EVENTS_PICK_D' or user_sts == 'EVENTS_PICK_D':
                if user_sts == 'EVENTS_PICK_D':
                    group = 2
                elif user_sts == 'EVENTS_PICK_A':
                    group = 3
                # save event name that user has choosen
                queries.append(f"UPDATE USERS SET last_keyboard = {group} WHERE tg_id = {usr_id};")
                queries.append(f"UPDATE USERS SET sts_chat      = 'IDLE'  WHERE tg_id = {usr_id};")
                queries.append(f"UPDATE USERS SET event_id      = {callback_data[1]} WHERE tg_id = {usr_id};")
                await insert_data(queries)
                keyboard = await get_keyboard(group_id=group, user_id=usr_id)
                await edit_message(usr_id, default_keyboard_text, keyboard)
        if action_type == "INVITATION_MY_CHOOSEN":
            queries.append(f"UPDATE USERS SET last_keyboard = 7 WHERE tg_id = {usr_id};")
            await confirm_choice(usr_id, callback_data[1] + ";" + callback_data[2] + ";" + callback_data[3], 7)
        if action_type == "INVITE_CHOOSEN": 
            queries.append(f"UPDATE USERS SET last_keyboard = 3 WHERE tg_id = {usr_id};")
            await confirm_choice(usr_id, callback_data[1], 3)
        elif action_type == "PERIOD_CHOOSEN":
            keyboard = await get_keyboard(group_id=2, user_id=usr_id)
            queries.append(f"UPDATE USERS SET sts_chat      = 'IDLE'  WHERE tg_id = {usr_id};")
            queries.append(f"UPDATE DAYS  SET period        = '{callback_data[1]}' WHERE id = (SELECT event_id FROM USERS WHERE tg_id = {usr_id});")
            await insert_data(queries)
            await edit_message(usr_id, "Description updated succesfully", keyboard)
        elif action_type == "WEEKDAY_CHOOSEN":
            keyboard = await get_keyboard(group_id=2, user_id=usr_id)
            queries.append(f"UPDATE USERS SET sts_chat      = 'IDLE'  WHERE tg_id = {usr_id};")
            queries.append(f"UPDATE WEEKDAY_prm SET weekday = {callback_data[1]} WHERE day_id = {callback_data[2]}")
            await insert_data(queries)
            # will calculate event only if weekday, occurence and month were filled
            await calculate_events(formats=[1],ids=[callback_data[2]])
            await edit_message(usr_id, "Weekday updated succesfully", keyboard)
        elif action_type == "OCCURENCE_CHOOSEN":
            keyboard = await get_keyboard(group_id=2, user_id=usr_id)
            queries.append(f"UPDATE USERS SET sts_chat      = 'IDLE'  WHERE tg_id = {usr_id};")
            queries.append(f"UPDATE WEEKDAY_prm SET occurence = {callback_data[1]} WHERE day_id = {callback_data[2]}")
            await insert_data(queries)
            # will calculate event only if weekday, occurence and month were filled
            await calculate_events(formats=[1],ids=[callback_data[2]])
            await edit_message(usr_id, "Occurence updated succesfully", keyboard)
        elif action_type == "MONTH_CHOOSEN":
            keyboard = await get_keyboard(group_id=2, user_id=usr_id)
            queries.append(f"UPDATE USERS SET sts_chat      = 'IDLE'  WHERE tg_id = {usr_id};")
            queries.append(f"UPDATE WEEKDAY_prm SET month = {callback_data[1]} WHERE day_id = {callback_data[2]}")
            await insert_data(queries)
            # will calculate event only if weekday, occurence and month were filled
            await calculate_events(formats=[1],ids=[callback_data[2]])
            await edit_message(usr_id, "Month updated succesfully", keyboard)
        elif action_type == "CONFIRM_CHOOSEN":
            if user_sts == 'MAKE_PRIVATE' or user_sts == 'MAKE_PUBLIC' :
                group = 3 
                if callback_data[1].lower() == "yes":
                    queries.append(f"UPDATE DAYS SET acces = '{callback_data[2]}' WHERE id = (SELECT event_id FROM USERS WHERE tg_id = {usr_id});")
                    msg = "Updated succesfully"
                else:
                    msg = "Action aborted!"
            elif user_sts == 'SUBSCRIBER_RMV':
                group = 3
                if callback_data[1].lower() == "yes":
                    queries.append(f"DELETE FROM link WHERE usr_id = {callback_data[2]} AND format = 'days' AND id1 = (SELECT event_id FROM USERS WHERE tg_id = {usr_id})")
                    msg = "User was unsubscribed!"
                else:
                    msg = "Action aborted!"
            elif user_sts == 'INVITE_PICK_MY_A' or user_sts == 'INVITE_PICK_MY_R':
                group = 7
                if callback_data[1].lower() == "yes":
                    if user_sts == 'INVITE_PICK_MY_A':
                        msg  = "Invitation was succesfully accepted!"
                        queries.append(f"UPDATE DAYS_invites SET sts = 'accepted' WHERE id = {callback_data[2]}")
                        queries.append(f"INSERT INTO link(usr_id, id1, opt, format) VALUES({usr_id}, {callback_data[3]}, '{callback_data[4]}', 'days');")
                    elif user_sts == 'INVITE_PICK_MY_R':
                        queries.append(f"UPDATE DAYS_invites SET sts = 'rejected' WHERE id = {callback_data[2]}")
                        msg  = "Invitation was succesfully rejected!"
                else:
                    msg = "Action aborted!"
            elif user_sts == 'INVITE_PICK':
                group = 3
                if callback_data[1].lower() == "yes":
                    queries.append(f"DELETE FROM DAYS_invites WHERE id = {callback_data[2]}")
                    msg = "Invitation deleted!"
                else:
                    msg = "Action aborted!"
            elif user_sts == 'MODIFY_DEL':
                group = 1
                if callback_data[1].lower() == "yes":
                    queries.append(f"DELETE FROM DAYS WHERE id = {callback_data[2]}")
                    queries.append(f"UPDATE USERS SET event_id = NULL WHERE tg_id = {usr_id}")
                    print(f"SELECT * FROM link INNER JOIN DAYS ON (DAYS.id = link.id1) WHERE id1 = {callback_data[2]} AND opt = 'look' AND usr_id <> {usr_id}")
                    subscribers = await get_query(f"SELECT * FROM link INNER JOIN DAYS ON (DAYS.id = link.id1) WHERE id1 = {callback_data[2]} AND opt = 'look' AND usr_id <> {usr_id}")
                    author = await get_query(f"SELECT name FROM USERS WHERE tg_id = {usr_id}")
                    author = author[0]['name']
                    author = await author_link(author, usr_id)
                    msg = "Event was succesfully deleted!"
                    # send notification for everyone subscribed to event
                    await insert_data(queries)
                    if len(subscribers) != 0:
                        msg = msg + "\n\nSubscribers of this event were notified about it"
                        for subscriber in subscribers:
                            notification = f" has just deleted event '{subscriber['name']}'."
                            if subscriber['day'] == None:
                                subscriber['day'] = default_not_data
                            if subscriber['descr'] == None:
                                subscriber['descr'] = default_not_data
                            notification = notification + f"It was scheduled on {subscriber['day']} and was about {subscriber['descr']}"
                            notification = await parse_msg(notification)
                            notification = f"Notification:\n\nUser {author}" + notification
                            await send_msg(int(subscriber['usr_id']), notification, "Markdown")
                else:
                    msg = "Action aborted!"
            elif user_sts == "MODIFY_NAME":
                group = 5
                if callback_data[1].lower() == "yes":
                    queries.append(f"UPDATE USERS SET name = '{callback_data[2]}' WHERE tg_id = {usr_id}")
                    msg = f"Name changed!\n\nYou are now: '{callback_data[2]}'"
                else:
                    msg = "Action aborted!"
            elif user_sts == "FEEDBACK_DELET":
                group = 5
                if callback_data[1].lower() == "yes":
                    queries.append(f"DELETE FROM FEEDBACK WHERE id = {callback_data[2]}")
                    msg = f"Feedback deleted!"
                else:
                    msg = "Action aborted!"
            elif user_sts == "EVENTS_PICK_U" or user_sts == "EVENTS_PICK_R":
                group = 1
                if callback_data[1].lower() == "yes":
                    if user_sts == "EVENTS_PICK_U":
                        msg = "Unsubscribed"
                    else:
                        msg = "Redactor rights removed"
                    msg = msg + " Succesfully!"
                    print(callback_data[4], bool(callback_data[4]))
                    if callback_data[4] == 'True':
                        queries.append(f"DELETE FROM DAYS WHERE id = {callback_data[2]}")
                        queries.append(f"DELETE FROM link WHERE id1 = {callback_data[2]} AND format = 'days'")
                        msg = msg + f"\n\nEvent was deleted!"
                    else:
                        print("deleting user link only")
                        queries.append(f"DELETE FROM link WHERE usr_id = {usr_id} AND id1 = {callback_data[2]} AND opt = '{callback_data[3]}' AND format = 'days'")
                else:
                    msg = "Action aborted!"
            elif user_sts == 'blah blah':
                pass
            queries.append(f"UPDATE USERS SET sts_chat = 'IDLE' WHERE tg_id = {usr_id};")
            # insert_data firstly!!!, so keyboard is updated with newest data
            await insert_data(queries)
            keyboard = await get_keyboard(group_id=group, user_id=usr_id)
            await edit_message(usr_id, msg, keyboard)
        elif action_type == "FEEDBACK_CHOOSEN":
            if user_sts == "FEEDBACK_ANSW":
                keyboard = await get_back_btn(keyboard_id=6)
                queries.append(f"UPDATE USERS SET last_input = '{callback_data[1]}'")
                await insert_data(queries)
                await edit_message(usr_id, f"Enter answer for choosen feedback", keyboard)
            elif user_sts == "FEEDBACK_DELET":
                await confirm_choice(usr_id, callback_data[1], 5)
            else:
                await edit_message(usr_id, "Unknown status...\n\nType /start to restart conversation")
        elif action_type == "SUBSCRIBER_CHOOSEN":
            # now only for status SUBSCRIBER_RMV
            await confirm_choice(usr_id, callback_data[1], 3)
        elif action_type == "BUTTON_PRESSED":
            # save where user is right now
            queries.append(f"UPDATE USERS SET last_keyboard = {callback_data[3]}  WHERE tg_id = {usr_id};")
            queries.append(f"UPDATE USERS SET sts_chat      = '{callback_data[4]}' WHERE tg_id = {usr_id};")
            await insert_data(queries)
            try:
                # means that button leads to another keyboard
                int(callback_data[1])
                keyboard  = await get_keyboard(group_id=callback_data[1], user_id = usr_id)
                await edit_message(usr_id, default_keyboard_text, keyboard)
            except ValueError:
                # means that button calls some function
                #  # https://stackoverflow.com/questions/1835756/using-try-vs-if-in-python
                # extract some parameters for functions
                event_id = await get_query(f"SELECT event_id FROM USERS WHERE tg_id = {usr_id}")
                event_id = event_id[0]['event_id']
                event_name = ""
                if event_id != None:
                    event_name = await get_query(f"SELECT name FROM DAYS WHERE DAYS.id = {event_id}")
                    if len(event_name) == 0:
                        event_name = ""
                    else:
                        event_name = event_name[0]['name']
                else:
                    event_id = 0
                result = await globals()[callback_data[1]](usr_id=usr_id, event_name=event_name, event_id=event_id)
                print(f"after executing {callback_data[1]} =", result)
    except Exception as e:
        msg = f"Ooops, an error ocured:\n {repr(e)}"
        traceback.print_exc()
        keyboard_gr = await get_query(f"SELECT last_keyboard FROM USERS WHERE tg_id = {usr_id}")
        if len(keyboard_gr) != 0:
            keyboard = await get_keyboard(group_id=keyboard_gr[0]['last_keyboard'], user_id=usr_id)
        await edit_message(usr_id, msg, keyboard)


async def edit_message(usr_id : int, text : str, reply_markup : InlineKeyboardMarkup = None, parse_mode : str = None):
    message_id = await get_query(f"SELECT days_msg_id FROM USERS WHERE tg_id = {usr_id}")
    message_id = message_id[0]['days_msg_id']
    # if there is no msg id in DB
    if message_id == None:
        message_id = await send_new_static_msg(usr_id, text, reply_markup, parse_mode)
    try:
        # If user pressed 'Clear history', then message will still be found, but user wont see it...
        # For this reason there is /start command
        await bot.edit_message_text(chat_id=usr_id, message_id=message_id, text=text, reply_markup=reply_markup, parse_mode=parse_mode)
    # if message was deleted by user
    except MessageToEditNotFound:
        message_id = await send_new_static_msg(usr_id, text,  reply_markup, parse_mode)
    except MessageNotModified:
        # handle case if user pressed same button again
        pass
    except Exception as e:
        print(repr(e))
        print(e)
        traceback.print_exc()
        await send_msg(usr_id, "An error ocured trying to modify main message:\n\n" + str(e))

async def send_new_static_msg(usr_id : int, msg : str, reply_markup : InlineKeyboardMarkup = None, parse_mode : str = None):
    sent_message = await send_msg(to=usr_id, msg=msg, reply_markup=reply_markup, parse_mode=parse_mode)
    message_id = sent_message.message_id
    await insert_data([f"UPDATE USERS SET days_msg_id = {message_id} WHERE tg_id = {usr_id}"])
    return message_id

# MAIN
logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
scheduler = AsyncIOScheduler()
dp = Dispatcher(bot)
dp.register_callback_query_handler(handle_button_press)

async def get_keyboard(group_id : int, user_id : int, row_width : int = 2):
    query =f'''
    SELECT * FROM DAYS_buttons
    WHERE DAYS_buttons.group_num = {group_id} AND
    DAYS_buttons.accs_lvl <= (SELECT accs_lvl FROM USERS WHERE USERS.tg_id = {user_id})
    ORDER BY DAYS_buttons.ordr
    '''
    buttons_json = await get_query(query)
    keyboard = InlineKeyboardMarkup(row_width=row_width)
    for button_json in buttons_json:
        if button_json['showif'] != None:
            if not await globals()[button_json['showif']](usr_id=user_id):
                print('skipping', button_json['text'])
                continue
        data = button_json['func']
        if data == None:
            data = button_json['nextGroup']
        last_keyboard = button_json['nextGroup']
        if last_keyboard is None:
            last_keyboard = button_json['group_num']
        data = "BUTTON_PRESSED" + ";" + data + ";" + button_json['group_num'] + ";" + last_keyboard + ";" + button_json['sts_user']
        button = InlineKeyboardButton(text=button_json['text'], callback_data=data)
        keyboard.add(button)
    return keyboard

async def escape_mysql(msg : str):
    print("before", msg)
    for char in  escape_chars:
        msg = msg.replace(char, '\\' + char)
    print("after", msg)
    return msg

async def parse_msg(msg: str, slash : bool = True):
    if slash:
        # escapes slash with a slash
        msg = msg.replace('\\', '\\\\')
    for char in Markdown_ch_all:
        msg = msg.replace(char, '\\' + char)
    return msg

async def send_msg(to : int, msg : str, parse_mode : str = None, disable_web_page_preview : bool = True, reply_markup : InlineKeyboardMarkup = None):
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
            sent_msg = await bot.send_message(to, chunk, parse_mode=parse_mode, disable_web_page_preview=disable_web_page_preview, reply_markup=reply_markup)
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
    print(queries)
    await insert_data(queries)

async def check_usr(from_id : int, message : types.Message):
    if not from_id in users:
        await message.reply("Sorry, this is a family bot, strangers are not allowed.\n\nHave a nice day!")
        return False
    return True

async def is_valid_year(year_str):
    try:
        year = int(year_str)
        return (year >= datetime.now().year) and (year < 9999)
    except ValueError:
        return False

async def is_valid_month(month_str):
    try:
        month = int(month_str)
        return (month > 0) and (month < 13)
    except ValueError:
        return False

async def is_valid_day(day_str):
    try:
        day = int(day_str)
        return (day > 0) and (day < 32)
    except ValueError:
        return False

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

async def author_link(name : str, tg_id : str):
    return f"[{name}](tg://user?id={tg_id})"

async def isYes(text : str):
    return (text in ['y', 'ye', 'yes', 'yeah'])


async def calculate_events(formats : list, ids : list = []):
    # 0 - regular events
    # 1 - irregular events
    response = ""
    queris = []
    print("calucalte_events", formats, ids)
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
        print(days)
        for day in days:
            if day['day'] == None:
                continue
            if len(ids) > 0 and day['id'] not in ids:
                continue
            if day['month'] == None or day['weekday'] == None or day['occurence'] == None:
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


async def delete_all_messages(chat_id : int):
    msgs = await get_query(f"SELECT * FROM DAYS_messages INNER JOIN USERS ON USERS.tg_id = DAYS_messages.chat_id WHERE chat_id = {chat_id}")
    main_id = msgs[0]['days_msg_id']
    for msg in msgs:
        if msg['msg_id'] == main_id:
            continue
        try:
            await bot.delete_message(chat_id=chat_id, message_id=msg['msg_id'])
        except Exception as e:
            #  if something failed, let user delete it by himself
            pass
    querries = [f"DELETE FROM DAYS_messages WHERE chat_id = {chat_id} AND msg_id <> {main_id}"]
    await insert_data(querries)

async def get_feedback_text(sts : str, answer : str = ""):
    if sts == '0':
        return 'new', ""
    elif sts == '1':
        return 'seen', ""
    elif sts == '2':
        return 'answered', "\nAnswer: " + answer
    return "Unknown status...", ""

def find_day_in_month(year, month, day_of_week, occurrence):
    # day_of_week = [0, 1, 2, 3, 4, 5, 6]
    # occurence [1, 2, 3, 4, 5]
    # check input parameters
    if day_of_week not in weekdays:
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


