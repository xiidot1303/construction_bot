from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from telegram import Update
from bot.update import dp, updater
from django.http import HttpResponse, FileResponse
from dotenv import load_dotenv
import os
from app.models import *
import json
from django.contrib.auth.decorators import login_required
import pandas as pd
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


@login_required
def folder_foremans(request):
    foremans = Foreman.objects.all().order_by('name')
    objects = []
    for f in foremans:
        objects.append(f.obj.all)
    context = {'foremans': foremans, 'objects': objects}
    return render(request, 'views/folder_foremans.html', context)

@login_required
def folder_clients(request):
    clients = Client.objects.all().order_by('name')
    objects = []
    for c in clients:
        objects.append(c.obj.all)
    context = {'clients': clients, 'objects': objects}
    return render(request, 'views/folder_clients.html', context)

@login_required
def material(request, obj):
    del_materials = Material.objects.filter(title=None)
    for m in del_materials:
        m.delete()

    materials = Material.objects.filter(obj=obj)
    total_amount = [str(int(i.amount)*int(i.price)) for i in materials]
    foreman = Foreman.objects.get(obj__title=obj).name

    # ________create excel file
    df = {'Название': [], 'Измерение': [], 'Количество': [], 'Суммы или доллары': [], 'Цена': [], 'Общая сумма': [], 'Прораб': [], 'Дата': []}
    
    #add title
    df['Название'] = [i.title for i in materials]
    df['Измерение'] = [i.measurement for i in materials]
    df['Количество'] = [i.amount for i in materials]
    df['Суммы или доллары'] = [i.summ_or_dollar for i in materials]
    df['Цена'] = [i.price for i in materials]
    df['Общая сумма'] = [i for i in total_amount]
    df['Прораб'] = [foreman for i in materials]
    df['Дата'] = [i.published.strftime('%d.%m.%Y') for i in materials]
    df = pd.DataFrame(df)
    df.to_excel('files/excel/material_{}.xlsx'.format(obj))
    #_________
    context = {'materials': materials, 'total_amount': total_amount, 'file_path': 'material_{}'.format(obj), 'foreman': foreman, 'type': 'Все', 'obj': obj}
    return render(request, 'views/material.html', context)


@login_required
def sort_material(request, obj, type):
    del_materials = Material.objects.filter(title=None)
    for m in del_materials:
        m.delete()

    materials = Material.objects.filter(obj=obj, type=type)
    total_amount = [str(int(i.amount)*int(i.price)) for i in materials]
    foreman = Foreman.objects.get(obj__title=obj).name

    # ________create excel file
    df = {'Название': [], 'Измерение': [], 'Количество': [], 'Суммы или доллары': [], 'Цена': [], 'Общая сумма': [], 'Прораб': [], 'Дата': []}
    
    #add title
    df['Название'] = [i.title for i in materials]
    df['Измерение'] = [i.measurement for i in materials]
    df['Количество'] = [i.amount for i in materials]
    df['Суммы или доллары'] = [i.summ_or_dollar for i in materials]
    df['Цена'] = [i.price for i in materials]
    df['Общая сумма'] = [i for i in total_amount]
    df['Прораб'] = [foreman for i in materials]
    df['Дата'] = [i.published.strftime('%d.%m.%Y') for i in materials]
    df = pd.DataFrame(df)
    df.to_excel('files/excel/material_{}.xlsx'.format(obj))
    #_________
    type_for_filter = 'Все'
    if type == 'flat':
        type_for_filter = 'Квартиры'
    elif type == 'plot':
        type_for_filter = 'Участки'

    context = {'materials': materials, 'total_amount': total_amount, 'file_path': 'material_{}'.format(obj), 'foreman': foreman, 'type': type_for_filter, 'obj': obj}
    return render(request, 'views/material.html', context)



@login_required
def salary(request, obj):
    del_salaries = Salary.objects.filter(title=None)
    for m in del_salaries:
        m.delete()
     
    salaries = Salary.objects.filter(obj=obj)
    df = {'Название': [], 'Суммы или доллары': [], 'Цена': [], 'Прораб': [], 'Дата': []}
    foreman = Foreman.objects.get(obj__title=obj).name
    #add title
    df['Название'] = [i.title for i in salaries]
    df['Суммы или доллары'] = [i.summ_or_dollar for i in salaries]
    df['Цена'] = [i.price for i in salaries]
    df['Прораб'] = [foreman for i in salaries]
    df['Дата'] = [i.published.strftime('%d.%m.%Y') for i in salaries]
    df = pd.DataFrame(df)
    df.to_excel('files/excel/salary_{}.xlsx'.format(obj))
    allsalaries = Salary.objects.all()
    overall_price_summ = sum([int(i.price) for i in salaries.filter(summ_or_dollar='суммы')])
    overall_price_dollar = sum([int(i.price) for i in salaries.filter(summ_or_dollar='доллары')])
    context = {'salaries': salaries, 'file_path': 'salary_{}'.format(obj), 'foreman': foreman, 'type': 'Все', 'type_for_filter': 'Все'
    ,'obj': obj, 'title': 'Все', 'allsalaries': allsalaries, 'overall_price_summ': overall_price_summ, 'overall_price_dollar': overall_price_dollar}
    return render(request, 'views/salary.html', context)



@login_required
def sort_salary(request, obj, title, type):
    del_salaries = Salary.objects.filter(title=None)
    for m in del_salaries:
        m.delete()
    if type == 'Все':
        if title == 'Все':
            salaries = Salary.objects.filter(obj=obj)
        else:
            salaries = Salary.objects.filter(obj=obj, title=title)
    else:
        if title == 'Все':
            salaries = Salary.objects.filter(obj=obj, type=type)
        else:
            salaries = Salary.objects.filter(obj=obj, type=type, title=title)
    df = {'Название': [], 'Суммы или доллары': [], 'Цена': [], 'Прораб': [], 'Дата': []}
    foreman = Foreman.objects.get(obj__title=obj).name
    #add title
    df['Название'] = [i.title for i in salaries]
    df['Суммы или доллары'] = [i.summ_or_dollar for i in salaries]
    df['Цена'] = [i.price for i in salaries]
    df['Прораб'] = [foreman for i in salaries]
    df['Дата'] = [i.published.strftime('%d.%m.%Y') for i in salaries]
    df = pd.DataFrame(df)
    df.to_excel('files/excel/salary_{}.xlsx'.format(obj))
    type_for_filter = 'Все'
    if type == 'flat':
        type_for_filter = 'Квартиры'
    elif type == 'plot':
        type_for_filter = 'Участки'
    l = []
    allsalaries = []
    for i in Salary.objects.all():
        if not i.title in l:
            allsalaries.append(i)
            l.append(i.title)
    import math
    overall_price_summ = sum([int(i.price) for i in salaries.filter(summ_or_dollar='суммы')])
    overall_price_dollar = sum([int(i.price) for i in salaries.filter(summ_or_dollar='доллары')])
    context = {'salaries': salaries, 'file_path': 'salary_{}'.format(obj), 'foreman': foreman, 'type_for_filter': type_for_filter, 'type': type, 
    'obj': obj, 'title': title, 'allsalaries': allsalaries, 'overall_price_summ': overall_price_summ, 'overall_price_dollar': overall_price_dollar}
    return render(request, 'views/salary.html', context)



@login_required
def all_foremans(request):
    foremans = Foreman.objects.all()
    context = {'foremans': foremans}
    return render(request, 'views/all_foremans.html', context)


@login_required
def objects(request):
    all_objects = Object.objects.all()
    context = {'objects': all_objects}
    return render(request, 'views/objects.html', context)



@login_required
def get_excel(request, file_path):
    f = open('files/excel/{}.xlsx'.format(file_path), 'rb')
    return FileResponse(f)



@login_required
def main_menu(request):
    return render(request, 'app/main.html', {})



@login_required
def material_title(request):
    titles = Material_title.objects.all()
    one_to_three = list(range(3))
    context = {'titles': titles, 'count': one_to_three}
    return render(request, 'views/material_titles.html', context)


@login_required
def salary_title(request):
    titles = Salary_title.objects.all()
    one_to_three = list(range(3))
    context = {'titles': titles, 'count': one_to_three}
    return render(request, 'views/salary_titles.html', context)