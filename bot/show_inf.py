from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ConversationHandler
from bot.conversationList import *
from app.models import *


def show_inf_about(update, context):
    c = update.callback_query
    bot = context.bot
    data = str(c.data)
    if 'inf-material' in data:
        sth, obj_title = data.split('_')
        materials = Material.objects.filter(obj=obj_title)
        n=1
        msg = ''
        for m in materials:
            msg += str(n) + '. {}, {}{}, {}{};\n'.format(m.title, m.amount, m.measurement, m.price, m.summ_or_dollar)
            n += 1
        i_back = InlineKeyboardButton(text='Назад', callback_data='back-show-inf_{}'.format(obj_title))
        c.edit_message_text(msg, reply_markup = InlineKeyboardMarkup([[i_back]]))

    elif 'inf-salary' in data:
        sth, obj_title = data.split('_')
        salaries = Salary.objects.filter(obj=obj_title)
        n=1
        msg = ''
        for s in salaries:
            msg += str(n) + '. {}, {}{};\n'.format(s.title,s.price, s.summ_or_dollar)
            n += 1
        i_back = InlineKeyboardButton(text='Назад', callback_data='back-show-inf_{}'.format(obj_title))
        c.edit_message_text(msg, reply_markup = InlineKeyboardMarkup([[i_back]]))
    elif 'back-show-inf' in data:
        sth, text = data.split('_')
        obj = Object.objects.get(title=text)
        i_material = InlineKeyboardButton(text='Материалы', callback_data='inf-material_{}'.format(text))
        i_salary = InlineKeyboardButton(text='Иш хакки', callback_data='inf-salary_{}'.format(text))
        i_back = InlineKeyboardButton(text='Назад', callback_data='back-to-objects_clients')
        c.edit_message_text('Остаток денег:{}\nПоказать информацию о ...'.format(obj.price), reply_markup=InlineKeyboardMarkup([[i_material], [i_salary], [i_back]]))
        return SHOW_INF_ABOUT
    
    elif 'back-to-objects' in data:
        sth, who = data.split('_')
        user = Bot_users.objects.get(user_id=c.message.chat.id)
        if who == 'foreman':
            obj = Foreman.objects.get(login=user.login).obj
        else:
            obj = Client.objects.get(login=user.login).obj
        objects_list = [[i.title] for i in obj.all()]
        bot.delete_message(c.message.chat.id, c.message.message_id)
        bot.send_message(c.message.chat.id, 'Все объекты', reply_markup=ReplyKeyboardMarkup(keyboard=objects_list, resize_keyboard=True))
        return ConversationHandler.END
