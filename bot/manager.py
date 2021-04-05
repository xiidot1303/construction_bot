from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ConversationHandler
from bot.conversationList import *
from app.models import *

def enter_manager(update, context):
    update.message.reply_text('Вы можете создать объекты и пополнить счёт прораба', reply_markup=ReplyKeyboardMarkup(keyboard=[['Создать объект', 'Пополнить счёт']], resize_keyboard=True))
    return MAIN_MENU_MANAGER

def main_menu_manager(update, context):
    bot = context.bot
    message = update.message.text
    if message == 'Создать объект':
        update.message.reply_text('Отправьте название объекта', reply_markup=ReplyKeyboardMarkup(keyboard=[['Назад']], resize_keyboard=True))
        return SEND_OBJECT_TITLE
    elif message == 'Пополнить счёт':
        foremans = [[InlineKeyboardButton(text=i.name, callback_data=i.name)] for i in Foreman.objects.all()]
        del_msg = update.message.reply_text('Укажите имя прораба, который хотите пополнить счёта', reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
        bot.delete_message(update.message.chat.id, del_msg.message_id)
        bot.send_message(update.message.chat.id, 'Укажите имя прораба, который хотите пополнить счёта', reply_markup=InlineKeyboardMarkup(foremans))
        return REPLENISH



def send_object_title(update, context):
    title = update.message.text
    if title == 'Назад':
        enter_manager(update, context)
        return MAIN_MENU_MANAGER
    Object.objects.create(title=title, price=str(update.message.chat.id), price_summ='*', price_dollar='*')
    update.message.reply_text('Отправьте остаток денег (долларов)', reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
    return SEND_OBJECT_PRICE_DOLLAR

def send_object_price_dollar(update, context):
    price = update.message.text
    obj = Object.objects.get(price=str(update.message.chat.id), price_summ='*')
    obj.price_dollar = price
    obj.save()
    update.message.reply_text('Отправьте остаток денег (сумм)')
    return SEND_OBJECT_PRICE_SUMM

def send_object_price_summ(update, context):
    bot = context.bot
    price = update.message.text
    obj = Object.objects.get(price=str(update.message.chat.id), price_summ='*')
    obj.price_summ = price
    obj.save()
    bot.send_message(update.message.chat.id, 'Успешно создан объект')
    bot.send_message(update.message.chat.id, 'Вы можете создать объекты и пополнить счёт прораба', reply_markup=ReplyKeyboardMarkup(keyboard=[['Создать объект', 'Пополнить счёт']], resize_keyboard=True))
    return MAIN_MENU_MANAGER


def replenish(update, contex):
    update = update.callback_query
    text = update.data
    transfer_money.objects.create(user_id=update.message.chat.id, foreman=text, transfered = 'False')
    objects = [[InlineKeyboardButton(text=i.title, callback_data=i.title)] for i in Foreman.objects.get(name=text).obj.all()]
    update.edit_message_text('Укажите объект', reply_markup=InlineKeyboardMarkup(objects))
    return SEND_TRANS_OBJ

def send_trans_obj(update, context):
    update = update.callback_query
    text = update.data
    obj = transfer_money.objects.get(user_id=update.message.chat.id, transfered='False')
    obj.object = text
    obj.save()
    update.edit_message_text('Сумм или доллар', reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text='Сумм', callback_data='Сумм'), InlineKeyboardButton(text='Доллар', callback_data='Доллар')]]))
    return SEND_TRANS_SUMM_OR_DOLLAR


def send_trans_summ_or_dollar(update, context):
    bot = context.bot
    update = update.callback_query
    text = update.data    
    obj = transfer_money.objects.get(user_id=update.message.chat.id, transfered='False')
    obj.summ_or_dollar = text
    obj.save()

    update.edit_message_text('Введите цену')
    return SEND_TRANS_PRICE


def send_trans_price(update, context):
    bot = context.bot
    text = update.message.text
    trans_obj = transfer_money.objects.get(user_id=update.message.chat.id, transfered='False')
    trans_obj.price = text
    trans_obj.transfered = 'True'
    trans_obj.save()
    foreman = Foreman.objects.get(name=trans_obj.foreman)
    obj = Object.objects.get(title=trans_obj.object)
    if trans_obj.summ_or_dollar == 'Сумм':
        foreman.account_summ = int(foreman.account_summ) + int(text)
        foreman.save()
        obj.price_summ = int(obj.price_summ) - int(text)
        obj.save()
    else:
        foreman.account_dollar = int(foreman.account_dollar) + int(text)
        foreman.save()
        obj.price_dollar = int(obj.price_dollar) - int(text)    
        objs.save()
    bot.send_message(update.message.chat.id, 'Успешно перенесено')
    enter_manager(update, context)
    return MAIN_MENU_MANAGER