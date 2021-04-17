from django.shortcuts import render, redirect
from django.http import HttpResponse
import os
from app.models import *
from app.views.main import *
from django.contrib.auth.decorators import login_required
from dotenv import load_dotenv
import os
import telegram
from telegram import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
basedir = os.path.abspath(os.path.dirname(''))
load_dotenv(os.path.join(basedir, '.env'))
TOKEN = os.environ.get('TOKEN')

def delete_object(request, pk):
    obj = Object.objects.get(pk=pk)
    obj.delete()
    return redirect(objects)

def delete_foreman(request, pk):
    obj = Foreman.objects.get(pk=pk)
    try:
        bot_user = Bot_users.objects.get(login=obj.login, password=obj.password)

        # send message to user
        bot = telegram.Bot(token=TOKEN)
        try:
            get = bot.sendMessage(chat_id=bot_user.user_id, text='Ваш профиль удален\nНажмите /cancel', reply_markup=ReplyKeyboardMarkup(keyboard=[['/cancel']], resize_keyboard=True))

        except:
            dedfedf = 0
        # delete
        bot_user.delete()
    except:
        dedede = 0
    obj.delete()
    return redirect(folder_foremans)

def delete_client(request, pk):
    obj = Client.objects.get(pk=pk)
    try:
        bot_user = Bot_users.objects.get(login=obj.login, password=obj.password)
            # send message to user
        bot = telegram.Bot(token=TOKEN)
        try:
            get = bot.sendMessage(chat_id=bot_user.user_id, text='Ваш профиль удален\nНажмите /cancel', reply_markup=ReplyKeyboardMarkup(keyboard=[['/cancel']], resize_keyboard=True))

        except:
            dedfedf = 0
        # delete
        bot_user.delete()
    except:
        dedede = 0
    obj.delete()
    return redirect(folder_clients)

def delete_material(request, pk):
    m = Material.objects.get(pk=pk)
    obj = m.obj
    m.delete()
    return redirect(material, obj=obj)


def delete_salary(request, pk):
    s = Salary.objects.get(pk=pk)
    obj = s.obj
    s.delete()
    return redirect(salary, obj=obj)


def delete_material_title(request, pk):
    obj = Material_title.objects.get(pk=pk)
    obj.delete()
    return redirect(material_title)


def delete_salary_title(request, pk):
    obj = Salary_title.objects.get(pk=pk)
    obj.delete()
    return redirect(salary_title)
