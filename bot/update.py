from telegram import Bot
from telegram.ext import Dispatcher, ConversationHandler
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from bot.main import *
from bot.login import *
from bot.conversationList import *
from bot.spend_money import *
from bot.show_inf import show_inf_about
from dotenv import load_dotenv
import os

basedir = os.path.abspath(os.path.dirname(''))
load_dotenv(os.path.join(basedir, '.env'))
TOKEN = os.environ.get('TOKEN')
WHERE = os.environ.get('WHERE')
bot_obj = Bot(TOKEN)
if WHERE == 'SERVER':
    dp = Dispatcher(bot_obj, None, workers=0, use_context=True)
else:
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher

login_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        LOGIN_AS: [MessageHandler(Filters.text, login_as)],
        SEND_LOGIN: [MessageHandler(Filters.text, send_login)],
        SEND_PASSWORD: [MessageHandler(Filters.text, send_password)],

    },
    fallbacks = []
)

select_objects = ConversationHandler(
    entry_points=[MessageHandler(Filters.text, objects)],
    states={
        #_______ spend money:
        # for Salary
        SPEND_MONEY_FOR: [CallbackQueryHandler(spend_money_for)],
        SEND_TITLE_SALARY: [MessageHandler(Filters.text, send_title_salary)],   
        SEND_SUMM_OR_DOLLAR_SALARY: [MessageHandler(Filters.text, send_summ_or_dollar_salar)],
        SEND_PRICE_SALARY: [MessageHandler(Filters.text, send_price_salary)],
        # For materials
        SEND_TITLE_MATERIAL: [MessageHandler(Filters.text, send_title_material)],
        SELECT_MEASUREMENT: [MessageHandler(Filters.text, select_measurement)],
        SEND_AMOUNT: [MessageHandler(Filters.text, send_amount)],
        SEND_SUMM_OR_DOLLAR_MATERIAL: [MessageHandler(Filters.text, send_summ_or_dollar_material)],
        SEND_PRICE_MATERIAL: [MessageHandler(Filters.text, send_price_material)],
        # ______ show inf
        SHOW_INF_ABOUT: [CallbackQueryHandler(show_inf_about)],
    },
    fallbacks=[],

)
dp.add_handler(login_handler)
dp.add_handler(select_objects)