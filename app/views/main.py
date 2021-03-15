from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from telegram import Update
from bot.update import dp, updater
from django.http import HttpResponse
from dotenv import load_dotenv
import os
from app.models import *
import json
basedir = os.path.abspath(os.path.dirname(''))
load_dotenv(os.path.join(basedir, '.env'))
WHERE = os.environ.get('WHERE')



#start bot
@csrf_exempt
def bot_webhook(request):
    #try:
    #   

    if WHERE == 'LOCAL':
        updater.start_polling()
    else:
        update = Update.de_json(json.loads(request.body.decode('utf-8')), dp.bot)
        dp.process_update(update)
    return HttpResponse('Bot started!')



def folder_foremans(request):
    foremans = Foreman.objects.all()
    objects = []
    for f in foremans:
        objects.append(f.obj.all)
    context = {'foremans': foremans, 'objects': objects}
    return render(request, 'views/folder_foremans.html', context)

def folder_clients(request):
    clients = Client.objects.all()
    objects = []
    for c in clients:
        objects.append(c.obj.all)
    context = {'clients': clients, 'objects': objects}
    return render(request, 'views/folder_clients.html', context)


def material(request, obj):
    materials = Material.objects.filter(obj=obj)
    context = {'materials': materials}
    return render(request, 'views/material.html', context)

def salary(request, obj):
    salaries = Salary.objects.filter(obj=obj)
    context = {'salaries': salaries}
    return render(request, 'views/salary.html', context)

def all_foremans(request):
    foremans = Foreman.objects.all()
    context = {'foremans': foremans}
    return render(request, 'views/all_foremans.html', context)











def main_menu(request):
    return render(request, 'app/main.html', {})

