import logging
import calendar
import re
import glob
import os
import sys
import subprocess
import csv

from MySQLdb import _mysql
from aiogram import Bot, Dispatcher, types
from remConstants import *
from datetime import datetime, date, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.exceptions import *
from exceptions import *
from calendar import monthrange
from pytz import timezone
import traceback
import config

async def create_invitation(recepient_name : str, sender_id : int, warn: str, inv: str, opt: str) -> str:
    response = ""
    querries = []
    
    usr_to = await get_query(f"SELECT tg_id FROM USERS WHERE name = '{recepient_name}'")
    if len(usr_to) == 0:
        response = f"Invitation not send:\nUser {recepient_name} not found."
        return response

    usr_to = usr_to[0]['tg_id']
    is_listening = await get_query(f"SELECT id FROM link WHERE usr_id = {usr_to} AND id1 = (SELECT event_id FROM USERS WHERE tg_id = {sender_id}) AND format = 'days' AND opt = {opt}")
    if len(is_listening) != 0:
        response = f" Invitation not send\n\nUser is already {warn}."
        return response

    event_answ = await get_query(f"SELECT * FROM DAYS WHERE id = (SELECT event_id FROM USERS WHERE tg_id = {sender_id})")
    event_answ = event_answ[0]
    querries.append(f"INSERT INTO DAYS_invites(usr_from, usr_to, day_id, type) VALUES({sender_id}, {usr_to}, {event_answ['id']}, {opt})")
    await insert_data(querries)
    
    # Notify user that he received an invitation
    notification = await get_day_info(day=event_answ, frmt=0)
    author = await get_query(f"SELECT name FROM USERS WHERE tg_id = {sender_id}")
    author = author[0]
    author = await author_link(author['name'], sender_id)
    notification = f" has sent you a {inv} invitation!\n\n" + notification
    notification = notification + "\n\nGo to 'My invitaions' to accept or reject this invitation."
    notification = await parse_msg(notification)
    notification = f"User {author}" + notification
    await send_notification(usr_to, system_name, "Notification", notification, "Markdown")
    response = f"Invitation sent to user {recepient_name}"

    return response

async def get_new_file_name(file_extension, event_id, prefix = ""):
    next_id = None
    data = await get_query(f"SELECT COUNT(*) AS 'amount' FROM DAYS_attachments WHERE day_id = {event_id}")
    if len(data) == 0:
        next_id = 1
    else:
        next_id = int(data[0]['amount']) + 1
    name = str(event_id) + "_" + str(next_id) + "" + file_extension
    full_path = path_attachment + (f"{prefix}_" if prefix > "" else "") + name
    return full_path

async def get_attachments(**kwargs):
    event_id = kwargs['event_id']
    usr_lang = kwargs['usr_lang']
    event_name = kwargs['event_name']
    usr_id = kwargs['usr_id']
    edit_msg = kwargs.get("edit_msg", True)
    attachments = await get_query(f"SELECT * FROM DAYS_attachments WHERE day_id = {event_id}")
    msg = None
    reply_markup = await get_back_btn(keyboard_id=13)
    if len(attachments) == 0:
        msg = config.lang_instance.get_text(usr_lang, 'FILES.attachments_none').replace('<event_name>', event_name)
    else:
        for attachment in attachments:
            await send_file_by_id(usr_id, attachment['tg_file_id'], "", None)
        msg = config.lang_instance.get_text(usr_lang, 'FILES.attachments_succes').replace('<event_name>', event_name).replace('<amount>', str(len(attachments)))
    if edit_msg:
        await edit_message(usr_id, msg, reply_markup)

async def export_to_csv(**kwargs):
    usr_id = kwargs['usr_id']
    usr_name = kwargs['usr_name']
    days = await get_query(f'''
        SELECT DAYS.name AS 'event_name', DAYS.day AS 'date', DAYS.descr AS 'description', USERS.name AS 'creator', DAYS.acces, DAYS.delIfInPast AS 'Delete_after_execution',
        DAYS.format AS type, DAYS.period, DAYS.period_am AS 'period_amount', WEEKDAY_prm.weekday, WEEKDAY_prm.occurence, WEEKDAY_prm.month, CONTINIOUSDAY_prm.day_start AS 'start_date',
        CONTINIOUSDAY_prm.day_end  AS 'end_date'
        FROM DAYS
        LEFT JOIN link ON DAYS.id = link.id1 AND link.format = 'days' AND link.opt = 'look'
        LEFT JOIN USERS ON (DAYS.who = USERS.tg_id)
        LEFT JOIN WEEKDAY_prm ON (DAYS.id =  WEEKDAY_prm.day_id)
        LEFT JOIN CONTINIOUSDAY_prm ON (DAYS.id =  CONTINIOUSDAY_prm.day_id)
        WHERE link.usr_id = {usr_id}
        ORDER BY DAYS.day;
    ''')
    reply_markup = await get_back_btn(keyboard_id=1)
    path = f"{path_csv}/{usr_name}_export.csv"
    f = open(path, 'w', encoding='utf-8-sig')
    csv_writer = csv.DictWriter(f, fieldnames=await get_csv_header())
    csv_writer.writeheader()
    for day in days:
        if day['type'] == '0':
            day['type'] = 'regular'
        elif day['type'] == '1':
            day['type'] = 'irregular'
            day = await format_irregular(day)
        elif day['type'] == '2':
            day['type'] = 'continious'
    csv_writer.writerows(days)
    f.flush()
    f.close()
    await send_file(usr_id, path, "Here are your events transformed into csv!", reply_markup)

async def add_from_csv(**kwargs):
    usr_id = kwargs['usr_id']
    usr_lang = kwargs['usr_lang']
    reply_markup = await get_back_btn(keyboard_id=9)
    await edit_message(usr_id, config.lang_instance.get_text(usr_lang, 'FILES.get_file').replace('<file_type>', 'csv'), reply_markup)

async def add_attachments(**kwargs):
    usr_id = kwargs['usr_id']
    usr_lang = kwargs['usr_lang']
    reply_markup = await get_back_btn(keyboard_id=13)
    await edit_message(usr_id, config.lang_instance.get_text(usr_lang, 'FILES.get_file').replace('<file_type>', ''), reply_markup)

async def get_csv_header():
    # name;day;descr;who;acces;delifinpast;format;period;period_am;weekday;occurence;month;day_start;day_end;
    return ["event_name","date","description","creator","acces","Delete_after_execution","type","period","period_amount","weekday","occurence","month","start_date","end_date"]

async def process_csv(usr_id : int, path : str):
    f = open(path, 'r', encoding='utf-8-sig') # utf-8 = no BOM | utf-8-sig - for BOM reading
    reader = csv.DictReader(f)
    csv_headers = await get_csv_header()
    reader.fieldnames = [header.lower().strip() for header in reader.fieldnames]
    import_headers = reader.fieldnames
    keyboard = await get_back_btn(keyboard_id=9)
    # Check column amount in csv
    if len(csv_headers) != len(import_headers):
        # difference can be one column = invite_users - ';' separated list of users to invite automatically
        if abs(len(csv_headers) - len(import_headers)) != 1:
            msg = f"Do not change columns! Your csv has {len(import_headers)} columns, while it should have exactly {len(csv_headers)} columns:\n\n"
            for header in csv_headers:
                msg = msg + header + ", "
            msg = msg.strip().strip(',')
            await edit_message(usr_id, msg, keyboard)
            return
    # Check if all columns have good names
    errors = []
    for i in range(len(csv_headers)):
        if csv_headers[i].lower() != import_headers[i].lower():
            errors.append(f"* '{import_headers[i]}' should be '{csv_headers[i]}' instead\n")
    if len(csv_headers) != len(import_headers) and len(import_headers) - len(csv_headers) == 1:
        if import_headers[-1] != "invite_users":
            errors.append("For input you can add only one additional column 'invite_users'. Should be a list of usernames to whom send invites (sep = ;)")
    if len(errors) > 0:
        msg = f"Do not change column names! Column names should be in the same order when you export them. You have following erros:\n\n"
        for err in errors:
            msg = msg + err
        await edit_message(usr_id, msg, keyboard)
        return
    flg_err = False
    flg_wrn = False
    querries = []
    querries_add = []
    querries_invites = []
    errors = {}
    warnings = {}
    i = 1
    for row in reader:
        i = i + 1
        errors[i] = []
        warnings[i] = []
        # format data...
        vDescr       = await escape_mysql(row['description'].lower().strip())
        vName        = await escape_mysql(row['event_name'].lower().strip())
        vDate        = row['date'].lower().strip()
        vType        = row['type'].lower().strip()
        vAcces       = row['acces'].lower().strip()
        vPeriod      = row['period'].lower().strip()
        vPeriodAm    = row['period_amount'].lower().strip()
        vWeekday     = row['weekday'].lower().strip()
        vOccurence   = row['occurence'].lower().strip()
        vMonth       = row['month'].lower().strip().capitalize()
        vDayStart    = row['start_date'].lower().strip()
        vDayEnd      = row['end_date'].lower().strip()
        vDelIfInPast = row['delete_after_execution'].lower().strip()
        vUsers       = row.get('invite_users', "").lower().strip()
        # check event type
        if vType == 'regular':
            vType = '0'
        elif vType == 'irregular':
            vType = '1'
        elif vType == 'continious':
            vType = '2'
        else:
            errors[i].append("Unknown event type. Only 'regular', 'irregular' or 'continious' allowed")
        # check if name is available for this author
        if vName > "":
            name_exists = await get_query(f"SELECT * FROM DAYS WHERE who = {usr_id} AND name = '{vName}'")
            if len(name_exists) != 0:
                errors[i].append(f"You have already created event named {vName}")
        else:
            errors[i].append(f"Event name not provided")
        if vDescr == "":
            vDescr = "NULL"
            warnings[i].append("Description is empty")
        # check if valid date is provided
        # check only for regular events, because for irregular it ll be calculated later
        # and for continious events date should be today
        if vDate > "":
            if vType == "0":
                try:
                    datetime.strptime(f"{row['date']}", "%Y-%m-%d").date()
                except ValueError as e:
                    errors[i].append(f"Date {row['date']} is not a valid date '{str(e)}'")
            elif vType == "1":
                warnings[i].append("Date should not be provided for irregular events. It will be ignored")
            elif vType == "2":
                warnings[i].append("Date should not be provided for continious events. It will be ignored and set to date start if it is provided")
        else:
            if vType == "0":
                warnings[i].append("Date not provided")
            else:
                vDate = "NULL"
        # skip creator
        # check acces
        if vAcces > "":
            if not vAcces in ['private', 'public']:
                errors[i].append("Unknown acces, only 'private' or 'public' allowed")
        else:
            vAcces = "private"
            warnings[i].append("Access is empty. By default event will be private")
        # check delifinpast
        if vDelIfInPast > "":
            if not vDelIfInPast in ['yes', 'no']:
                errors[i].append("Unknown 'delete after execution' option, only 'yes' or 'no' allowed")
        else:
            vDelIfInPast = "yes"
            warnings[i].append("'delete after execution' is empty. By default 'yes' is set")
        if vPeriod > "":
            if vType in ['0','2']:
                if vPeriod not in periods:
                    msg = "Unknown period option, only "
                    for vPeriod in periods:
                        msg = msg + f"'{vPeriod}',"
                    msg = msg.strip(',') + " are allowed"
                    errors[i].append(msg)
            elif vType == "1":
                warnings[i].append("Period should not be provided for irregular events. It will be ignored")
        elif vType in ['0','2']:
            vPeriod = "NULL"
            warnings[i].append("Period is empty")
        if vPeriodAm > "":
            if vType in ['0','2']:
                try:
                    if int(vPeriodAm) <= 0:
                        errors[i].append("Period amount should be a positive integer")
                except ValueError:
                    errors[i].append("Period amount should be an integer")
            elif vType == '1':
                warnings[i].append("Period amount should not be provided for irregular events. It will be ignored")
        elif vType in ['0','2']:
            vPeriodAm = "NULL"
            warnings[i].append("Period amount is empty")
        # weekday is only for irregular event
        if vWeekday > "":
            if vType == '1':
                if not vWeekday in weekdays.values():
                    msg = "Unknown weekday option, only "
                    for vOption in weekdays.values():
                        msg = msg + f"'{vOption}',"
                    msg = msg.strip(',') + " are allowed"
                    errors[i].append(msg)
                else:
                    # get key by value
                    vWeekday = list(weekdays.keys())[list(weekdays.values()).index(vWeekday)]
            else:
                warnings[i].append("Weekday should only be provided for irregular events. It will be ignored")
        elif vType == '1':
            vWeekday = "NULL"
            warnings[i].append("Weekday is empty")
        # Occurence is only for irregular event
        if vOccurence > "":
            if vType == '1':
                if not vOccurence in occurrences.values():
                    msg = "Unknown occurence option, only "
                    for vOption in occurrences.values():
                        msg = msg + f"'{vOption}',"
                    msg = msg.strip(',') + " are allowed"
                    errors[i].append(msg)
                else:
                    # get key by value
                    vOccurence = list(occurrences.keys())[list(occurrences.values()).index(vOccurence)]
            else:
                warnings[i].append("Occurence should only be provided for irregular events. It will be ignored")
        elif vType == '1':
            vOccurence = "NULL"
            warnings[i].append("Occurence is empty")
        # Month is only for irregular event
        if vMonth > "":
            if vType == '1':
                if not vMonth in months.values():
                    msg = "Unknown month option, only "
                    for vOption in months.values():
                        msg = msg + f"'{vOption}',"
                    msg = msg.strip(',') + " are allowed"
                    errors[i].append(msg)
                else:
                    # get key by value
                    vMonth = list(months.keys())[list(months.values()).index(vMonth)]
            else:
                warnings[i].append("Month should only be provided for irregular events. It will be ignored")
        elif vType == '1':
            vMonth = "NULL"
            warnings[i].append("Month is empty")
        # Start date is only for continious events
        if vDayStart > "":
            if vType == '2':
                try:
                    vDayStart = datetime.strptime(vDayStart, "%Y-%m-%d").date()
                    vDate = vDayStart
                except ValueError:
                    errors[i].append(f"Start date {vDayStart} is not a valid date")
            else:
                warnings[i].append("Date start should only be provided for continious events. It will be ignored")
        elif vType == '2':
            vDayStart = await get_today()
            vDate = vDayStart
            warnings[i].append("Start date is empty. By default today will be used")
        # End date is only for continious events
        if vDayEnd > "":
            if vType == '2':
                try:
                    vDayEnd = datetime.strptime(vDayEnd, "%Y-%m-%d").date()
                    if vDayStart > vDayEnd:
                        errors[i].append(f"End date {vDayEnd} is earlier than start date {vDayStart}")
                except ValueError:
                    errors[i].append(f"End date {vDayEnd} is not a valid date")
            else:
                warnings[i].append("Date end should only be provided for continious events. It will be ignored")
        elif vType == '2':
            vDayEnd = "NULL"
            warnings[i].append("End date is empty. Event will be repeated forever")
        # TODO escape fields for sql
        if len(errors[i]) == 0:
            tmpDate = vDate if vDate == 'NULL' else f"'{vDate}'"
            querries.append(f"INSERT INTO DAYS(day, descr, period, period_am, format, who, name, acces, delIfInPast) VALUES({tmpDate}, '{vDescr}', '{vPeriod}', {vPeriodAm}, {vType}, {usr_id}, '{vName}', '{vAcces}', '{vDelIfInPast}');\n")
            if vType == "1":
                querries.append(f"UPDATE WEEKDAY_prm SET occurence = {vOccurence} WHERE day_id = (SELECT id FROM DAYS WHERE name = '{vName}' AND who = {usr_id} LIMIT 1);\n")
                querries.append(f"UPDATE WEEKDAY_prm SET month = {vMonth} WHERE day_id = (SELECT id FROM DAYS WHERE name = '{vName}' AND who = {usr_id} LIMIT 1);\n")
                querries.append(f"UPDATE WEEKDAY_prm SET weekday = {vWeekday} WHERE day_id = (SELECT id FROM DAYS WHERE name = '{vName}' AND who = {usr_id} LIMIT 1);\n")
            elif vType == "2":
                querries.append(f"UPDATE CONTINIOUSDAY_prm SET day_start = '{vDayStart}' WHERE day_id = (SELECT id FROM DAYS WHERE name = '{vName}' AND who = {usr_id} LIMIT 1);\n")
                querries.append(f"UPDATE CONTINIOUSDAY_prm SET day_end = '{vDayEnd}' WHERE day_id = (SELECT id FROM DAYS WHERE name = '{vName}' AND who = {usr_id} LIMIT 1);\n")
        else:
            flg_err = True
        if vUsers != "":
            # Send invites to users
            users = vUsers.split(";")
            for user in users:
                usr_to = await get_query(f"SELECT tg_id FROM USERS WHERE name = '{user}'")
                if len(usr_to) == 0:
                    warnings[i].append(f"'{user}' does not exist. Invitation will not be sent")
                    continue
                usr_to = usr_to[0]['tg_id']
                if usr_id == int(usr_to):
                    warnings[i].append(f"You can not send an invitation to youself. Invitation will not be sent")
                    continue
                querries.append(f"INSERT INTO DAYS_invites(usr_from, usr_to, day_id, type) SELECT {usr_id}, {usr_to}, id, 'look' FROM DAYS WHERE name = '{vName}' AND who = {usr_id};\n")
                # response = await create_invitation(user, usr_id, 'subscribed to this event', "'subscriber'", "'look'")
                # I can`t do so, because DAYS_invites has a FK to DAYS... So I have to send invitation after I create DAYS
                # But days are created after confirmation buttons is pressed.
        if len(warnings[i]) != 0:
            flg_wrn = True
    msg = ""
    if flg_err:
        i = 0
        for key in errors:
            if len(errors[key]) == 0:
                continue
            j = 1
            row = f"Line Nr {key}:\n\n"
            for err_txt in errors[key]:
                row = row + f"\t{j}) {err_txt}\n"
            msg = msg + row
            i = i + 1
        msg = f"You have errors in {i} rows:\n" + msg 
    if flg_wrn:
        i = 0
        if msg > "":
            msg = msg + "\nAnd"
        msg_warn = ""
        for key in warnings:
            if len(warnings[key]) == 0:
                continue
            j = 1
            row = f"Line Nr {key}:\n"
            for wrn_txt in warnings[key]:
                row = row + f"\t\t\t{j}) {wrn_txt}\n"
            msg_warn = msg_warn + row
            i = i + 1
        msg = msg + f" You have warnings in {i} rows:\n\n" + msg_warn
    if len(querries) > 0:
        # insert transaction keywords
        querries = ["START TRANSACTION;\n\n"] + querries + ["\nCOMMIT;\n"]
        files = '1'
        f = open(f"{path_querries}/{usr_id}_main.sql", 'w', encoding='utf-8')
        f.writelines(querries)
        f.flush()
        f.close()
        if msg > "":
            msg = msg + "\n\nImport events anyway? Lines with errors will be skipped, other will be imported"
        else:
            msg = "No errors found. Import events?"
        await confirm_choice(usr_id, f"{files};{usr_id}", 9, msg)
    else:
        msg = msg + "\n\n" + "Can not import a single line. Fix errors and come back"
        keyboard = await get_back_btn(9)
        await edit_message(usr_id, msg, keyboard)

async def get_day_row_info(day : dict):
    if day['day'] is None:
        day['day'] = default_not_calc
    row = "* " + f"{day['day']}: {day['name']} - {day['descr']}."
    if day['format'] == '0' or day['format'] == '2':
        if day['period_am'] != None and day['period'] != None:
            row = row + f" Repeat every {day['period_am']} {day['period']}."
        else:
            row = row + f" Don`t repeat."
        if day['format'] == '2':
            if day['day_start'] == None:
                day['day_start'] = default_not_data
            if day['day_end'] == None:
                day['day_end'] = default_not_data
            row = row + f" From {day['day_start']} until {day['day_end']}."
    elif day['format'] == '1':
        day = await format_irregular(day)
        row = row + f" Occurs on every {day['occurence']} {day['weekday']} of {day['month']}"
    if day.get('USERS.name') != None:
        author = f"[{day['USERS.name']}](tg://user?id={day['tg_id']})"
    else:
        author = 'UNKNOWN'
    row = await parse_msg(row)
    row = row + f" id = {day['id']}, author = {author}"
    return row

async def print_events(**kwargs):
    usr_id = kwargs['usr_id']
    days = await get_query(f'''
        SELECT DAYS.*, USERS.*, WEEKDAY_prm.*, CONTINIOUSDAY_prm.*
        FROM DAYS
        LEFT JOIN link ON DAYS.id = link.id1 AND link.format = 'days' AND link.opt = 'look'
        LEFT JOIN USERS ON (DAYS.who = USERS.tg_id)
        LEFT JOIN WEEKDAY_prm ON (DAYS.id =  WEEKDAY_prm.day_id)
        LEFT JOIN CONTINIOUSDAY_prm ON (DAYS.id =  CONTINIOUSDAY_prm.day_id)
        WHERE link.usr_id = {usr_id}
        ORDER BY DAYS.day;
    ''')
    msg = f"There are {len(days)} events:\n\n"
    for day in days:
        row = await get_day_row_info(day)
        msg = msg + row + "\n\n"
    reply_markup = await get_back_btn(keyboard_id=1)
    await edit_message(usr_id, msg, reply_markup, "Markdown")
    return ""

async def print_event(**kwargs):
    usr_id = kwargs['usr_id']
    day = await get_query(f'''
        SELECT DAYS.*, USERS.*, WEEKDAY_prm.*, CONTINIOUSDAY_prm.*
        FROM DAYS
        LEFT JOIN USERS ON (DAYS.who = USERS.tg_id)
        LEFT JOIN WEEKDAY_prm ON (DAYS.id =  WEEKDAY_prm.day_id)
        LEFT JOIN CONTINIOUSDAY_prm ON (DAYS.id =  CONTINIOUSDAY_prm.day_id)
        WHERE DAYS.id = (SELECT event_id FROM USERS WHERE tg_id = {usr_id})
        ORDER BY DAYS.day;
    ''')
    row = await get_day_row_info(day[0])
    reply_markup = await get_back_btn(keyboard_id=2)
    await edit_message(usr_id, row, reply_markup, "Markdown")

async def get_back_btn(keyboard_id : int):
    keyboard = InlineKeyboardMarkup()
    button = InlineKeyboardButton(text='🔙Back', callback_data=f'BUTTON_PRESSED;{keyboard_id};{keyboard_id};{keyboard_id};IDLE')
    # use add instead of insert so back button always takes full last row
    keyboard.add(button)
    return keyboard

async def add_back_btn(keyboard_id : int, keyboard : InlineKeyboardMarkup):
    button = InlineKeyboardButton(text='🔙Back', callback_data=f'BUTTON_PRESSED;{keyboard_id};{keyboard_id};{keyboard_id};IDLE')
    # use add instead of insert so back button always takes full last row
    keyboard.add(button)
    return keyboard

async def add_event(**kwargs):
    usr_id = kwargs['usr_id']
    type   = kwargs['type']
    reply_markup = await get_back_btn(keyboard_id=9)
    await edit_message(usr_id, f"Enter new {type} event name", reply_markup)
    return ""

async def add_continious(**kwargs):
    return await add_event(**kwargs, type='continious')

async def add_regular(**kwargs):
    return await add_event(**kwargs, type='regular')

async def add_irregular(**kwargs):
    return await add_event(**kwargs, type='irregular')

async def change_date(**kwargs):
    usr_id = kwargs['usr_id']
    keyboard = InlineKeyboardMarkup()
    year_now = date.today().year
    for i in range(year_now + 30, year_now - 1, -1):
        button = InlineKeyboardButton(text=str(i), callback_data=f'DATE_YEAR_CHOOSEN;{i}')
        keyboard.insert(button)
    keyboard = await add_back_btn(2, keyboard)
    await edit_message(usr_id, f"Choose new date year:", keyboard)
    return ""

async def change_date_month(**kwargs):
    usr_id = kwargs['usr_id']
    keyboard = InlineKeyboardMarkup()
    for mnt_key, mnt_val in months.items():
        button = InlineKeyboardButton(text=mnt_val, callback_data=f'DATE_MONTH_CHOOSEN;{mnt_key}')
        keyboard.insert(button)
    keyboard = await add_back_btn(2, keyboard)
    await edit_message(usr_id, f"Choose new date month:", keyboard)

async def change_date_day(**kwargs):
    usr_id = kwargs['usr_id']
    dd = monthrange(int(kwargs['yyyy']), int(kwargs['mm']))[1]
    keyboard = InlineKeyboardMarkup()
    dd_today = (await get_today()).day
    for i in range(1, dd + 1):
        button = InlineKeyboardButton(text=str(i) + (" Today" if i == dd_today else ""), callback_data=f'DATE_DAY_CHOOSEN;{i}')
        keyboard.insert(button)
    keyboard = await add_back_btn(2, keyboard)
    await edit_message(usr_id, f"Choose new date day:", keyboard)

async def change_date_date(**kwargs):
    usr_id  = kwargs['usr_id'] 
    usr_sts = kwargs['usr_sts'] 
    querries = []
    keyboard = await get_keyboard(2, usr_id)
    querries.append(f"UPDATE USERS SET sts_chat = 'IDLE' WHERE tg_id = {usr_id};")
    answ_date = await get_query(f"SELECT last_input FROM USERS WHERE tg_id = {usr_id}")
    answ_date = answ_date[0]['last_input']
    msg = f"Date was changed succesfully to '{answ_date}' (format: yyyy-mm-dd)"
    if not await is_valid_date(answ_date):
        msg = f"Although year, month and day are correct values, date '{answ_date}' (format: yyyy-mm-dd) is not a valid date."
    else:
        day_id = await get_query(f"SELECT event_id FROM USERS WHERE tg_id = {usr_id}")
        day_id = day_id[0]['event_id']
        if usr_sts == "MODIFY_DATE":
            querries.append(f"UPDATE DAYS SET day = '{answ_date}' WHERE DAYS.id = {day_id}")
        elif usr_sts in ["MODIFY_BGN", "MODIFY_END"]:
            vToday = await get_today()
            if usr_sts == "MODIFY_BGN":
                vDayStart = datetime.strptime(answ_date, "%Y-%m-%d").date()
                vDayEnd = await get_query(f"SELECT day_end FROM CONTINIOUSDAY_prm WHERE day_id = {day_id}")
                vDayEnd = vDayEnd[0]['day_end']
                if vDayEnd != None:
                    vDayEnd = datetime.strptime(vDayEnd, "%Y-%m-%d").date()
                else:
                    vDayEnd = await get_infinite_date()
                if vDayStart > vDayEnd:
                    msg = f"Start date {vDayStart} can not be later than end date {vDayEnd}"
                elif vDayStart == vDayEnd:
                    msg = f"Start date {vDayStart} can not be equal to end date {vDayEnd}"
                else:
                    querries.append(f"UPDATE CONTINIOUSDAY_prm SET day_start = '{answ_date}' WHERE day_id = {day_id}")
                    # by default continious event is repeated every day
                    querries.append(f"UPDATE DAYS SET period = 'day' WHERE id = {day_id}")
                    querries.append(f"UPDATE DAYS SET period_am = 1 WHERE id = {day_id}")
                    if vToday < vDayStart:
                        # if period has not started yet, then set day.day to period beginning
                        querries.append(f"UPDATE DAYS SET day = '{answ_date}' WHERE id = {day_id}")
                    elif vToday >= vDayStart:
                        # if period has started, then set day.day to tommorow
                        querries.append(f'''UPDATE DAYS SET day = '{(vToday + (timedelta(days=1))).strftime("%Y-%m-%d")}' WHERE id = {day_id}''')
            elif usr_sts == "MODIFY_END":
                vDayEnd = datetime.strptime(answ_date, "%Y-%m-%d").date()
                vDayStart = await get_query(f"SELECT day_start FROM CONTINIOUSDAY_prm WHERE day_id = {day_id}")
                vDayStart = vDayStart[0]['day_start']
                if vDayStart != None:
                    vDayStart = datetime.strptime(vDayStart, "%Y-%m-%d").date()
                else:
                    vDayStart = await get_tiny_date()
                if vDayStart > vDayEnd:
                    msg = f"End date {vDayEnd} can not be earlier than start date {vDayStart}"
                elif vDayStart == vDayEnd:
                    msg = f"End date {vDayEnd} can not be equal to start date {vDayStart}"
                elif vToday > vDayEnd:
                    msg = f"Today {vToday} is already past {vDayEnd}. End date should be bigger than today"
                else:
                    querries.append(f"UPDATE CONTINIOUSDAY_prm SET day_end = '{answ_date}' WHERE day_id = {day_id}")
    await insert_data(querries)
    await edit_message(usr_id, msg, keyboard)
    await delete_all_messages(usr_id)

async def change_evnt_name(**kwargs):
    usr_id = kwargs['usr_id']
    event_name = kwargs['event_name']
    reply_markup = await get_back_btn(keyboard_id=2)
    await edit_message(usr_id, f"Enter new name for event {event_name}", reply_markup)
    return ""

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
        keyboard.insert(button)
    keyboard = await add_back_btn(2, keyboard)
    await edit_message(usr_id, f"Choose new period for event {event_name}", keyboard)
    return ""

async def change_weekday(**kwargs):
    usr_id = kwargs['usr_id']
    event_name = kwargs['event_name']
    event_id = kwargs['event_id']
    keyboard = InlineKeyboardMarkup()
    for wkd_key, wkd_val in weekdays.items():
        button = InlineKeyboardButton(text=wkd_val, callback_data=f'WEEKDAY_CHOOSEN;{wkd_key};{event_id}')
        keyboard.insert(button)
    keyboard = await add_back_btn(2, keyboard)
    await edit_message(usr_id, f"Choose new weekday for event {event_name}", keyboard)
    return ""

async def change_occurence(**kwargs):
    usr_id = kwargs['usr_id']
    event_name = kwargs['event_name']
    event_id = kwargs['event_id']
    keyboard = InlineKeyboardMarkup()
    for ocr_key, ocr_val in occurrences.items():
        button = InlineKeyboardButton(text=ocr_val, callback_data=f'OCCURENCE_CHOOSEN;{ocr_key};{event_id}')
        keyboard.insert(button)
    keyboard = await add_back_btn(2, keyboard)
    await edit_message(usr_id, f"Choose new occurence for event {event_name}", keyboard)
    return ""

async def change_month(**kwargs):
    usr_id = kwargs['usr_id']
    event_name = kwargs['event_name']
    event_id = kwargs['event_id']
    keyboard = InlineKeyboardMarkup()
    for mnt_key, mnt_val in months.items():
        button = InlineKeyboardButton(text=mnt_val, callback_data=f'MONTH_CHOOSEN;{mnt_key};{event_id}')
        keyboard.insert(button)
    keyboard = await add_back_btn(2, keyboard)
    await edit_message(usr_id, f"Choose new month for event {event_name}", keyboard)
    return ""

async def change_delIfPast(**kwargs):
    usr_id = kwargs['usr_id']
    event_id = kwargs['event_id']
    await confirm_choice(usr_id, f"yes;{event_id}", 3, 'Event will be deleted after its execution time')
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
        sts, additional = await get_feedback_text(feedback['sts'], feedback['answer'])
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
        WHERE d.day_id = {event_id};
    '''
    # i want to show all invites to this event, not only from user (d.usr_from = {usr_id})
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
    keyboard = InlineKeyboardMarkup(row_width=2)
    for feedback in feedbacks:
        sts, additional = await get_feedback_text(feedback['sts'])
        txt = f"{feedback['name']} : status '{sts}', left on {feedback['whn']}"
        button = InlineKeyboardButton(text=txt, callback_data=f'FEEDBACK_CHOOSEN;{feedback["id"]}')
        keyboard.insert(button)
    keyboard = await add_back_btn(6, keyboard)
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
        keyboard.insert(button)
    keyboard = await add_back_btn(5, keyboard)
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
        WHERE d.day_id = {event_id};
    '''
    # it is possible to pick all invites, not only that you send (d.usr_from = {usr_id} AND)
    invites = await get_query(query)
    if len(invites) == 0:
        msg = f"Event {event_name} has 0 invitations"
        keyboard  = await get_back_btn(keyboard_id=3)
    else:
        msg = f"Choose an invitation"
        keyboard = InlineKeyboardMarkup(row_width=2)
        for invite in invites:
            txt = invite['usr_to_name'] + ' by ' + invite['usr_from_name'] + ' - ' + invite['sts']
            button = InlineKeyboardButton(text=txt, callback_data=f'INVITE_CHOOSEN;{invite["id"]}')
            keyboard.insert(button)
        keyboard = await add_back_btn(3, keyboard)
    await edit_message(usr_id, msg, keyboard)
    return ""

async def pick_attachment(**kwargs):
    usr_id     = kwargs['usr_id']
    event_id   = kwargs['event_id']
    event_name   = kwargs['event_name']
    attachments = await get_query(f"SELECT real_name, id FROM DAYS_attachments d WHERE d.day_id = {event_id}")
    if len(attachments) == 0:
        msg = f"Event {event_name} has 0 attachments"
        keyboard  = await get_back_btn(keyboard_id=13)
    else:
        msg = f"Choose an attachment"
        keyboard = InlineKeyboardMarkup(row_width=2)
        for attachment in attachments:
            button = InlineKeyboardButton(text=attachment['real_name'], callback_data=f'ATTACHMENT_CHOOSEN;{attachment["id"]}')
            keyboard.insert(button)
        keyboard = await add_back_btn(13, keyboard)
    await edit_message(usr_id, msg, keyboard)
    return ""

async def check_event_acces(usr_id : int, goal : str):
    event_acces = await get_query(f"SELECT id, name, acces FROM DAYS WHERE DAYS.id = (SELECT event_id FROM USERS WHERE tg_id = {usr_id})")
    event_acces = event_acces[0]['acces']
    return event_acces == goal

async def check_event_format(usr_id : int, goal : str):
    event_format = await get_query(f"SELECT id, name, format FROM DAYS WHERE DAYS.id = (SELECT event_id FROM USERS WHERE tg_id = {usr_id})")
    event_format = event_format[0]['format']
    return event_format == goal

async def confirm_choice(usr_id : int, callback_data : str, group : int, msg : str = ""):
    keyboard = InlineKeyboardMarkup()
    for word in confirm_words:
        button = InlineKeyboardButton(text=word, callback_data=f'CONFIRM_CHOOSEN;{word};{callback_data}')
        keyboard.insert(button)
    keyboard = await add_back_btn(group, keyboard)
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
    keyboard = InlineKeyboardMarkup(row_width=2)
    for invite in invites:
        type = invite['type']
        if type == 'look':
            type = 'listen to'
        elif type == 'modify':
            type = 'become a redactor of'
        button = InlineKeyboardButton(text=invite['u_name'] + ' - ' + invite['name'] + ' - ' + type, callback_data=f"INVITATION_MY_CHOOSEN;{invite['di.id']};{invite['id']};{invite['type']}")
        keyboard.insert(button)
    keyboard = await add_back_btn(7, keyboard)
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

async def is_event_continious(**kwargs):
    return await check_event_format(kwargs['usr_id'], '2')

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

async def find_by_name(**kwargs):
    usr_lang = kwargs['usr_lang']
    reply_markup = await get_back_btn(keyboard_id=12)
    await edit_message(usr_id=kwargs['usr_id'], text=config.lang_instance.get_text(usr_lang, f'PUBLIC.by_name'), reply_markup=reply_markup)

async def find_by_desc(**kwargs):
    usr_lang = kwargs['usr_lang']
    reply_markup = await get_back_btn(keyboard_id=12)
    await edit_message(usr_id=kwargs['usr_id'], text=config.lang_instance.get_text(usr_lang, f'PUBLIC.by_desc'), reply_markup=reply_markup)

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
            keyboard.insert(button)
    else:
        msg = f"Noone is subscribed to event '{event_name}'"
    keyboard = await add_back_btn(3, keyboard)
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
    msg = await parse_msg(msg)
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
    keyboard = await get_keyboard(group_id=3, user_id=usr_id)
    await edit_message(usr_id=usr_id, text=msg, reply_markup=keyboard, parse_mode="Markdown")
    return ""

async def stop_redact(**kwargs):
    await stop_acting(kwargs['usr_id'], kwargs['event_id'], kwargs['event_name'], kwargs['usr_lang'], 'modify', 10)
    return ""

async def stop_subbing(**kwargs):
    await stop_acting(kwargs['usr_id'], kwargs['event_id'], kwargs['event_name'], kwargs['usr_lang'], 'look', 1)
    return ""

async def stop_acting(usr_id : str, event_id: str, event_name: str, usr_lang: str, action : str, group : int):
    # Only users that have acces to event (link.opt = 'modify') should get here!
    # Therefore I dont check for it in this function
    day_data = await get_query(f"SELECT id FROM link WHERE id1 = {event_id} AND opt = '{action}' AND format = 'days' ")
    msg = ""
    if len(day_data) == 1:
        msg = config.lang_instance.get_text(usr_lang, f'MODIFY.{action}_warning').replace('<event_name>', event_name)
    await confirm_choice(usr_id, event_id + ";" + action + ";" + str(len(day_data) == 1), group, msg)

async def delete_event(**kwargs):
    # Only users that have acces to event (link.opt = 'modify') should get here!
    # Therefore I dont check for it in this function
    usr_id = kwargs['usr_id']
    event_id = kwargs['event_id']
    await confirm_choice(usr_id, event_id, 10)
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
        keyboard  = await get_back_btn(keyboard_id=1)
    else:
        msg = f"Choose event that you want to modify"
        keyboard = InlineKeyboardMarkup(row_width=3)
        for day in days:
            if day['day'] is None:
                day['day'] = default_not_calc
            button = InlineKeyboardButton(text=day['name'], callback_data=f'EVENT_CHOOSEN;{day["id"]};{opt}')
            keyboard.insert(button)
        # callback_data = <TYPE> ; <nextkeyboard>or<function> ; <currentKeyboard> ; <group_num><sts_user>
        #data = "BUTTON_PRESSED" + ";" + data + ";" + button_json['group_num'] + ";" + last_keyboard + ";" + button_json['sts_user']
        keyboard = await add_back_btn(1, keyboard)
    await edit_message(usr_id, msg, keyboard)
    return ""

async def make_backup(**kwargs):
    usr_id = kwargs['usr_id']
    keyboard  = await get_back_btn(keyboard_id=6)
    if usr_id != int(chat):
        await edit_message(usr_id, "Only for head chief admin!", keyboard)
        return
    # Popen is non blocking process
    subprocess.Popen(['bash', backup_script])
    await edit_message(usr_id, 'Backup is being created asynchronously!', keyboard)

async def get_backup(**kwargs):
    usr_id = kwargs['usr_id']
    keyboard  = await get_back_btn(keyboard_id=6)
    if usr_id != int(chat):
        await edit_message(usr_id, "Only for head chief admin!", keyboard)
        return
    list_of_files = glob.glob(backups_folder)
    if list_of_files == []:
        await edit_message(usr_id, "No backups found...", keyboard)
        return
    latest_file = max(list_of_files, key=os.path.getctime)
    await send_file(usr_id, latest_file, "Here you go!\n\nHere is the latest database backup", keyboard)

async def get_help(**kwargs):
    usr_id = kwargs['usr_id']
    keyboard  = await get_back_btn(keyboard_id=0)
    await send_file(usr_id, pdf_help, "Here you go!:\n\nHere is a manual 'help.pdf'", keyboard)

async def calc_force(**kwargs):
    usr_id = kwargs['usr_id']
    reply_markup = await get_back_btn(keyboard_id=6)
    response = await calculate_events(formats=[0,1,2], force=True)
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
        queries = []
        # Load next keyboard that needs event name
        user_info = await get_query(f"SELECT sts_chat, language FROM USERS WHERE tg_id = {usr_id}")
        user_sts = user_info[0]['sts_chat']
        usr_lang = user_info[0]['language']
        keyboard = None
        if action_type == "EVENT_CHOOSEN":
            # save event name that user has choosen
            queries.append(f"UPDATE USERS SET event_id      = {callback_data[1]} WHERE tg_id = {usr_id};")
            await insert_data(queries)
            # load keyboard with modifying options
            if user_sts == "EVENTS_PICK_U":
                day_name = await get_query(f"SELECT name FROM DAYS WHERE id = {callback_data[1]}")
                day_name = day_name[0]['name']
                await stop_subbing(usr_id=usr_id, event_id=callback_data[1], event_name=day_name, usr_lang=usr_lang)
            else:
                keyboard = await get_keyboard(group_id=10, user_id=usr_id)
                await edit_message(usr_id, default_keyboard_text, keyboard)
        if action_type == "INVITATION_MY_CHOOSEN":
            queries.append(f"UPDATE USERS SET last_keyboard = 7 WHERE tg_id = {usr_id};")
            await confirm_choice(usr_id, callback_data[1] + ";" + callback_data[2] + ";" + callback_data[3], 7)
        if action_type == "INVITE_CHOOSEN": 
            queries.append(f"UPDATE USERS SET last_keyboard = 3 WHERE tg_id = {usr_id};")
            await confirm_choice(usr_id, callback_data[1], 3)
        elif action_type == "PERIOD_CHOOSEN":
            keyboard = await get_keyboard(group_id=2, user_id=usr_id)
            day_data = await get_query(f"SELECT * FROM DAYS INNER JOIN CONTINIOUSDAY_prm ON DAYS.id = CONTINIOUSDAY_prm.day_id WHERE DAYS.id = (SELECT event_id FROM USERS WHERE tg_id = {usr_id})")
            if len(day_data) > 0:
                day_data = day_data[0]
                if day_data["period_am"] != None:
                    try:
                        day_data['day'] = await get_new_date(datetime.strptime(day_data['day'], "%Y-%m-%d").date(), callback_data[1], int(day_data["period_am"]))
                        await check_period(day_data['day'], day_data['day_start'], day_data['day_end'])
                    except DateOutOfBounds as e:
                        await edit_message(usr_id, "Can not update period, because:\n\n" + str(e), keyboard)
                        return
            queries.append(f"UPDATE USERS SET sts_chat      = 'IDLE'  WHERE tg_id = {usr_id};")
            queries.append(f"UPDATE DAYS  SET period        = '{callback_data[1]}' WHERE id = (SELECT event_id FROM USERS WHERE tg_id = {usr_id});")
            await insert_data(queries)
            await edit_message(usr_id, "Period updated succesfully", keyboard)
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
        elif action_type == "DATE_YEAR_CHOOSEN":
            queries.append(f"UPDATE USERS SET last_input = '{callback_data[1]}' WHERE tg_id = {usr_id}")
            await insert_data(queries)
            await change_date_month(usr_id = usr_id)
        elif action_type == "DATE_MONTH_CHOOSEN":
            answ_day = await get_query(f"SELECT last_input FROM USERS WHERE tg_id = {usr_id}")
            answ_day = answ_day[0]['last_input']
            mm = '0' + callback_data[1] if len(callback_data[1]) == 1 else callback_data[1]
            queries.append(f"UPDATE USERS SET last_input = '{answ_day + '-' + mm}' WHERE tg_id = {usr_id}")
            await insert_data(queries)
            await change_date_day(usr_id = usr_id, yyyy = answ_day, mm = mm)
        elif action_type == "DATE_DAY_CHOOSEN":
            answ_day = await get_query(f"SELECT last_input FROM USERS WHERE tg_id = {usr_id}")
            answ_day = answ_day[0]['last_input']
            dd = '0' + callback_data[1] if len(callback_data[1]) == 1 else callback_data[1]
            queries.append(f"UPDATE USERS SET last_input = '{answ_day + '-' + dd}' WHERE tg_id = {usr_id}")
            await insert_data(queries)
            await change_date_date(usr_id = usr_id, usr_sts = user_sts)
        elif action_type == "NOTIFIC_OPT_CHOOSEN":
            queries.append(f"UPDATE USERS SET last_input = '{callback_data[1]}' WHERE tg_id = {usr_id}")
            await insert_data(queries)
            await add_notific_hour(usr_id, usr_lang)
        elif action_type == "NOTIFIC_HH_CHOOSEN":
            answ_ntf = await get_query(f"SELECT last_input FROM USERS WHERE tg_id = {usr_id}")
            answ_ntf = answ_ntf[0]['last_input']
            answ_ntf = answ_ntf + ';' + callback_data[1]
            queries.append(f"UPDATE USERS SET last_input = '{answ_ntf}' WHERE tg_id = {usr_id}")
            await insert_data(queries)
            await add_notific_minutes(usr_id, callback_data[1], usr_lang)
        elif action_type == "NOTIFIC_MM_CHOOSEN":
            answ_ntf = await get_query(f"SELECT last_input, event_id FROM USERS WHERE tg_id = {usr_id}")
            event_id = answ_ntf[0]['event_id']
            answ_ntf = answ_ntf[0]['last_input']
            answ_ntf = answ_ntf + ' : ' + callback_data[1]
            queries.append(f"UPDATE USERS SET last_input = '{answ_ntf}' WHERE tg_id = {usr_id}")
            await insert_data(queries)
            await create_notific(usr_id, answ_ntf, event_id, usr_lang)
        elif action_type == "NOTIFIC_CHOOSEN":
            await confirm_choice(usr_id, callback_data[1], 11)
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
                        action = 'accepted'
                        msg  = "Invitation was succesfully accepted!"
                        queries.append(f"UPDATE DAYS_invites SET sts = 'accepted' WHERE id = {callback_data[2]}")
                        queries.append(f"INSERT INTO link(usr_id, id1, opt, format) VALUES({usr_id}, {callback_data[3]}, '{callback_data[4]}', 'days');")
                    elif user_sts == 'INVITE_PICK_MY_R':
                        action = 'rejected'
                        queries.append(f"UPDATE DAYS_invites SET sts = 'rejected' WHERE id = {callback_data[2]}")
                        msg  = "Invitation was succesfully rejected!"
                    # send notification to Invitation sender
                    event_answ = await get_query(f"SELECT * FROM DAYS WHERE id = {callback_data[3]}")
                    username   = await get_query(f"SELECT name FROM USERS WHERE tg_id = {usr_id}")
                    usr_from   = await get_query(f"SELECT usr_from FROM DAYS_invites WHERE id = {callback_data[2]}")
                    event_answ = event_answ[0]
                    username   = username[0]['name']
                    usr_from   = usr_from[0]['usr_from']
                    notification = await get_day_info(day=event_answ, frmt=0)
                    notification = f"User {username} has {action} your invitation!\n\n" + notification
                    await send_notification(int(usr_from), system_name, "Notification", notification)
                    msg = msg + f"\n\nNotification sent to invitation sender"
                else:
                    msg = "Action aborted!"
            elif user_sts == 'INVITE_PICK':
                group = 3
                if callback_data[1].lower() == "yes":
                    query = f'''
                        SELECT USERS.name AS u_name, DAYS.*, di.*
                        FROM DAYS_invites di
                        INNER JOIN USERS ON (USERS.tg_id = di.usr_from)
                        INNER JOIN DAYS  ON (DAYS.id = di.day_id)
                        WHERE di.id = {callback_data[2]}
                    '''
                    invite = await get_query(query)
                    invite = invite[0]
                    if not (invite['sts'] in ['accepted', 'rejected']):
                        # send notification to users to whom this invite was
                        # invite type
                        if invite['type'] == 'look':
                            action = 'listen to'
                        elif invite['type'] == 'modify':
                            action = 'become a redactor of'
                        else:
                            action = '<Unknown>'
                        # user that deleted the invite. It may be not only author of invitation
                        author = await get_query(f"SELECT name FROM USERS WHERE tg_id = {usr_id}")
                        author = author[0]['name']
                        author = await author_link(author, usr_id)
                        # form text message itself and send it
                        notification = f"  has just deleted invitation that was sent to you. Invitation info:\n\n{invite['u_name']} was inviting you to {action} event '{invite['name']}'. It was scheduled on '{invite['day']}' and was about '{invite['descr']}'"
                        notification = await parse_msg(notification)
                        notification = f"User {author}" + notification
                        await send_notification(invite['usr_to'], system_name, "Notification", notification, "Markdown")
                    queries.append(f"DELETE FROM DAYS_invites WHERE id = {callback_data[2]}")
                    msg = "Invitation deleted!"
                else:
                    msg = "Action aborted!"
            elif user_sts == 'MODIFY_DEL':
                if callback_data[1].lower() == "yes":
                    group = 1
                    queries.append(f"DELETE FROM DAYS WHERE id = {callback_data[2]}")
                    queries.append(f"UPDATE USERS SET event_id = NULL WHERE tg_id = {usr_id}")
                    queries.append(f"UPDATE USERS SET last_keyboard = 1 WHERE tg_id = {usr_id}")
                    # info needed for notification
                    listeners = await get_event_listeners(callback_data[2], 'all', f"AND usr_id <> {usr_id}")
                    day = await get_query(f'''
                        SELECT DAYS.*, USERS.*, WEEKDAY_prm.*, CONTINIOUSDAY_prm.*
                        FROM DAYS
                        LEFT JOIN USERS ON (DAYS.who = USERS.tg_id)
                        LEFT JOIN WEEKDAY_prm ON (DAYS.id =  WEEKDAY_prm.day_id)
                        LEFT JOIN CONTINIOUSDAY_prm ON (DAYS.id =  CONTINIOUSDAY_prm.day_id)
                        WHERE DAYS.id = {callback_data[2]}
                        ORDER BY DAYS.day;
                    ''')
                    day = day[0]
                    author = await get_query(f"SELECT name FROM USERS WHERE tg_id = {usr_id}")
                    author = author[0]['name']
                    author = await author_link(author, usr_id)
                    msg = "Event was succesfully deleted!"
                    # send notification for everyone subscribed to event
                    await insert_data(queries)
                    if len(listeners) != 0:
                        msg = msg + "\n\nSubscribers and redactors of this event were notified about it"
                        notification = f" has just deleted event '{day['name']}'.\nEvent info:\n\n" + await get_day_row_info(day)
                        notification = f"User {author}" + notification
                        for listener in listeners:
                            await send_notification(listener['usr_id'], system_name, "Notification", notification, "Markdown")
                else:
                    group = 10
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
                    if callback_data[4] == 'True':
                        queries.append(f"DELETE FROM DAYS WHERE id = {callback_data[2]}")
                        queries.append(f"DELETE FROM link WHERE id1 = {callback_data[2]} AND format = 'days'")
                        msg = msg + f"\n\nEvent was deleted!"
                    else:
                        queries.append(f"DELETE FROM link WHERE usr_id = {usr_id} AND id1 = {callback_data[2]} AND opt = '{callback_data[3]}' AND format = 'days'")
                else:
                    msg = "Action aborted!"
            elif user_sts == 'MODIFY_PST':
                group = 2
                if callback_data[1].lower() == 'yes':
                    msg = f"If event is regular and period and period amount are not choosen, it will be deleted after exectuion. Or if event is continious"
                    msg = msg + " and end date is in past, it will be deleted"
                    queries.append(f"UPDATE DAYS SET delIfInPast = 'yes' WHERE id = {callback_data[3]}")
                else:
                    queries.append(f"UPDATE DAYS SET delIfInPast = 'no' WHERE id = {callback_data[3]}")
                    msg = f"Event wont be deleted unless you do it by yourself"
                msg = "Saved!\n\n" + msg
            elif user_sts == "EVENTS_ADD_CSV":
                group = 9
                if callback_data[1].lower() == "yes":
                    # not perfect, because it cannot catch errors
                    msg = "Events are being created asynchronously. It may take a few seconds."
                    subprocess.Popen(['bash', path_querries_launch, f"{path_querries}/{callback_data[3]}_main.sql"])
                else:
                    msg = "Action aborted!"
            elif user_sts == "NOTIFIC_DEL":
                group = 11
                if callback_data[1].lower() == "yes":
                    msg = config.lang_instance.get_text(usr_lang, 'DAYS_notifications.deleted')
                    queries.append(f"DELETE FROM DAYS_notifications WHERE id = {callback_data[2]}")
                else:
                    msg = "Action aborted!"
            elif user_sts == "ATTACHMENT_DELETE":
                group = 13
                if callback_data[1].lower() == "yes":
                    msg = config.lang_instance.get_text(usr_lang, 'FILES.attachment_deleted')
                    attachment = await get_query(f"SELECT system_path FROM DAYS_attachments WHERE id = {callback_data[2]}")
                    attachment = attachment[0]['system_path']
                    if os.path.isfile(path=attachment):
                        os.remove(path=attachment)
                    queries.append(f"DELETE FROM DAYS_attachments WHERE id = {callback_data[2]}")
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
        elif action_type == "PUB_EVNT_CHSN":
            keyboard = InlineKeyboardMarkup(row_width=2)
            button = InlineKeyboardButton(text="✅Subscribe to", callback_data=f"SUBSCRIBE_TO;{callback_data[1]};{callback_data[2]}")
            keyboard.insert(button)
            keyboard = await add_back_btn(12, keyboard)
            await edit_message(usr_id, config.lang_instance.get_text(usr_lang, "PUBLIC.action").replace('<event_name>', callback_data[2]), keyboard)
        elif action_type == "SUBSCRIBE_TO":
            queries.append(f"INSERT INTO link(usr_id, id1, opt, format) VALUES({usr_id}, {callback_data[1]}, 'look', 'days')")
            keyboard = await get_back_btn(12)
            await insert_data(queries)
            await edit_message(usr_id, config.lang_instance.get_text(usr_lang, "PUBLIC.confirm").replace('<event_name>', callback_data[2]), keyboard)
        elif action_type == "ATTACHMENT_CHOOSEN":
            queries.append(f"UPDATE USERS SET last_keyboard = 13 WHERE tg_id = {usr_id};")
            await confirm_choice(usr_id, callback_data[1], 13)
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
                # https://stackoverflow.com/questions/1835756/using-try-vs-if-in-python
                # extract some parameters for functions
                usr_info = await get_query(f"SELECT name, event_id, language FROM USERS WHERE tg_id = {usr_id}")
                usr_name = usr_info[0]['name']
                event_id = usr_info[0]['event_id']
                usr_lang = usr_info[0]['language']
                event_name = ""
                if event_id != None:
                    event_name = await get_query(f"SELECT name FROM DAYS WHERE DAYS.id = {event_id}")
                    if len(event_name) == 0:
                        event_name = ""
                    else:
                        event_name = event_name[0]['name']
                else:
                    event_id = 0
                result = await globals()[callback_data[1]](usr_id=usr_id, event_name=event_name, event_id=event_id, usr_name=usr_name, usr_lang = usr_lang)
    except Exception as e:
        msg = f"Ooops, an error ocured:\n {repr(e)}"
        traceback.print_exc()
        keyboard_gr = await get_query(f"SELECT last_keyboard FROM USERS WHERE tg_id = {usr_id}")
        if len(keyboard_gr) != 0:
            keyboard = await get_keyboard(group_id=keyboard_gr[0]['last_keyboard'], user_id=usr_id)
        await edit_message(usr_id, msg, keyboard)

async def send_msg(to : int, msg : str, parse_mode : str = None, disable_web_page_preview : bool = True, reply_markup : InlineKeyboardMarkup = None):
    # TODO telegram bot API has a limit of 100 buttons for inline keyboard.
    # It is possible to add more to an inline keyboard object, but only first 100 will be displayed.
    # One solution is to ask for <N> records and add '<' '>' buttons to ask next or previous <N> records
    # **************************************************************************************************
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
                line = msg[left:n+1]
                i = n + 1
            else:
                line = msg[left:right]
                i = right + 1
            if not(line == "" or line == '\n'):
                msg_list.append(line)
    else:
        msg_list.append(msg)
    querries = []
    for i in range(len(msg_list)):
        # attach keyboard only to last message
        if i == (len(msg_list) - 1):
            sent_msg = await bot.send_message(to, msg_list[i], parse_mode=parse_mode, disable_web_page_preview=disable_web_page_preview, reply_markup=reply_markup)
        else:
            sent_msg = await bot.send_message(to, msg_list[i], parse_mode=parse_mode, disable_web_page_preview=disable_web_page_preview)
        sent_msg_id = sent_msg.message_id
        query = f"INSERT INTO DAYS_messages(chat_id, msg_id) VALUES({to}, {sent_msg_id})"
        querries.append(query)
    await insert_data(querries)
    return sent_msg

async def edit_message(usr_id : int, text : str, reply_markup : InlineKeyboardMarkup = None, parse_mode : str = None):
    # TODO telegram bot API has a limit of 100 buttons for inline keyboard.
    # It is possible to add more to an inline keyboard object, but only first 100 will be displayed.
    # One solution is to ask for <N> records and add '<' '>' buttons to ask next or previous <N> records
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
    except BadRequest as e:
        error_code = e.args[0] if e.args else None
        if error_code.lower() == 'message_too_long':
            # IDK why but MessageIsTooLong exception is not being caught
            await send_msg(to=usr_id, msg=text, parse_mode=parse_mode)
            sent_msg = await send_msg(to=usr_id, msg="Message was sent in multiple messages, because it is too long", parse_mode=parse_mode, reply_markup=reply_markup)
            querries = [f"UPDATE USERS SET days_msg_id = {sent_msg.message_id} WHERE tg_id = {usr_id}"]
            await insert_data(querries)
        else:
            traceback.print_exc()
            await send_msg(usr_id, "An error ocured trying to modify main message:\n\n" + str(e))
    except Exception as e:
        traceback.print_exc()
        await send_msg(usr_id, "An error ocured trying to modify main message:\n\n" + str(e))

async def send_new_static_msg(usr_id : int, msg : str, reply_markup : InlineKeyboardMarkup = None, parse_mode : str = None):
    sent_message = await send_msg(to=usr_id, msg=msg, reply_markup=reply_markup, parse_mode=parse_mode)
    message_id = sent_message.message_id
    await insert_data([f"UPDATE USERS SET days_msg_id = {message_id} WHERE tg_id = {usr_id}"])
    return message_id

async def send_file(usr_id : int, path : str, label : str, keyboard : InlineKeyboardMarkup):
    message = await bot.send_document(usr_id, document=open(path, 'rb'))
    await edit_message(usr_id, label, keyboard)
    queries = [f"INSERT INTO DAYS_messages(chat_id, msg_id) VALUES({usr_id}, {message.message_id})"]
    await insert_data(queries)

async def send_file_by_id(usr_id : int, file_id : str, label : str, keyboard : InlineKeyboardMarkup):
    # too lazy lol
    try:
        message = await bot.send_document(usr_id, document=file_id)
    except BadRequest as e:
        message = await bot.send_photo(usr_id, photo=file_id)
    if label > "" or keyboard != None:
        await edit_message(usr_id, label, keyboard)
    queries = [f"INSERT INTO DAYS_messages(chat_id, msg_id) VALUES({usr_id}, {message.message_id})"]
    await insert_data(queries)

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
        to_disp = True
        if button_json['showif'] != None:
            to_disp = False
            # if at least one clause is true, then show. showif = first or second or third...
            for clause in button_json['showif'].split(','):
                if await globals()[clause](usr_id=user_id):
                    to_disp = True
                    break
        if not to_disp:
            continue
        data = button_json['func']
        if data == None:
            data = button_json['nextGroup']
        last_keyboard = button_json['nextGroup']
        if last_keyboard is None:
            last_keyboard = button_json['group_num']
        data = "BUTTON_PRESSED" + ";" + data + ";" + button_json['group_num'] + ";" + last_keyboard + ";" + button_json['sts_user']
        button = InlineKeyboardButton(text=button_json['text'], callback_data=data)
        keyboard.insert(button)
    return keyboard

async def escape_mysql(msg : str):
    for char in  escape_chars:
        msg = msg.replace(char, '\\' + char)
    return msg

async def parse_msg(msg: str, slash : bool = True):
    if slash:
        # escapes slash with a slash
        msg = msg.replace('\\', '\\\\')
    for char in Markdown_ch_all:
        msg = msg.replace(char, '\\' + char)
    return msg



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

async def get_today(delta : timedelta = None):
    if delta == None:
        delta = timedelta(days=0)
    return (datetime.now(timezone('Europe/Kiev')) + delta).date()

async def get_today_time(format : str, delta : timedelta = None):
    if delta == None:
        delta = timedelta(minutes=0)
    return (datetime.now(timezone('Europe/Kiev')) + delta).strftime(format)

async def get_infinite_date():
    return datetime(9999, 1, 1).date()

async def get_tiny_date():
    return datetime(1, 1, 1).date()
    
async def reschedule(day : dict) -> None:

    if not day['format'] in ['0', '2']:
        return None

    if day["period"] == None or int(day["period_am"]) == None:
        # if these fields are not provided event does not need to be rescheduled
        if day['delIfInPast'] == "yes" and day['format'] == '0':
            listeners = await get_event_listeners(day['id'], 'all')
            await insert_data([f"DELETE FROM DAYS WHERE id = {day['id']}"])
            # does this notification work at all??? TODO - check
            for listener in listeners:
                await send_notification(listener['usr_id'], system_name, "Notification", f"Regular event {day['name']} was deleted, because period and period amount were not provided. Therefore it executes only once")
        return None
    vDate = datetime.strptime(day['day'], "%Y-%m-%d").date()
    period = day["period"]
    amount = int(day["period_am"])
    vDate = await get_new_date(vDate, period, amount)
    if day['format'] == '2':
        await check_period(vDate, day['day_start'], day['day_end'])
    querris = []
    querris.append(f'UPDATE DAYS SET day = DATE("{vDate.strftime("%Y-%m-%d")}") WHERE id = {day["id"]}')
    await insert_data(querris)
    return vDate.strftime("%Y-%m-%d")

async def get_day_info(day : dict, frmt : int):
    date = day['day']
    descr = day['descr']
    if date == None:
        date = default_not_data
    if descr == None:
        descr = default_not_data
    if frmt == 0:
        return f"Event is called {day['name']}. It is scheduled on {date}.\n\nEvent is about {descr}"
    elif frmt == 1:
        return f"{day['name']}.\n\nIt is about {descr}"

async def author_link(name : str, tg_id : str):
    return f"[{name}](tg://user?id={tg_id})"

async def isYes(text : str):
    return (text in ['y', 'ye', 'yes', 'yeah'])


async def calculate_events(formats : list, ids : list = [], delta_days : timedelta = None, force : bool = False):
    # 0 - regular events
    # 1 - irregular events
    # 2 - continious events
    # force - IGNORE!
    response = ""
    queris = []
    vToday = await get_today(delta_days)
    if 0 in formats:
        days = await get_query("SELECT * FROM DAYS WHERE format = 0")
        for day in days:
            if day['day'] == None:
                continue
            if len(ids) > 0 and day['id'] not in ids:
                continue
            vDate = datetime.strptime(day['day'], "%Y-%m-%d").date()
            if vDate < vToday:
                vNewDate = await reschedule(day)
                if vNewDate != None:
                    response = response + "* Event " + f"{day['name']} " + f" is scheduled on {vNewDate}\n\n"
    if 1 in formats:
        days = await get_query("SELECT * FROM DAYS INNER JOIN WEEKDAY_prm ON DAYS.id = WEEKDAY_prm.day_id WHERE format = 1 ORDER BY day;")
        for day in days:
            if len(ids) > 0 and day['id'] not in ids:
                continue
            if day['month'] == None or day['weekday'] == None or day['occurence'] == None:
                continue

            if day['day'] != None:
                vDate = datetime.strptime(day['day'], "%Y-%m-%d").date()
            if day['day'] == None or vDate < vToday:
                v_date = find_day_in_month(datetime.now().year, int(day['month']), int(day['weekday']), int(day['occurence']))
                if v_date < vToday:
                    v_date = find_day_in_month(datetime.now().year + 1, int(day['month']), int(day['weekday']), int(day['occurence']))
                queris.append(f"UPDATE DAYS SET day = '{v_date}' WHERE id = {day['id']}")
                response = response + "* Event " + f"{day['descr']} " + f" is scheduled on {v_date}\n\n"

    if 2 in formats:
        days = await get_query("SELECT * FROM DAYS INNER JOIN CONTINIOUSDAY_prm ON DAYS.id = CONTINIOUSDAY_prm.day_id WHERE format = 2 ORDER BY day;")
        for day in days:
            if len(ids) > 0 and day['id'] not in ids:
                continue
            if day['day'] == None:
                continue
            vDate = datetime.strptime(day['day'], "%Y-%m-%d").date()
            vStart = day['day_start']
            vEnd = day['day_end']
            if vStart == None:
                vStart = await get_tiny_date()
            else:
                vStart = datetime.strptime(vStart, "%Y-%m-%d").date()
            if vEnd == None:
                vEnd = await get_infinite_date()
            else:
                vEnd = datetime.strptime(vEnd, "%Y-%m-%d").date()
            # IF today is in period -> reschedule to next
            if vToday > vStart and vToday <= vEnd:
                try:
                    vNewDate = await reschedule(day)
                    response = response + "* Event " + f"{day['name']} " + f" is scheduled on {vNewDate}\n\n"
                except DateOutOfBounds as e:
                    if day['delIfInPast'] == "yes":
                        # send notification that event was deleted, because next calculated date is after end date
                        queris.append(f"DELETE FROM DAYS WHERE id = {day['id']}")
                        listeners = await get_event_listeners(day['id'], 'all')
                        for listener in listeners:
                            await send_notification(listener['usr_id'], system_name, "Notification", f"Continious event {day['name']} was deleted, because {str(e)}")
            elif vToday > vEnd and day['delIfInPast'] == "yes":
                # send notification that event was deleted, today is later than end date
                queris.append(f"DELETE FROM DAYS WHERE id = {day['id']}")
                listeners = await get_event_listeners(day['id'], 'all')
                for listener in listeners:
                    await send_notification(listener['usr_id'], system_name, "Notification", f"Continious event {day['name']} was deleted, because today is {vToday} and end date is {vEnd}")
    await insert_data(queris)
    return response

async def get_event_listeners(event_id : int, opt : str, clause : str  = ""):
    # clause - additional sql query
    if not opt in ['all', 'look', 'modify']:
        raise SystemError
    if opt == 'all':
        query = f"SELECT DISTINCT usr_id FROM link WHERE id1 = {event_id} AND link.format = 'days' AND (link.opt = 'look' OR link.opt = 'modify') {clause}"
        t =  await get_query(query)
        return await get_query(query)
    else:
        query = f"SELECT * FROM link WHERE id1 = {event_id} AND link.format = 'days' AND link.opt = '{opt}' {clause}"
        return await get_query(query)

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

async def check_period(date : date, day_start : str, day_end : str):
    if day_start == None:
        return
    if day_end != None:
        day_end = datetime.strptime(day_end, "%Y-%m-%d").date()
        if date > day_end:
            raise DateOutOfBounds(f"Calculated date is {date} while end date is {day_end}")

async def get_new_date(iDate : date, period : str, amount : int):
    if period == "year":
        try:
            iDate = iDate.replace(year = iDate.year + amount)
        except ValueError:
            # exception for 'visokosniy' year (29 february transfers to 1 march)
            iDate = iDate + (date(iDate.year + amount, 1, 1) - date(iDate.year, 1, 1))
    elif period == "week":
        iDate = iDate + timedelta(days=(7 * amount))
    elif period == "day":
        iDate = iDate + timedelta(days=(1 * amount))
    elif period == "month":
        # why do I use this insted of timedelta?
        iDate = await add_months(iDate, amount)
    return iDate

async def send_notification(to : int, sender : str, header : str, body : str, parse_mode : str = None):
    await send_msg(to, f"{header}\n\n{body}\n\n© {sender}", parse_mode)

async def format_irregular(day : dict):
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
    return day

# DAYS_notifications
async def print_notific(**kwargs):
    usr_id = kwargs['usr_id']
    event_name = kwargs['event_name']
    notifications = await get_query(f"SELECT * FROM DAYS_notifications WHERE day_id = (SELECT event_id FROM USERS WHERE tg_id = {usr_id})")
    msg = f"There are {len(notifications)} notifications for event {event_name}:\n\n"
    for notific in notifications:
        row = f"* {notific_text[notific['when_date']]} at {notific['when_time']}" 
        msg = msg + row + "\n\n"
    reply_markup = await get_back_btn(keyboard_id=11)
    await edit_message(usr_id, msg, reply_markup)
    return ""

async def pick_notific(**kwargs):
    usr_id = kwargs['usr_id']
    event_id = kwargs['event_id']
    event_name = kwargs['event_name']
    usr_lang = kwargs['usr_lang']
    notifics = await get_query(f"SELECT * FROM DAYS_notifications WHERE day_id = {event_id}")
    reply_markup = await get_back_btn(keyboard_id=11)
    if len(notifics) == 0:
        txt = config.lang_instance.get_text(usr_lang, 'DAYS_notifications.no_notifics').replace('<event_name>', event_name)
        await edit_message(usr_id, txt, reply_markup)
    else:
        keyboard = InlineKeyboardMarkup(row_width=2)
        for notific in notifics:
            button = InlineKeyboardButton(text=notific_text[notific['when_date']] + " - " + notific['when_time'], callback_data=f'NOTIFIC_CHOOSEN;{notific["id"]}')
            keyboard.insert(button)
        keyboard = await add_back_btn(11, keyboard)
        await edit_message(usr_id, config.lang_instance.get_text(usr_lang, 'DAYS_notifications.choose').replace('<event_name>', event_name), keyboard)


async def add_notific(**kwargs):
    usr_id = kwargs['usr_id']
    keyboard = InlineKeyboardMarkup(row_width=len(notific_text) // 3)
    for ntf_key, ntf_val in notific_text.items():
        button = InlineKeyboardButton(text=ntf_val, callback_data=f'NOTIFIC_OPT_CHOOSEN;{ntf_key}')
        keyboard.insert(button)
    keyboard = await add_back_btn(11, keyboard)
    await edit_message(usr_id, f"Chose notification day", keyboard)

async def add_notific_hour(usr_id, usr_lang):
    keyboard = InlineKeyboardMarkup(row_width=4)
    for i in range(24):
        txt = str(i)
        txt = txt if len(txt) == 2 else '0' + txt
        button = InlineKeyboardButton(text=txt, callback_data=f'NOTIFIC_HH_CHOOSEN;{txt}')
        keyboard.insert(button)
    keyboard = await add_back_btn(11, keyboard)
    await edit_message(usr_id, f"Chose notification hour", keyboard)

async def add_notific_minutes(usr_id, hour, usr_lang):
    keyboard = InlineKeyboardMarkup(row_width=3)
    for i in range(0, 60, 5):
        mm = str(i)
        mm = mm if len(mm) == 2 else '0' + mm
        txt = hour + " : " + mm        
        button = InlineKeyboardButton(text=txt, callback_data=f'NOTIFIC_MM_CHOOSEN;{mm}')
        keyboard.insert(button)
    keyboard = await add_back_btn(11, keyboard)
    await edit_message(usr_id, f"Chose notification minutes", keyboard)

async def create_notific(usr_id, data, event_id, usr_lang):
    # data = <DAYS_notifications.when_date> ; <DAYS_notifications.when_time>
    data = data.split(';')
    querries = [f"INSERT INTO DAYS_notifications (day_id, when_date, when_time) VALUES({event_id}, '{data[0]}', '{data[1]}')"]
    await insert_data(querries)
    keyboard = await get_back_btn(11)
    await edit_message(usr_id, config.lang_instance.get_text(usr_lang, 'DAYS_notifications.created'), keyboard)


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
