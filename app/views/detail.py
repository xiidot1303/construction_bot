from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from app.forms import *
from app.models import *

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
        foreman = Foreman.objects.get(obj__title=obj.obj)
        Obj = Object.objects.get(title=obj.obj)
        try:
            if obj.summ_or_dollar == 'суммы':
                Obj.price_summ = str(float(Obj.price_summ) - (float(obj.amount) * float(obj.price)))
                if obj.type == 'Квартира':
                    obj.type = 'flat'
                elif obj.type == 'Участка':
                    obj.type = 'plot'
                obj.save()

                if float(Obj.price_summ) < 0:
                    context['message'] = 'Недостаточно средств'
                    obj.delete()
                else:
                    Obj.save()
                    context['message'] = 'Успешно создано'
            else:
                Obj.price_dollar = str(float(Obj.price_dollar) - (float(obj.amount) * float(obj.price)))
                if obj.type == 'Квартира':
                    obj.type = 'flat'
                elif obj.type == 'Участка':
                    obj.type = 'plot'
                obj.save()

                if float(Obj.price_dollar) < 0:
                    context['message'] = 'Недостаточно средств'
                    obj.delete()
                else:
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
        foreman = Foreman.objects.get(obj__title=obj.obj)
        Obj = Object.objects.get(title=obj.obj)
        try:
            if obj.summ_or_dollar == 'суммы':
                Obj.price_summ = str(float(Obj.price_summ) - float(obj.price))
                if obj.type == 'Квартира':
                    obj.type = 'flat'
                elif obj.type == 'Участка':
                    obj.type = 'plot'
                obj.save()

                if float(Obj.price_summ) < 0:
                    context['message'] = 'Недостаточно средств'
                    obj.delete()
                else:
                    Obj.save()
                    context['message'] = 'Успешно создано'
            else:
                Obj.price_dollar = str(float(Obj.price_dollar) - float(obj.price))
                if obj.type == 'Квартира':
                    obj.type = 'flat'
                elif obj.type == 'Участка':
                    obj.type = 'plot'
                obj.save()

                if float(Obj.price_dollar) < 0:
                    context['message'] = 'Недостаточно средств'
                    obj.delete()
                else:
                    Obj.save()
                    context['message'] = 'Успешно создано'
        except:
            context['message'] = 'Значения введены неверно'
            obj.delete()
        context['pk'] = Object.objects.get(title=obj.obj).pk
        
        
        return context