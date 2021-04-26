from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ConversationHandler
from bot.conversationList import *
from app.models import *
from dotenv import load_dotenv
import os

basedir = os.path.abspath(os.path.dirname(''))
load_dotenv(os.path.join(basedir, '.env'))
MANAGER = os.environ.get('MANAGER')


def start(update, context):
    user = Bot_users.objects.filter(user_id=update.message.chat.id)
    managers = list(map(int, MANAGER.split()))
    

    if update.message.chat.id in managers:
        dwoidhoqw = 0
        return ConversationHandler.END
    elif user:
        #______________main manu __________________
        #user = Bot_users.objects.get(user_id=update.message.chat.id)
        #login = user.login
        #if user.who == 'foreman':
        #    obj = Foreman.objects.get(login=login).obj
        #else:
        #    obj = Client.objects.get(login=login).obj
        #objects_list = [[i.title] for i in obj.all()]
        #update.message.reply_text('Все объекты', reply_markup=ReplyKeyboardMarkup(keyboard=objects_list, resize_keyboard=True))
        #return ConversationHandler.END
        sth = 0
    else:
        update.message.reply_text('Авторизация как', reply_markup=ReplyKeyboardMarkup(keyboard=[['Прораб'], ['Клиент']], resize_keyboard=True))
        return LOGIN_AS
def reload(update, context):
    managers = list(map(int, MANAGER.split()))
    if not update.message.chat.id in managers:
        if Bot_users.objects.filter(user_id=update.message.chat.id):
            empty_material = Material.objects.filter(price=None)
            empty_salary = Salary.objects.filter(price=None)
            if empty_material or empty_salary:
                qwerty = 0 # do nothing
            update.message.reply_text('Главное меню', reply_markup=ReplyKeyboardMarkup(keyboard=[['Объекты'], ['Выйти из аккаунта']], resize_keyboard=True))
            return MAIN_MENU
        else:
            update.message.reply_text('Вы не зарегистрированы. нажмите /start')


def main_menu(update, context):
    bot = context.bot
    text = update.message.text
    if text == 'Объекты':
        user = Bot_users.objects.get(user_id=update.message.chat.id)
        login = user.login
        if user.who == 'foreman':
            obj = Foreman.objects.get(login=login).obj
        else:
            obj = Client.objects.get(login=login).obj
        
        objects_list = [[i.title] for i in obj.all()]
        objects_list.append(['Главное меню'])
        update.message.reply_text('Все объекты', reply_markup=ReplyKeyboardMarkup(keyboard=objects_list, resize_keyboard=True))
        return ConversationHandler.END
    if text == 'Выйти из аккаунта':
        update.message.reply_text('Вы действительно хотите выйти из бота?', reply_markup=ReplyKeyboardMarkup(keyboard=[['Да', 'Назад']], resize_keyboard=True))
        return EXIT_OR_NO

def exit_or_no(update, context):
    bot = context.bot
    text = update.message.text
    if text == 'Назад':
        update.message.reply_text('Главное меню', reply_markup=ReplyKeyboardMarkup(keyboard=[['Объекты'], ['Выйти из аккаунта']], resize_keyboard=True))
        return MAIN_MENU
    elif text == 'Да':
        user = Bot_users.objects.get(user_id=update.message.chat.id)
        user.delete()
        update.message.reply_text('Вы вышли из аккаунта. Нажмите /start для входа ', reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
        return ConversationHandler.END



def objects(update, context):
    
    bot=context.bot
    text = update.message.text
    # delete empty Material or Salary object, which was not finished
    
    materials = Material.objects.filter(price=None)
    for m in materials:
        m.delete()
    salaries = Salary.objects.filter(price=None)
    for s in salaries:
        s.delete()

    try:

        who = Bot_users.objects.get(user_id=update.message.chat.id).who
        foreman = Foreman.objects.get(obj__title=text)
        if who == 'foreman':
            obj = Object.objects.get(title=text)
            
            i_material = InlineKeyboardButton(text='Материалы', callback_data='spend-money-to-material_{}'.format(text))
            i_salary = InlineKeyboardButton(text='Иш хакки', callback_data='spend-money-for-salary_{}'.format(text))
            i_back = InlineKeyboardButton(text='Назад', callback_data='back-to-objects_foreman')
            d = bot.send_message(update.message.chat.id, 'Тратить деньги на...', reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
            bot.delete_message(update.message.chat.id, d.message_id)
            bot.send_message(update.message.chat.id, 'Остаток денег:{} сумм, {} доллар\nТратить деньги на...'.format(obj.price_summ, obj.price_dollar), reply_markup=InlineKeyboardMarkup([[i_material], [i_salary], [i_back]]))

            return SPEND_MONEY_FOR
        else:
            obj = Object.objects.get(title=text)
            i_material_flat = InlineKeyboardButton(text='Материалы квартиры', callback_data='inf-material-flat_{}'.format(text))
            i_material_plot = InlineKeyboardButton(text='Материалы участки', callback_data='inf-material-plot_{}'.format(text))
            i_salary = InlineKeyboardButton(text='Иш хакки', callback_data='inf-salary_{}'.format(text))
            i_back = InlineKeyboardButton(text='Назад', callback_data='back-to-objects_client')
            d = bot.send_message(update.message.chat.id, 'Показать информацию о ...', reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
            bot.delete_message(update.message.chat.id, d.message_id)
            bot.send_message(update.message.chat.id, 'Остаток денег: {} сумм, {} доллар \nПоказать информацию о ...'.format(obj.price_summ, obj.price_dollar), reply_markup=InlineKeyboardMarkup([[i_material_flat], [i_material_plot], [i_salary], [i_back]]))
            return SHOW_INF_ABOUT
    except:
        update.message.reply_text('Нет такого объекта')


def cancel(update, context):
    bot = context.bot
    if not Bot_users.objects.filter(user_id=update.message.chat.id):
        get = update.message.reply_text('Нажмите /start для повторного входа в бота', reply_markup=ReplyKeyboardMarkup(keyboard=[['/start']], resize_keyboard=True))
        bot.delete_message(update.message.chat.id, get.message_id-2)
        bot.delete_message(update.message.chat.id, get.message_id-1)
        return ConversationHandler.END