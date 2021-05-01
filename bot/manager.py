from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ConversationHandler
from bot.conversationList import *
from bot.functions import *
from app.models import *
from dotenv import load_dotenv
import os

basedir = os.path.abspath(os.path.dirname(''))
load_dotenv(os.path.join(basedir, '.env'))
MANAGER = os.environ.get('MANAGER')
def enter_manager(update, context):
    managers = list(map(float, MANAGER.split()))
    if update.message.chat.id in managers:
        update.message.reply_text('Вы можете создать объекты и пополнить счёт прораба', reply_markup=ReplyKeyboardMarkup(keyboard=[['Создать объект', 'Пополнить счёт'], ['Создать материал', 'Создать иш хакки']], resize_keyboard=True))
        return MAIN_MENU_MANAGER
    else:
        update.message.reply_text('У вас нет разрешения на доступ к этому меню')
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
    elif message == 'Создать материал':
        titles = [[i.title] for i in Object.objects.all()]
        titles.append(['Назад'])
        update.message.reply_text('Введите имя объекта, из которого вы хотите создать материал:', reply_markup = ReplyKeyboardMarkup(keyboard=titles, resize_keyboard=True))
        return CREATE_MATERIAL_send_object_title
    elif message == 'Создать иш хакки':
        titles = [[i.title] for i in Object.objects.all()]
        titles.append(['Назад'])
        update.message.reply_text('Введите имя объекта, из которого вы хотите создать материал:', reply_markup = ReplyKeyboardMarkup(keyboard=titles, resize_keyboard=True))
        return CREATE_SALARY_send_object_title


def send_object_title(update, context):
    title = update.message.text
    if title == 'Назад':
        enter_manager(update, context)
        return MAIN_MENU_MANAGER
    Object.objects.create(title=title, price=str(update.message.chat.id), price_summ='*', price_dollar='*')
    update.message.reply_text('Отправьте остаток денег (долларов), на материалы и иш хакки с пробелям\n{материал} {иш хакки}\nНапример:\n\n1000 2000', reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
    return SEND_OBJECT_PRICE_DOLLAR

def send_object_price_dollar(update, context):
    try:
        price_material, price_salary = str(update.message.text).split()
    except:
        update.message.reply_text('Ошибка!\n\nОтправьте остаток денег (долларов), на материалы и иш хакки с пробелям\n{материал} {иш хакки}\nНапример:\n\n1000 2000')
        return SEND_OBJECT_PRICE_DOLLAR
    obj = Object.objects.get(price=str(update.message.chat.id), price_summ='*')
    obj.price_material_dollar = price_material
    obj.price_salary_dollar = price_salary
    obj.save()
    update.message.reply_text('Отправьте остаток денег (сумм), на материалы и иш хакки с пробелям\n{материал} {иш хакки}\nНапример:\n\n1000 2000')
    return SEND_OBJECT_PRICE_SUMM

def send_object_price_summ(update, context):
    bot = context.bot
    try:
        price_material, price_salary = str(update.message.text).split()
    except:
        update.message.reply_text('Ошибка!\n\nОтправьте остаток денег (сумм), на материалы и иш хакки с пробелям\n{материал} {иш хакки}\nНапример:\n\n1000 2000')
        return SEND_OBJECT_PRICE_SUMM
    obj = Object.objects.get(price=str(update.message.chat.id), price_summ='*')
    obj.price_material_summ = price_material
    obj.price_salary_summ = price_salary
    obj.save()
    bot.send_message(update.message.chat.id, 'Успешно создан объект')
    bot.send_message(update.message.chat.id, 'Вы можете создать объекты и пополнить счёт прораба', reply_markup=ReplyKeyboardMarkup(keyboard=[['Создать объект', 'Пополнить счёт'], ['Создать материал', 'Создать иш хакки']], resize_keyboard=True))
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
        foreman.account_summ = float(foreman.account_summ) + float(text)
        foreman.save()
        #obj.price_summ = float(obj.price_summ) - float(text)
        #obj.save()
    else:
        foreman.account_dollar = float(foreman.account_dollar) + float(text)
        foreman.save()
        #obj.price_dollar = float(obj.price_dollar) - float(text)    
        #obj.save()
    bot.send_message(update.message.chat.id, 'Успешно перенесено')
    enter_manager(update, context)
    return MAIN_MENU_MANAGER
    



# create Material
def create_material_send_object_title(update, context):
    text = update.message.text
    if text == 'Назад':
        update.message.reply_text('Вы можете создать объекты и пополнить счёт прораба', reply_markup=ReplyKeyboardMarkup(keyboard=[['Создать объект', 'Пополнить счёт'], ['Создать материал', 'Создать иш хакки']], resize_keyboard=True))
        return MAIN_MENU_MANAGER
    is_available = Object.objects.filter(title=text)
    if not is_available:
        update.message.reply_text('Объект недоступен, повторно введите названия объекта')
        return CREATE_MATERIAL_send_object_title
    Material.objects.create(obj=text, user_id=update.message.chat.id)
    
    update.message.reply_text('Выберите тип договора', reply_markup=ReplyKeyboardMarkup(keyboard=[['Квартира', 'Участка']], resize_keyboard=True))
    return CREATE_MATERIAL_SEND_TYPE
    
    
def create_material_send_type(update, context):
    text = update.message.text
    obj = Material.objects.get(user_id=update.message.chat.id, type=None)

    if text == 'Квартира': 
        obj.type = 'flat'
        obj.save()
    elif text == 'Участка':
        obj.type = 'plot'
        obj.save()
    else:
        update.message.reply_text('Выберите тип договора')
        return CREATE_MATERIAL_SEND_TYPE
    update.message.reply_text('Выберите название', reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
    return CREATE_MATERIAL_send_material_title

def create_material_send_material_title(update, context):
    text = update.message.text
    obj = Material.objects.get(user_id=update.message.chat.id, title=None)
    obj.title = text
    obj.save()
    update.message.reply_text('Выберите единицу измерения', reply_markup=ReplyKeyboardMarkup(keyboard=[['м', 'кг', 'м^3', 'м^2']], resize_keyboard=True))
    return CREATE_MATERIAL_SELECT_MEASUREMENT

def create_material_select_measurement(update, context):
    obj = Material.objects.get(user_id=update.message.chat.id, measurement=None)
    obj.measurement = update.message.text
    obj.save()
    update.message.reply_text('Введите количество', reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
    return CREATE_MATERIAL_SEND_AMOUNT


def create_material_send_amount(update, context):
    if update.message.text != '/manager':
        if not is_float(update.message.text):
            update.message.reply_text('Неверное значение\nВведите количество')
            return CREATE_MATERIAL_SEND_AMOUNT
        obj = Material.objects.get(user_id=update.message.chat.id, amount=None)
        obj.amount = update.message.text
        obj.save()
        update.message.reply_text('Выберите суммы или доллары', reply_markup=ReplyKeyboardMarkup(keyboard=[['суммы', 'доллары']], resize_keyboard=True))
        return CREATE_MATERIAL_SEND_SUMM_OR_DOLLAR_MATERIAL

def create_material_send_summ_or_dollar_material(update, context):
    obj = Material.objects.get(user_id=update.message.chat.id, summ_or_dollar=None)
    obj.summ_or_dollar = update.message.text
    obj.save()
    update.message.reply_text('Введите цену за 1шт(м, кг и т.д)', reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
    return CREATE_MATERIAL_SEND_PRICE_MATERIAL

def create_material_send_price_material(update, context):
    if update.message.text != '/manager':   
        if not is_float(update.message.text):
            update.message.reply_text('Неверное значение\nВведите цену')
            return CREATE_MATERIAL_SEND_PRICE_MATERIAL
        bot = context.bot
        material_obj = Material.objects.get(user_id=update.message.chat.id, price=None)
        material_obj.price = update.message.text
        material_obj.save()
        Obj = Object.objects.get(title=material_obj.obj)
       
        if material_obj.summ_or_dollar == 'суммы':
            Obj.price_material_summ = str(float(Obj.price_material_summ) - (float(material_obj.amount) * float(material_obj.price)))
            
            Obj.save()
            bot.send_message(update.message.chat.id, 'Успешно создан новый материал')
        else:
            Obj.price_material_dollar = str(float(Obj.price_material_dollar) - (float(material_obj.amount) * float(material_obj.price)))
        
            Obj.save()
            bot.send_message(update.message.chat.id, 'Успешно создан новый материал')
        
        bot.send_message(update.message.chat.id, 'Вы можете создать объекты и пополнить счёт прораба', reply_markup=ReplyKeyboardMarkup(keyboard=[['Создать объект', 'Пополнить счёт'], ['Создать материал', 'Создать иш хакки']], resize_keyboard=True))
        return MAIN_MENU_MANAGER


# create salary
def create_salary_send_object_title(update, context):
    text = update.message.text
    if text == 'Назад':
        update.message.reply_text('Вы можете создать объекты и пополнить счёт прораба', reply_markup=ReplyKeyboardMarkup(keyboard=[['Создать объект', 'Пополнить счёт'], ['Создать материал', 'Создать иш хакки']], resize_keyboard=True))
        return MAIN_MENU_MANAGER
    is_available = Object.objects.filter(title=text)
    if not is_available:
        update.message.reply_text('Объект недоступен, повторно введите названия объекта')
        return CREATE_SALARY_send_object_title
    Salary.objects.create(obj=text, user_id=update.message.chat.id)
    update.message.reply_text('Выберите тип договора', reply_markup=ReplyKeyboardMarkup(keyboard=[['Квартира', 'Участка']], resize_keyboard=True))
    return CREATE_SALARY_send_type

def create_salary_send_type(update, context):
    text = update.message.text
    obj = Salary.objects.get(user_id=update.message.chat.id, type=None)

    if text == 'Квартира': 
        obj.type = 'flat'
        obj.save()
    elif text == 'Участка':
        obj.type = 'plot'
        obj.save()
    else:
        update.message.reply_text('Выберите тип договора')
        return CREATE_SALARY_send_type
    titles = [[i.title] for i in Salary_title.objects.all()]
    update.message.reply_text('Выберите название', reply_markup=ReplyKeyboardMarkup(keyboard=titles, resize_keyboard=True))
    
    return CREATE_SALARY_send_salary_title



def create_salary_send_salary_title(update, context):
    obj = Salary.objects.get(user_id=update.message.chat.id, title=None)
    obj.title = update.message.text
    obj.save()
    update.message.reply_text('Выберите суммы или доллары', reply_markup=ReplyKeyboardMarkup(keyboard=[['суммы', 'доллары']], resize_keyboard=True))
    return CREATE_SALARY_SEND_SUMM_OR_DOLLAR_SALARY

def create_salary_send_summ_or_dollar_salary(update, context):
    obj = Salary.objects.get(user_id=update.message.chat.id, summ_or_dollar=None)
    obj.summ_or_dollar = update.message.text
    obj.save()
    update.message.reply_text('Введите цену за работу', reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
    return CREATE_SALARY_SEND_PRICE_SALARY

def create_salary_send_price_salary(update, context):
    if update.message.text != '/manager':
        if not is_float(update.message.text):
            update.message.reply_text('Неверное значение\nВведите цену')
            return CREATE_SALARY_SEND_PRICE_SALARY
        bot = context.bot
        text = update.message.text
        obj = Salary.objects.get(user_id=update.message.chat.id, price=None)
        obj.price = update.message.text
        obj.save()
        Obj = Object.objects.get(title=obj.obj)
  
        if obj.summ_or_dollar == 'суммы':
            Obj.price_salary_summ = str(float(Obj.price_salary_summ) - (float(update.message.text)))
            
            Obj.save()
            bot.send_message(update.message.chat.id, 'Успешно создан новый иш хакки')
        else:
            Obj.price_salary_dollar = str(float(Obj.price_salary_dollar) - (float(update.message.text)))        
     
            Obj.save()
            bot.send_message(update.message.chat.id, 'Успешно создан новый иш хакки')
        

        
        bot.send_message(update.message.chat.id, 'Вы можете создать объекты и пополнить счёт прораба', reply_markup=ReplyKeyboardMarkup(keyboard=[['Создать объект', 'Пополнить счёт'], ['Создать материал', 'Создать иш хакки']], resize_keyboard=True))
        return MAIN_MENU_MANAGER


