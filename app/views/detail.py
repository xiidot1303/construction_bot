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