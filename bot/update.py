from telegram import Bot
from telegram.ext import Dispatcher, ConversationHandler, PicklePersistence
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from bot.main import *
from bot.login import *
from bot.conversationList import *
from bot.spend_money import *
from bot.show_inf import show_inf_about
from bot.manager import *
from app.models import Object
from dotenv import load_dotenv
import os

basedir = os.path.abspath(os.path.dirname(''))
load_dotenv(os.path.join(basedir, '.env'))
TOKEN = os.environ.get('TOKEN')
WHERE = os.environ.get('WHERE')
bot_obj = Bot(TOKEN)
persistence = PicklePersistence(filename='filebot')
if WHERE == 'SERVER':
    updater = 1213
    dp = Dispatcher(bot_obj, None, workers=0, use_context=True, persistence=persistence)
else:
    updater = Updater(token=TOKEN, use_context=True, persistence=persistence)
    dp = updater.dispatcher

objects_list = [i.title for i in Object.objects.all()]


login_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        LOGIN_AS: [MessageHandler(Filters.text, login_as)],
        SEND_LOGIN: [MessageHandler(Filters.text, send_login)],
        SEND_PASSWORD: [MessageHandler(Filters.text, send_password)],

    },
    fallbacks = []
)

reload_handler = ConversationHandler(
    entry_points=[CommandHandler('reload', reload), MessageHandler(Filters.text(['Дальше', 'Главное меню']), reload)],
    states={
        MAIN_MENU: [MessageHandler(Filters.text(['Выйти из аккаунта', 'Объекты']), main_menu)],
        EXIT_OR_NO: [MessageHandler(Filters.text(['Да', 'Назад']), exit_or_no)],
    },
    fallbacks=[CommandHandler('cancel', cancel)],
    persistent=True,
    name='reload'
)

select_objects = ConversationHandler(
    entry_points=[MessageHandler(Filters.text, objects)],
    states={
        #_______ spend money:
        # for Salary
        SEND_TYPE_SALARY: [MessageHandler(Filters.text, send_type_salary)],
        SPEND_MONEY_FOR: [CallbackQueryHandler(spend_money_for)],
        SEND_TITLE_SALARY: [MessageHandler(Filters.text, send_title_salary)],   
        SEND_SUMM_OR_DOLLAR_SALARY: [MessageHandler(Filters.text, send_summ_or_dollar_salar)],
        SEND_PRICE_SALARY: [MessageHandler(Filters.text, send_price_salary)],
        # For materials
        SEND_TYPE_MATERIAL: [MessageHandler(Filters.text, send_type_material)],
        SEND_TITLE_MATERIAL: [MessageHandler(Filters.text, send_title_material)],
        SELECT_MEASUREMENT: [MessageHandler(Filters.text, select_measurement)],
        SEND_AMOUNT: [MessageHandler(Filters.text, send_amount)],
        SEND_SUMM_OR_DOLLAR_MATERIAL: [MessageHandler(Filters.text, send_summ_or_dollar_material)],
        SEND_PRICE_MATERIAL: [MessageHandler(Filters.text, send_price_material)],
        # ______ show inf
        SHOW_INF_ABOUT: [CallbackQueryHandler(show_inf_about)],
    },
    fallbacks=[CommandHandler('cancel', cancel)],
    persistent=True,
    name='object'


)

manager_handler = ConversationHandler(
    entry_points=[CommandHandler('manager', enter_manager)],
    states = {
        MAIN_MENU_MANAGER: [MessageHandler(Filters.text(['Создать объект', 'Пополнить счёт', 'Создать иш хакки', 'Создать материал']), main_menu_manager)],
        SEND_OBJECT_TITLE: [MessageHandler(Filters.text, send_object_title)],
        SEND_OBJECT_PRICE_DOLLAR: [MessageHandler(Filters.text, send_object_price_dollar)],
        SEND_OBJECT_PRICE_SUMM: [MessageHandler(Filters.text, send_object_price_summ)],
        #transfering
        REPLENISH: [CallbackQueryHandler(replenish)],
        SEND_TRANS_OBJ: [CallbackQueryHandler(send_trans_obj)],
        SEND_TRANS_SUMM_OR_DOLLAR: [CallbackQueryHandler(send_trans_summ_or_dollar)],
        SEND_TRANS_PRICE: [MessageHandler(Filters.text, send_trans_price)],
        #Create material

        CREATE_MATERIAL_send_object_title: [MessageHandler(Filters.text, create_material_send_object_title)],
        CREATE_MATERIAL_SEND_TYPE: [MessageHandler(Filters.text, create_material_send_type)],
        CREATE_MATERIAL_send_material_title: [MessageHandler(Filters.text, create_material_send_material_title)],
        CREATE_MATERIAL_SELECT_MEASUREMENT: [MessageHandler(Filters.text, create_material_select_measurement)],
        CREATE_MATERIAL_SEND_AMOUNT: [MessageHandler(Filters.text, create_material_send_amount)],
        CREATE_MATERIAL_SEND_SUMM_OR_DOLLAR_MATERIAL: [MessageHandler(Filters.text, create_material_send_summ_or_dollar_material)],
        CREATE_MATERIAL_SEND_PRICE_MATERIAL: [MessageHandler(Filters.text, create_material_send_price_material)],

        #create salary
        CREATE_SALARY_send_object_title: [MessageHandler(Filters.text, create_salary_send_object_title)],
        CREATE_SALARY_send_type: [MessageHandler(Filters.text, create_salary_send_type)],
        CREATE_SALARY_send_salary_title: [MessageHandler(Filters.text, create_salary_send_salary_title)],
        CREATE_SALARY_SEND_SUMM_OR_DOLLAR_SALARY: [MessageHandler(Filters.text, create_salary_send_summ_or_dollar_salary)],
        CREATE_SALARY_SEND_PRICE_SALARY: [MessageHandler(Filters.text, create_salary_send_price_salary)]

        

    },
    fallbacks = [CommandHandler('cancel', cancel)],
    persistent=True,
    name='manager'

)

dp.add_handler(login_handler)


dp.add_handler(manager_handler)
dp.add_handler(reload_handler)
dp.add_handler(CommandHandler('cancel', cancel))
dp.add_handler(select_objects)