from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from app.forms import *
from app.models import *
import xlrd

class ObjCreateView(LoginRequiredMixin, CreateView):
    template_name = 'create/create_obj.html'
    form_class = ObjForm
    success_url = '/object_detail/{id}'
    permanent = True

class ForemanCreateView(LoginRequiredMixin, CreateView):
    template_name = 'create/create_foreman.html'
    form_class = ForemanForm
    success_url = '/foreman_detail/{id}'
    permanent = True


class ClientCreateView(LoginRequiredMixin, CreateView):
    template_name = 'create/create_client.html'
    form_class = ClientForm
    success_url = '/client_detail/{id}'
    permanent = True


def create_material(request, object):

    m = Material.objects.create(obj=object)
    return redirect('/update_material/{}'.format(str(m.pk)))

class CategoryCreateView(LoginRequiredMixin, CreateView):
    template_name = 'create/create_category.html'
    form_class = CategoryForm
    success_url = '/categories'
    permanent = True

def create_salary(request, object):

    m = Salary.objects.create(obj=object)
    return redirect('/update_salary/{}'.format(str(m.pk)))



class Material_titleCreateView(LoginRequiredMixin, CreateView):
    template_name = 'create/create_material_title.html'
    form_class = Material_titleForm
    success_url = 'material_titles'
    permanent = True

class Salary_titleCreateView(LoginRequiredMixin, CreateView):
    template_name = 'create/create_salary_title.html'
    form_class = Salary_titleForm
    success_url = 'salary_titles'
    permanent = True
    
def create_incoming(request, obj):
    obj = Object.objects.get(pk=obj)
    client = Client.objects.filter(obj = obj)[0]

    incoming = Incoming.objects.create(client=client, object=obj, price_material_summ='0', price_material_dollar='0', 
    price_salary_summ='0', price_salary_dollar='0')
    return redirect('/incoming/{}'.format(str(incoming.pk)))

def create_material_by_excel(request):
    if request.method == 'POST':
        bbf = Material_excelFrom(request.POST, request.FILES)
        if bbf.is_valid():
            obj = bbf.cleaned_data['obj']
            type = bbf.cleaned_data['type']
            file = bbf.cleaned_data['file']
            # print(file)
            #get informations from excel file
            excel = Excel.objects.get_or_create(pk=1)
            excel = Excel.objects.get(pk=1)
            excel.file = file
            excel.save()
            book = xlrd.open_workbook('files/{}'.format(str(excel.file)))
            sheet = book.sheet_by_index(0)
            title = sheet.col(1)
            measurement = sheet.col(2)
            amount = sheet.col(3)
            price = sheet.col(4)
            all_summ = sheet.col(5)
            all_dollar = sheet.col(6)
            category = sheet.col(7)
            n = 3
            for t in title[3:]:
                if t.value == '':
                    break

                if all_summ[n].value == '':
                    currency = 'доллары'
                else:
                    currency = 'суммы'
                category_ = str(category[n].value)
                Category.objects.get_or_create(title=category_)
                category_ = Category.objects.filter(title=category_)[0]
                Material.objects.create(title = t.value, measurement = measurement[n].value, amount = str(amount[n].value), summ_or_dollar=currency, price=str(price[n].value).replace(',', ''), obj=obj, type=type, category=category_)
            

                n += 1
            



            # end excel
            return redirect(create_material_by_excel)
        else:
            objects = Object.objects.all()
            bbf = Material_excelFrom()
            context = {'form': bbf}
            return render(request, 'create/create_material_by_excel.html', context)
    else:
        objects = Object.objects.all()
        bbf = Material_excelFrom()
        context = {'form': bbf}
        return render(request, 'create/create_material_by_excel.html', context)