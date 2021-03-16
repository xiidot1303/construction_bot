from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from bot.conversationList import *
from app.models import *
def start(update, context):
    user = Bot_users.objects.filter(user_id=update.message.chat.id)
    if user:
        #______________main manu __________________
        #user = Bot_users.objects.get(user_id=update.message.chat.id)
        #login = user.login
        #if user.who == 'foreman':
        #    obj = Foreman.objects.get(login=login).obj
        #else:
        #    obj = Client.objects.get(login=login).obj
        #objects_list = [[i.title] for i in obj.all()]
        #update.message.reply_text('Все объекты', reply_markup=ReplyKeyboardMarkup(keyboard=objects_list, resize_keyboard=True))
        neidbiew = 0
    else:
        update.message.reply_text('Авторизация как', reply_markup=ReplyKeyboardMarkup(keyboard=[['Прораб'], ['Клиент']], resize_keyboard=True))
        return LOGIN_AS


def objects(update, context):
    bot=context.bot
    text = update.message.text
    try:
        who = Bot_users.objects.get(user_id=update.message.chat.id).who
        if who == 'foreman':
            obj = Object.objects.get(title=text)
            i_material = InlineKeyboardButton(text='Материалы', callback_data='spend-money-to-material_{}'.format(text))
            i_salary = InlineKeyboardButton(text='Иш хакки', callback_data='spend-money-for-salary_{}'.format(text))
            i_back = InlineKeyboardButton(text='Назад', callback_data='back-to-objects_foreman')
            d = bot.send_message(update.message.chat.id, 'Тратить деньги на...', reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
            bot.delete_message(update.message.chat.id, d.message_id)
            bot.send_message(update.message.chat.id, 'Остаток денег:{}\nТратить деньги на...'.format(obj.price), reply_markup=InlineKeyboardMarkup([[i_material], [i_salary], [i_back]]))

            return SPEND_MONEY_FOR
        else:
            obj = Object.objects.get(title=text)
            i_material = InlineKeyboardButton(text='Материалы', callback_data='inf-material_{}'.format(text))
            i_salary = InlineKeyboardButton(text='Иш хакки', callback_data='inf-salary_{}'.format(text))
            i_back = InlineKeyboardButton(text='Назад', callback_data='back-to-objects_client')
            d = bot.send_message(update.message.chat.id, 'Показать информацию о ...', reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
            bot.delete_message(update.message.chat.id, d.message_id)
            bot.send_message(update.message.chat.id, 'Остаток денег:{}\nПоказать информацию о ...'.format(obj.price), reply_markup=InlineKeyboardMarkup([[i_material], [i_salary], [i_back]]))
            return SHOW_INF_ABOUT
    except:
        update.message.reply_text('Нет такого объекта')
