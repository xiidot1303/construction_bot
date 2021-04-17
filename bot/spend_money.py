from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ConversationHandler
from bot.conversationList import *
from app.models import *

def spend_money_for(update, context):
    c = update.callback_query
    bot = context.bot
    data = str(c.data)
    if 'spend-money-to-material' in data:
        s, object_title = str(data).split('_')
        
        titles = [[i.title] for i in Material_title.objects.all()]
        bot.delete_message(c.message.chat.id, c.message.message_id)

        bot.send_message(c.message.chat.id, 'Выберите название')

        Material.objects.create(obj=object_title, user_id=c.message.chat.id)
        return SEND_TITLE_MATERIAL
    elif 'spend-money-for-salary' in data:
        s, object_title = str(data).split('_')
        
        titles = [[i.title] for i in Salary_title.objects.all()]
        bot.delete_message(c.message.chat.id, c.message.message_id)

        bot.send_message(c.message.chat.id, 'Выберите название')

        Salary.objects.create(obj=object_title, user_id=c.message.chat.id)
        return SEND_TITLE_SALARY
    

    elif 'back-to-objects' in data:
        sth, who = data.split('_')
        user = Bot_users.objects.get(user_id=c.message.chat.id)
        if who == 'foreman':
            obj = Foreman.objects.get(login=user.login).obj
        else:
            obj = Client.objects.get(login=user.login).obj
        objects_list = [[i.title] for i in obj.all()]
        objects_list.append(['Главное меню'])
        bot.delete_message(c.message.chat.id, c.message.message_id)
        bot.send_message(c.message.chat.id, 'Все объекты', reply_markup=ReplyKeyboardMarkup(keyboard=objects_list, resize_keyboard=True))
        return ConversationHandler.END

def send_title_salary(update, context):
    obj = Salary.objects.get(user_id=update.message.chat.id, title=None)
    obj.title = update.message.text
    obj.save()
    update.message.reply_text('Выберите суммы или доллары', reply_markup=ReplyKeyboardMarkup(keyboard=[['суммы', 'доллары']], resize_keyboard=True))
    return SEND_SUMM_OR_DOLLAR_SALARY

def send_summ_or_dollar_salar(update, context):
    obj = Salary.objects.get(user_id=update.message.chat.id, summ_or_dollar=None)
    obj.summ_or_dollar = update.message.text
    obj.save()
    update.message.reply_text('Введите цену за работу', reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
    return SEND_PRICE_SALARY

def send_price_salary(update, context):
    if update.message.text != '/reload':
        bot = context.bot
        text = update.message.text
        obj = Salary.objects.get(user_id=update.message.chat.id, price=None)
        obj.price = update.message.text
        obj.save()
        Obj = Object.objects.get(title=obj.obj)
        foreman = Foreman.objects.get(obj__title=obj.obj)
        if obj.summ_or_dollar == 'суммы':
            foreman.account_summ = str(int(foreman.account_summ) - (int(update.message.text)))
            if int(foreman.account_summ) < 0:
                bot.send_message(update.message.chat.id, 'Недостаточно средств')
                obj.delete()
            else:
                foreman.save()
        else:
            foreman.account_dollar = str(int(foreman.account_dollar) - (int(update.message.text)))        
            if int(foreman.account_dollar) < 0:
                bot.send_message(update.message.chat.id, 'Недостаточно средств')
                obj.delete()
            else:
                foreman.save()


        # return to object menu, where can spend money for materials or salary
        foreman = Foreman.objects.get(obj__title=Obj.title)
        text = Obj.title
        obj = Object.objects.get(title=Obj.title)
        i_material = InlineKeyboardButton(text='Материалы', callback_data='spend-money-to-material_{}'.format(text))
        i_salary = InlineKeyboardButton(text='Иш хакки', callback_data='spend-money-for-salary_{}'.format(text))
        i_back = InlineKeyboardButton(text='Назад', callback_data='back-to-objects_foreman')
        d = bot.send_message(update.message.chat.id, 'Тратить деньги на...', reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
        bot.delete_message(update.message.chat.id, d.message_id)
        bot.send_message(update.message.chat.id, 'Остаток денег:{} сумм, {} доллар\nТратить деньги на...'.format(Obj.price_summ, Obj.price_dollar), reply_markup=InlineKeyboardMarkup([[i_material], [i_salary], [i_back]]))


        return SPEND_MONEY_FOR
        


def send_title_material(update, context):
    text = update.message.text
    obj = Material.objects.get(user_id=update.message.chat.id, title=None)
    obj.title = text
    obj.save()
    update.message.reply_text('Выберите единицу измерения', reply_markup=ReplyKeyboardMarkup(keyboard=[['м', 'кг', 'м^3', 'м^2']], resize_keyboard=True))
    return SELECT_MEASUREMENT

def select_measurement(update, context):
    obj = Material.objects.get(user_id=update.message.chat.id, measurement=None)
    obj.measurement = update.message.text
    obj.save()
    update.message.reply_text('Введите количество', reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
    return SEND_AMOUNT


def send_amount(update, context):
    if update.message.text != '/reload':
        obj = Material.objects.get(user_id=update.message.chat.id, amount=None)
        obj.amount = update.message.text
        obj.save()
        update.message.reply_text('Выберите суммы или доллары', reply_markup=ReplyKeyboardMarkup(keyboard=[['суммы', 'доллары']], resize_keyboard=True))
        return SEND_SUMM_OR_DOLLAR_MATERIAL

def send_summ_or_dollar_material(update, context):
    obj = Material.objects.get(user_id=update.message.chat.id, summ_or_dollar=None)
    obj.summ_or_dollar = update.message.text
    obj.save()
    update.message.reply_text('Введите цену за 1шт(м, кг и т.д)', reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
    return SEND_PRICE_MATERIAL

def send_price_material(update, context):
    if update.message.text != '/reload':   
        bot = context.bot
        material_obj = Material.objects.get(user_id=update.message.chat.id, price=None)
        material_obj.price = update.message.text
        material_obj.save()
        Obj = Object.objects.get(title=material_obj.obj)
        foreman = Foreman.objects.get(obj__title=material_obj.obj)
        if material_obj.summ_or_dollar == 'суммы':
            foreman.account_summ = str(int(foreman.account_summ) - (int(material_obj.amount) * int(material_obj.price)))
            if int(foreman.account_summ) < 0:
                bot.send_message(update.message.chat.id, 'Недостаточно средств')
                material_obj.delete()
            else:
                foreman.save()
        else:
            foreman.account_dollar = str(int(foreman.account_dollar) - (int(material_obj.amount) * int(material_obj.price)))
            if int(foreman.account_dollar) < 0:
                bot.send_message(update.message.chat.id, 'Недостаточно средств')
                material_obj.delete()
            else:
                foreman.save()
        # return to object menu, where can spend money for materials or salary
        foreman = Foreman.objects.get(obj__title=Obj.title)
        text = Obj.title
        i_material = InlineKeyboardButton(text='Материалы', callback_data='spend-money-to-material_{}'.format(text))
        i_salary = InlineKeyboardButton(text='Иш хакки', callback_data='spend-money-for-salary_{}'.format(text))
        i_back = InlineKeyboardButton(text='Назад', callback_data='back-to-objects_foreman')
        d = bot.send_message(update.message.chat.id, 'Тратить деньги на...', reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
        bot.delete_message(update.message.chat.id, d.message_id)
        bot.send_message(update.message.chat.id, 'Остаток денег:{} сумм, {} доллар\nТратить деньги на...'.format(Obj.price_summ, Obj.price_dollar), reply_markup=InlineKeyboardMarkup([[i_material], [i_salary], [i_back]]))
        return SPEND_MONEY_FOR