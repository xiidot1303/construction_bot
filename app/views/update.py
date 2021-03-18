from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic.edit import UpdateView
from app.forms import *
from app.models import *

class ObjEditView(LoginRequiredMixin, UpdateView):
    model = Object
    form_class = ObjForm
    success_url = '/folder1/'
    

class ForemanEditView(LoginRequiredMixin, UpdateView):
    model = Foreman
    form_class = ForemanForm
    success_url = '/main/'
class ClientEditView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    success_url = '/main/'