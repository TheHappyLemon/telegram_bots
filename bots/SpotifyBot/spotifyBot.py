from telegram import *
from telegram.ext import *
from constants import *
from os import kill, getpid, environ, execl, getenv
import sys
from random import randint
from spotifyClass import spotifyUpdater

import signal

'''
TODO
for update playlist check when message was sent to
prevent spam. When ending processing - save time
when start proccesing - check if message.date is > than saved
also maybe put datetime transfrom into separate module useful
'''

class tBot:

    def __init__(self) -> None:
        self.up = Updater(token, use_context=True)
        self.dp = self.up.dispatcher
        self.dp.add_handler(CommandHandler("start", self.__start__))
        self.dp.add_handler(CommandHandler("ping", self.__ping__))
        self.dp.add_handler(CommandHandler("restart", self.__restart__))
        self.dp.add_handler(MessageHandler(Filters.text, self.__message_handler__))
        self.is_updating_spotify = False
        self.need_answ = False
        self.spoti = spotifyUpdater()

    def __ping__(self, update, context):
        user = update.message.from_user
        if not self.__check_permission__(user["id"], "admin"):
            return
        context.bot.send_message(chat_id=update.effective_chat.id, text="Allive,  " + user["username"] + "!")

    def __restart__(self, update, context):
        user = update.message.from_user
        if not self.__check_permission__(user["id"], "admin"):
            return
        context.bot.send_message(chat_id=update.effective_chat.id, text="Restarting myself!")
        environ["WAS_RESTARTED"] = "True"
        environ["RESTARTED_BY"]  = str(user["id"])
        execl(sys.executable, sys.executable, *sys.argv)

    def run(self):
        self.up.start_polling()
        self.up.idle()

    def __yes__(self, update, context):
        user = update.message.from_user
        if self.__check_permission__(user["id"], "spotify") and self.need_answ:
            update.message.reply_text(self.spoti.add_tracks())
            self.need_answ = False
        else:
            update.message.reply_text(answers[randint(0, len(answers) - 1)])


    def __no__(self, update, context):
        user = update.message.from_user
        if self.__check_permission__(user["id"], "spotify") and self.need_answ:
            self.spoti.clear_gathered()
            self.need_answ = False
            update.message.reply_text("Ok, forgetting these rn!")
        else:
            update.message.reply_text(answers[randint(0, len(answers) - 1)])

    def __update_playlist__(self, update, context):
        songs = ""

        user = update.message.from_user
        if self.is_updating_spotify:
            update.message.reply_text("I'm still proccesing previous request...")
            return
        if self.__check_permission__(user["id"], "spotify") and not self.is_updating_spotify:
            self.is_updating_spotify = True
            update.message.reply_text(self.spoti.get_header())

            songs = self.spoti.gather_songs()
            for i in range(0, len(songs), 4096):
                update.message.reply_text(songs[i:i+4096])

            buttons = self.__form_buttons__(user["id"], conf_buttons)
            context.bot.send_message(chat_id=update.effective_chat.id, text="Should I add them, " +  user["username"] + "?",
                          reply_markup = ReplyKeyboardMarkup(buttons))
            self.need_answ = True
            self.is_updating_spotify = False
            #spoti.add_new_tracks()
            #update.message.reply_text(spoti.get_response())

    def __kill_bot__(self, update):
        user = update.message.from_user
        if self.__check_permission__(user["id"], "admin"):
            update.message.reply_text("Killing myself...")
            kill(getpid(), signal.SIGINT)

    def __message_handler__(self, update, context):
        try:
            func = getattr(self, "__" + update.message.text.replace(" ", "_").lower() + "__")
            func(update, context)
        except AttributeError:
            print('sry')
            context.bot.send_message(chat_id=update.effective_chat.id, text=answers[randint(0, len(answers) - 1)])

        if update.message.text in main_buttons:
            pass

    def __check_permission__(self, user_id, must_be):
        if user_id in user_roles:
            if 'admin' in user_roles[user_id]:
                return True
            return must_be in user_roles[user_id]
        return False

    def __form_buttons__(self, user_id, source):
        buttons = []
        for button in source:
            for role in user_roles[user_id]:
                if role in source[button] or role == "admin":
                    buttons.append([KeyboardButton(button)])
                    break
        return buttons

    def __start__(self, update, context):
        user = update.message.from_user
        buttons = self.__form_buttons__(user["id"], main_buttons)
        context.bot.send_message(chat_id=update.effective_chat.id, text="Hello,  " + user["username"],
                                  reply_markup = ReplyKeyboardMarkup(buttons))


if __name__ == "__main__":
    bot = tBot()
    bot.run()
