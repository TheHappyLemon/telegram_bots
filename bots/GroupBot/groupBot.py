from telegram import *
from telegram.ext import *
from constants import token, no_name, mems, bs_chat, adm_id, test_chat
from random import randint
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
import pytz

class tBot:

    def __init__(self) -> None:
        self.up = Updater(token, use_context=True)
        self.dp = self.up.dispatcher
        self.isOn = True
        self.dp.add_handler(CommandHandler("disable", self.__disable__))
        self.dp.add_handler(CommandHandler("enable", self.__enable__))
        self.dp.add_handler(CommandHandler("check", self.__check__))
        self.dp.add_handler(CommandHandler("all", self.__all__))
        self.dp.add_handler(CommandHandler("add", self.__add__))
        self.dp.add_handler(CommandHandler("log", self.__log__))
        self.dp.add_handler(CommandHandler("help", self.__help__))
        self.dp.add_handler(CommandHandler("goodboy", self.__boy__))
        self.dp.add_handler(CommandHandler("my_jobs", self.__job__))
        self.dp.add_handler(CommandHandler("flip_week", self.__chg_week__))
        self.is_league_week = False
        if mems != {}:
            self.members = mems
        else:
            self.members = {}

    def run(self):
        print("running")
        self.up.start_polling()
        self.up.idle()

    def __get_name__(self, user):
        name = user["username"]
        if name == None:
            return no_name
        return name

    def __disable__(self, update, context):
        if not self.isOn:
           context.bot.send_message(chat_id=update.effective_chat.id, text="Already disabled...")
           return
        self.isOn = False
        context.bot.send_message(chat_id=update.effective_chat.id, text="Disabled!\n\nWill not remind until enabled")

    def __enable__(self, update, context):
        if self.isOn:
           context.bot.send_message(chat_id=update.effective_chat.id, text="Already enabled!")
           return
        self.isOn = True
        context.bot.send_message(chat_id=update.effective_chat.id, text="Enabled\n\nWill remind until disabled")

    def __check__(self, update, context):
        user = update.message.from_user
        msg = f"I'm alive! Thanks for asking, {self.__get_name__(user)}.\n\n"
        if update.effective_chat.id == int(bs_chat) or update.effective_chat.id == int(test_chat):
            msg = msg + f"is_league_week = {self.is_league_week}\nEnabled={self.isOn}"
        context.bot.send_message(chat_id=update.effective_chat.id, text= msg)

    def __all__(self, update, context):
        chat_id = str(update.effective_chat.id)
        if len(self.members) == 0:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Who am I supposed to mention... 😭")
            return
        mention = ""
        for member in self.members[chat_id]:
            mention = mention + "["+self.members[chat_id][member]+"](tg://user?id="+str(member)+")" + "\n"
        mention = mention + "\nGET OVER HERE"
        context.bot.send_message(chat_id=update.effective_chat.id, text=mention, parse_mode="Markdown")


    def __add__(self, update, context):
        user = update.message.from_user
        chat_id = str(update.effective_chat.id)
        if chat_id not in self.members:
            self.members[chat_id] = {}
            self.__write_to_log__("added chat with id = " + chat_id + '\n')
        if user["id"] not in self.members[chat_id]:
            self.members[chat_id][user["id"]] = self.__get_name__(user)
            self.__write_to_log__("added user to chat " + chat_id + ". User id = " + str(user["id"]) + " User name = " +  self.members[chat_id][user["id"]] + '\n')
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="I already know you 🙄")
            return
        context.bot.send_message(chat_id=update.effective_chat.id, text="Added " + user["username"] + "!")

    def __help__(self, update, context):
        answ = "Existing commands:\n1)check - ping me\n2)all - mention everybody addded with 'add comand'\n3)add - add user to mention\n4)help - help"
        context.bot.send_message(chat_id=update.effective_chat.id, text=answ)

    def __write_to_log__(self, msg):
        with open(file='log.txt', mode='a', encoding="utf-8") as my_file:
            my_file.writelines(msg)

    def __log__(self, update, context):
        user = update.message.from_user
        if user["id"] != adm_id:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Only for admin :-)")
            return
        self.__write_to_log__(str(self.members))
        context.bot.send_message(chat_id=update.effective_chat.id, text="Wrote to log succesfully")

    def __boy__(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text="Under construction...")

    def __job__(self, update, context):
        f = open('jobs.txt', 'w')
        scheduler.print_jobs(out = f)
        f.flush()
        f.close()
        f = open('jobs.txt', 'r')
        text = f.read()
        context.bot.send_message(chat_id=update.effective_chat.id, text=text)

    def __chg_week__(self, update, context):
        user = update.message.from_user
        if user["id"] != adm_id:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Only for admin :-)")
            return
        msg = f"is_league_week was {self.is_league_week}. Now it is: "
        self.is_league_week = not self.is_league_week
        msg = msg + str(self.is_league_week)
        context.bot.send_message(chat_id=update.effective_chat.id, text=msg)


def remind_club_league(iBot : tBot):
    if not iBot.isOn:
       return
    msg = "Remind!\n\n"
    if iBot.is_league_week:
        msg = msg + "Club league day has started. Do not forget to play it 💪😉"
    else:
        msg = msg + "It is QUEST week. Do not forget to complete them 💪😉"
    msg = msg + "\n"
    for member in iBot.members[bs_chat]:
        msg = msg + "["+iBot.members[bs_chat][member]+"](tg://user?id="+str(member)+")" + "\n"
    msg = msg + "\n\n" + "gl hf"
    if datetime.today().weekday() == 6:
        iBot.is_league_week = not iBot.is_league_week
    iBot.dp.bot.send_message(chat_id=bs_chat, text=msg, parse_mode="Markdown")


if __name__ == "__main__":
    bot = tBot()
    scheduler = BackgroundScheduler()
    trigger = CronTrigger(day_of_week='wed,fri,sun', hour=17, minute=0, timezone=pytz.timezone('Europe/Kiev'))
    scheduler.add_job(remind_club_league, trigger=trigger, args=(bot, ))
    scheduler.start()
    bot.run()
