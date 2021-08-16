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
from bot.functions import *
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
            get = bot.sendMessage(chat_id=bot_user.user_id, text=get_word('type cancel', update), reply_markup=ReplyKeyboardMarkup(keyboard=[['/cancel']], resize_keyboard=True))

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
            get = bot.sendMessage(chat_id=bot_user.user_id, text=get_word('type cancel', update), reply_markup=ReplyKeyboardMarkup(keyboard=[['/cancel']], resize_keyboard=True))

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
    obj_name = m.obj
    obj = Object.objects.get(title=obj_name)
    if m.summ_or_dollar == 'суммы':
        try:
            obj.price_material_summ = str(float(obj.price_material_summ) + (float(m.price) * float(m.amount)))
            obj.price_material_dollar = str(float(obj.price_material_dollar) + summ_to_dollar(float(m.price) * float(m.amount)))
        except:
            q = 0
        if m.user_id != None:
            try:
                foreman = Foreman.objects.get(login=Bot_users.objects.get(user_id=m.user_id).login)
                foreman.account_summ = float(foreman.account_summ) + (float(m.price) * float(m.amount))
                foreman.account_dollar = float(foreman.account_dollar) + summ_to_dollar(float(m.price) * float(m.amount))
                foreman.save()
            except:
                q=0
    else:
        try:
            obj.price_material_dollar = str(float(obj.price_material_dollar) + (float(m.price) * float(m.amount)))
            obj.price_material_summ = str(float(obj.price_material_summ) + dollar_to_summ(float(m.price) * float(m.amount)))
        except:
            q=0
        if m.user_id != None:
            try:
                foreman = Foreman.objects.get(login=Bot_users.objects.get(user_id=m.user_id).login)
                foreman.account_dollar = float(foreman.account_dollar) + (float(m.price) * float(m.amount))
                foreman.account_summ = float(foreman.account_summ) + dollar_to_summ(float(m.price) * float(m.amount))
                foreman.save()
            except:
                q=0
    obj.save()
    m.delete()
    return redirect(material, obj=obj_name)


def delete_salary(request, pk):
    s = Salary.objects.get(pk=pk)
    obj_name = s.obj
    obj = Object.objects.get(title=obj_name)
    if s.summ_or_dollar == 'суммы':
        try:
            obj.price_salary_summ = str(float(obj.price_salary_summ) + float(s.price))
            obj.price_salary_dollar = str(float(obj.price_salary_dollar) + summ_to_dollar(s.price))
        except:
            q=0
        if s.user_id != None:
            try:
                foreman = Foreman.objects.get(login=Bot_users.objects.get(user_id=s.user_id).login)
                foreman.account_summ = float(foreman.account_summ) + (float(s.price))
                foreman.account_dollar = float(foreman.account_dollar) + summ_to_dollar(float(s.price))
                foreman.save()
            except:
                q=0
    else:
        try:
            obj.price_salary_dollar = str(float(obj.price_salary_dollar) + float(s.price))
            obj.price_salary_summ = str(float(obj.price_salary_summ) + dollar_to_summ(s.price))
        except:
            q=0
        if s.user_id != None:
            try:
                foreman = Foreman.objects.get(login=Bot_users.objects.get(user_id=s.user_id).login)
                foreman.account_dollar = float(foreman.account_dollar) + (float(s.price))
                foreman.account_summ = float(foreman.account_summ) + dollar_to_summ(float(s.price))
                foreman.save()
            except:
                q=0

    obj.save()
    s.delete()
    return redirect(salary, obj=obj_name)


def delete_material_title(request, pk):
    obj = Material_title.objects.get(pk=pk)
    obj.delete()
    return redirect(material_title)


def delete_salary_title(request, pk):
    obj = Salary_title.objects.get(pk=pk)
    obj.delete()
    return redirect(salary_title)
