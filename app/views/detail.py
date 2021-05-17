from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from app.forms import *
from app.models import *
from bot.functions import *
class ForemanDetailView(LoginRequiredMixin, DetailView):
    model = Foreman
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        obj = context['object']
        context['message'] = 'Успешно добавлен новый прораб'
        context['name'] = 'Имя: {}'.format(obj.name)
        return context



class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        obj = context['object']
        context['message'] = 'Успешно добавлен новый Клиент'
        context['name'] = 'Имя: {}'.format(obj.name)
        return context


class ObjDetailView(LoginRequiredMixin, DetailView):
    model = Object
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        obj = context['object']
        context['title'] = 'Название: {}'.format(obj.title)
        return context

class MaterialDetailView(LoginRequiredMixin, DetailView):
    model = Material
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        obj = context['object']
        Obj = Object.objects.get(title=obj.obj)
        try:
            if obj.summ_or_dollar == 'суммы':
                Obj.price_material_summ = str(float(Obj.price_material_summ) - (float(obj.amount) * float(obj.price)))
                Obj.price_material_dollar = str(float(Obj.price_material_dollar) - (summ_to_dollar(float(obj.amount) * float(obj.price))))
                if obj.type == 'Квартира':
                    obj.type = 'flat'
                elif obj.type == 'Участка':
                    obj.type = 'plot'
                obj.save()

                
                Obj.save()
                context['message'] = 'Успешно создано'
            else:
                Obj.price_material_dollar = str(float(Obj.price_material_dollar) - (float(obj.amount) * float(obj.price)))
                Obj.price_material_summ = str(float(Obj.price_material_summ) - (dollar_to_summ(float(obj.amount) * float(obj.price))))
                if obj.type == 'Квартира':
                    obj.type = 'flat'
                elif obj.type == 'Участка':
                    obj.type = 'plot'
                obj.save()

                Obj.save()
                context['message'] = 'Успешно создано'
        except:
            context['message'] = 'Значения введены неверно'
            obj.delete()
        context['pk'] = Object.objects.get(title=obj.obj).pk
        
        
        return context




class SalaryDetailView(LoginRequiredMixin, DetailView):
    model = Salary
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        obj = context['object']
    
        Obj = Object.objects.get(title=obj.obj)
        try:
            if obj.summ_or_dollar == 'суммы':
                Obj.price_salary_summ = str(float(Obj.price_salary_summ) - float(obj.price))
                Obj.price_salary_dollar = str(float(Obj.price_salary_dollar) - (summ_to_dollar(obj.price)))
                if obj.type == 'Квартира':
                    obj.type = 'flat'
                elif obj.type == 'Участка':
                    obj.type = 'plot'
                obj.save()

                Obj.save()
                context['message'] = 'Успешно создано'
            else:
                Obj.price_salary_dollar = str(float(Obj.price_salary_dollar) - float(obj.price))
                Obj.price_salary_summ = str(float(Obj.price_salary_summ) - (dollar_to_summ(obj.price)))
                if obj.type == 'Квартира':
                    obj.type = 'flat'
                elif obj.type == 'Участка':
                    obj.type = 'plot'
                obj.save()

                Obj.save()
                context['message'] = 'Успешно создано'
        except:
            context['message'] = 'Значения введены неверно'
            obj.delete()
        context['pk'] = Object.objects.get(title=obj.obj).pk
        
        
        return context