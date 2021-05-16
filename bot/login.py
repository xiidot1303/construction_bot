from app.models import *
from telegram import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from bot.conversationList import *
from telegram.ext import ConversationHandler
def login_as(update, context):
    text = update.message.text
    if text == 'Прораб':
        obj = Bot_users.objects.get_or_create(user_id=update.message.chat.id, who = 'foreman')
       
    
    elif text == 'Клиент':
        obj = Bot_users.objects.get_or_create(user_id=update.message.chat.id, who = 'client')
    else:
        update.message.reply_text('Авторизация как')
        return LOGIN_AS    
    update.message.reply_text('Введите логин', reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
    return SEND_LOGIN


def send_login(update, context):
    login = update.message.text
    who = Bot_users.objects.get(user_id=update.message.chat.id).who
    if Bot_users.objects.filter(login=login, who=who):
        update.message.reply_text('Этот профиль используется другим пользователем, введите другой логин')
        return SEND_LOGIN
    check = Foreman.objects.filter(login=login)
    if not check:
        check = Client.objects.filter(login=login)
    
    if check:
        obj = Bot_users.objects.get(user_id=update.message.chat.id)
        obj.login = login
        obj.save()
        update.message.reply_text('Введите пароль')
        return SEND_PASSWORD
    else:
        update.message.reply_text('Неправильно, повторно введите логин')
def send_password(update, context):
    password = update.message.text
    obj = Bot_users.objects.get(user_id=update.message.chat.id)
    if obj.who == 'foreman':
        check = Foreman.objects.filter(login=obj.login, password=password)
    elif obj.who == 'client':
        check = Client.objects.filter(login=obj.login, password=password)
    if check:
        obj.password = password
        obj.save()
        #_____________ welcome menu___________________ 

        update.message.reply_text('Добро пожаловать в наш бот', reply_markup = ReplyKeyboardMarkup(keyboard=[['Дальше']], resize_keyboard=True))
        return ConversationHandler.END
    


    else:
        update.message.reply_text('Неправильно, введите пароль еще раз')
