from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from telegram import Update
from bot.update import dp, updater
from functions.get_currency import currency
from django.http import HttpResponse, FileResponse
from dotenv import load_dotenv
import os
from app.models import *
from bs4 import BeautifulSoup
import requests
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
    total_amount = [str(float(i.amount)*float(i.price)) for i in materials]
    price_summ = sum([float(i.amount)*float(i.price) for i in materials.filter(summ_or_dollar='суммы')])
    price_dollar = sum([float(i.amount)*float(i.price) for i in materials.filter(summ_or_dollar='доллары')])
    summ_to_dollar = round(float(price_summ / currency()), 4)
    overall = price_dollar + summ_to_dollar
    # ________create excel file
    df = {'№': [], 'Название': [], 'Измерение': [], 'Количество': [], 'Цена': [], 'Всего (сум)': [], 'Всего ($)': [], 'Дата': []}
    
    #add title
    df['№'] = [i for i in range(1, len(materials)+1)]
    df['Название'] = [i.title for i in materials]
    df['Измерение'] = [i.measurement for i in materials]
    df['Количество'] = [i.amount for i in materials]
    df['Цена'] = [i.price for i in materials]
    n = 0
    for i in materials:
        if i.summ_or_dollar == 'суммы':
            df['Всего (сум)'].append(str(total_amount[n]))
            df['Всего ($)'].append(' ')
        else:
            df['Всего (сум)'].append(' ')
            df['Всего ($)'].append(str(total_amount[n]))

        n += 1

    
    df['Дата'] = [i.published.strftime('%d.%m.%Y') for i in materials]
    df['Цена'].append(' ')
    df['Цена'].append(str(currency()))
    df['Всего (сум)'].append(str(price_summ))
    df['Всего (сум)'].append(str(summ_to_dollar))
    df['Всего (сум)'].append('$'+str(overall))
    df['Всего ($)'].append(str(price_dollar))
    for a in df:
        while len(df[a]) != len(df['Всего (сум)']):
            df[a].append(' ')
    df = pd.DataFrame(df).set_index('№')


    df.to_excel('files/excel/material_{}.xlsx'.format(obj))
    #_________
    context = {'materials': materials, 'total_amount': total_amount, 'file_path': 'material_{}'.format(obj), 'type': 'Все', 'obj': obj,
    'price_summ': price_summ, 'price_dollar': price_dollar,
    'currency': currency, 'summ_to_dollar': summ_to_dollar, 'overall': overall}
    return render(request, 'views/material.html', context)


@login_required
def sort_material(request, obj, type):
    del_materials = Material.objects.filter(title=None)
    for m in del_materials:
        m.delete()

    materials = Material.objects.filter(obj=obj, type=type)
    total_amount = [str(float(i.amount)*float(i.price)) for i in materials]
    price_summ = sum([float(i.amount)*float(i.price) for i in materials.filter(summ_or_dollar='суммы')])
    price_dollar = sum([float(i.amount)*float(i.price) for i in materials.filter(summ_or_dollar='доллары')])
    summ_to_dollar = round(float(price_summ / currency()), 4)
    overall = price_dollar + summ_to_dollar

    # ________create excel file
    df = {'№': [], 'Название': [], 'Измерение': [], 'Количество': [], 'Цена': [], 'Всего (сум)': [], 'Всего ($)': [], 'Дата': []}
    
    #add title
    df['№'] = [i for i in range(1, len(materials)+1)]
    df['Название'] = [i.title for i in materials]
    df['Измерение'] = [i.measurement for i in materials]
    df['Количество'] = [i.amount for i in materials]
    df['Цена'] = [i.price for i in materials]
    n = 0
    for i in materials:
        if i.summ_or_dollar == 'суммы':
            df['Всего (сум)'].append(str(total_amount[n]))
            df['Всего ($)'].append(' ')
        else:
            df['Всего (сум)'].append(' ')
            df['Всего ($)'].append(str(total_amount[n]))

        n += 1

    
    df['Дата'] = [i.published.strftime('%d.%m.%Y') for i in materials]
    df['Цена'].append(' ')
    df['Цена'].append(str(currency()))
    df['Всего (сум)'].append(str(price_summ))
    df['Всего (сум)'].append(str(summ_to_dollar))
    df['Всего (сум)'].append('$'+str(overall))
    df['Всего ($)'].append(str(price_dollar))
    for a in df:
        while len(df[a]) != len(df['Всего (сум)']):
            df[a].append(' ')
    df = pd.DataFrame(df).set_index('№')
    df.to_excel('files/excel/material_{}.xlsx'.format(obj))
    #_________
    type_for_filter = 'Все'
    if type == 'flat':
        type_for_filter = 'Квартиры'
    elif type == 'plot':
        type_for_filter = 'Участки'

    context = {'materials': materials, 'total_amount': total_amount, 'file_path': 'material_{}'.format(obj), 'type': type_for_filter, 'obj': obj,
    'price_summ': price_summ, 'price_dollar': price_dollar,
    'currency': currency, 'summ_to_dollar': summ_to_dollar, 'overall': overall}
    return render(request, 'views/material.html', context)



@login_required
def salary(request, obj):
    del_salaries = Salary.objects.filter(title=None)
    for m in del_salaries:
        m.delete()
     
    salaries = Salary.objects.filter(obj=obj)
    
    price_summ = sum([float(i.price) for i in salaries.filter(summ_or_dollar='суммы')])
    price_dollar = sum([float(i.price) for i in salaries.filter(summ_or_dollar='доллары')])
    summ_to_dollar = round(float(price_summ / currency()), 4)
    overall = price_dollar + summ_to_dollar
    #___to excel
    df = {'№': [], 'Название': [], 'Цена (сум)': [], 'Цена ($)': [], 'Дата': []}
 
    #add title
    df['№'] = [i for i in range(1, len(salaries)+1)]
    df['Название'] = [i.title for i in salaries]
    for i in salaries:
        if i.summ_or_dollar == 'суммы':
            df['Цена (сум)'].append(str(i.price))
            df['Цена ($)'].append(' ')
        else:
            df['Цена (сум)'].append(' ')
            df['Цена ($)'].append(str(i.price))

    df['Дата'] = [i.published.strftime('%d.%m.%Y') for i in salaries]
    
    df['Название'].append(' ')
    df['Название'].append(str(currency()))
    df['Цена (сум)'].append(str(price_summ))
    df['Цена (сум)'].append(str(summ_to_dollar))
    df['Цена (сум)'].append('$'+str(overall))
    df['Цена ($)'].append(str(price_dollar))
    for a in df:
        while len(df[a]) != len(df['Цена (сум)']):
            df[a].append(' ')
    
    df = pd.DataFrame(df).set_index('№')

    df.to_excel('files/excel/salary_{}.xlsx'.format(obj))
    allsalaries = Salary.objects.all()

    context = {'salaries': salaries, 'file_path': 'salary_{}'.format(obj), 'type': 'Все', 'type_for_filter': 'Все'
    ,'obj': obj, 'title': 'Все', 'allsalaries': allsalaries,
    'price_summ': price_summ, 'price_dollar': price_dollar,
    'currency': currency, 'summ_to_dollar': summ_to_dollar, 'overall': overall}
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
    
    price_summ = sum([float(i.price) for i in salaries.filter(summ_or_dollar='суммы')])
    price_dollar = sum([float(i.price) for i in salaries.filter(summ_or_dollar='доллары')])
    summ_to_dollar = round(float(price_summ / currency()), 4)
    overall = price_dollar + summ_to_dollar
    #___to excel
    df = {'№': [], 'Название': [], 'Цена (сум)': [], 'Цена ($)': [], 'Дата': []}
 
    #add title
    df['№'] = [i for i in range(1, len(salaries)+1)]
    df['Название'] = [i.title for i in salaries]
    for i in salaries:
        if i.summ_or_dollar == 'суммы':
            df['Цена (сум)'].append(str(i.price))
            df['Цена ($)'].append(' ')
        else:
            df['Цена (сум)'].append(' ')
            df['Цена ($)'].append(str(i.price))

    df['Дата'] = [i.published.strftime('%d.%m.%Y') for i in salaries]
    
    df['Название'].append(' ')
    df['Название'].append(str(currency()))
    df['Цена (сум)'].append(str(price_summ))
    df['Цена (сум)'].append(str(summ_to_dollar))
    df['Цена (сум)'].append('$'+str(overall))
    df['Цена ($)'].append(str(price_dollar))
    for a in df:
        while len(df[a]) != len(df['Цена (сум)']):
            df[a].append(' ')
    
    df = pd.DataFrame(df).set_index('№')
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


    context = {'salaries': salaries, 'file_path': 'salary_{}'.format(obj), 'type_for_filter': type_for_filter, 'type': type, 
    'obj': obj, 'title': title, 'allsalaries': allsalaries,
    'price_summ': price_summ, 'price_dollar': price_dollar,
    'currency': currency, 'summ_to_dollar': summ_to_dollar, 'overall': overall}
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

@login_required
def all_materials(request, type):
    if type == 'Все':
        materials = Material.objects.all()
    else:
        materials = Material.objects.filter(type=type)
    total_amount = [str(float(i.amount)*float(i.price)) for i in materials]
    type_for_filter = 'Все'
    if type == 'flat':
        type_for_filter = 'Квартиры'
    elif type == 'plot':
        type_for_filter = 'Участки'
    price_summ = sum([float(i.amount)*float(i.price) for i in materials.filter(summ_or_dollar='суммы')])
    price_dollar = sum([float(i.amount)*float(i.price) for i in materials.filter(summ_or_dollar='доллары')])
    #### find currency
    url = 'https://bank.uz/currency'
    content = BeautifulSoup(requests.get(url).content, features='lxml')
    top_left = content.find('div', {'class':"diogram-top-left"})
    ul = top_left.find('ul', {'class': 'nav nav-tabs'})
    tabs_a = ul.find('div', {'class': 'tabs-a'})
    text = tabs_a.find_all('span', {'class': "medium-text"})
    currency = float(text[1].text.replace(' ', ''))
    #_________
    summ_to_dollar = round(float(price_summ / currency), 4)
    overall = price_dollar + summ_to_dollar
    context = {'materials': materials, 'type': type_for_filter, 'total_amount': total_amount, 'price_summ': price_summ, 'price_dollar': price_dollar,
    'currency': currency, 'summ_to_dollar': summ_to_dollar, 'overall': overall}
    return render(request, 'views/all_materials.html', context)

def all_salaries(request, type, title):

    del_salaries = Salary.objects.filter(title=None)
    for m in del_salaries:
        m.delete()
    if type == 'Все':
        if title == 'Все':
            salaries = Salary.objects.all()
        else:
            salaries = Salary.objects.filter(title=title)
    else:
        if title == 'Все':
            salaries = Salary.objects.filter(type=type)
        else:
            salaries = Salary.objects.filter(type=type, title=title)
    
    type_for_filter = 'Все'
    if type == 'flat':
        type_for_filter = 'Квартиры'
    elif type == 'plot':
        type_for_filter = 'Участки'
    price_summ = sum([float(i.price) for i in salaries.filter(summ_or_dollar='суммы')])
    price_dollar = sum([float(i.price) for i in salaries.filter(summ_or_dollar='доллары')])
    #### find currency
    #url = 'https://bank.uz/currency'
    #content = BeautifulSoup(requests.get(url).content, features='lxml')
    #top_left = content.find('div', {'class':"diogram-top-left"})
    #ul = top_left.find('ul', {'class': 'nav nav-tabs'})
    #tabs_a = ul.find('div', {'class': 'tabs-a'})
    #text = tabs_a.find_all('span', {'class': "medium-text"})
    #currency = float(text[1].text.replace(' ', ''))
    #_________
    summ_to_dollar = round(float(price_summ / currency()), 4)
    overall = price_dollar + summ_to_dollar
    allsalaries = []
    l = []
    for i in Salary.objects.all():
        if not i.title in l:
            allsalaries.append(i)
            l.append(i.title)


    context = {'salaries': salaries, 'type': type_for_filter, 'price_summ': price_summ, 'price_dollar': price_dollar,
    'currency': currency(), 'summ_to_dollar': summ_to_dollar, 'overall': overall, 'title': title, 'allsalaries': allsalaries}
    return render(request, 'views/all_salaries.html', context)

def report_foreman(request, foreman):
    all_foremans = Foreman.objects.all()
    if foreman == 'Все':
        transfers = transfer_money.objects.filter(transfered='True')
    else:
        transfers = transfer_money.objects.filter(transfered='True', foreman=foreman)
    account_summ = []
    account_dollar = []
    for i in transfers:
        s = Foreman.objects.get(name=i.foreman).account_summ
        if s == None:
            account_summ.append('')
        else:
            account_summ.append(s)
        d = Foreman.objects.get(name=i.foreman).account_dollar
        if s == None:
            account_dollar.append('')
        else:
            account_dollar.append(s)
        
    context = {'transfers': transfers, 'foreman': foreman, 'all_foremans': all_foremans, 'account_dollar': account_dollar, 'account_summ': account_summ}
    return render(request, 'views/report_foreman.html', context)
