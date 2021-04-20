from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic.edit import UpdateView
from app.forms import *
from app.models import *

class ObjEditView(LoginRequiredMixin, UpdateView):
    model = Object
    form_class = ObjForm
    success_url = '/folder1'
    

class ForemanEditView(LoginRequiredMixin, UpdateView):
    model = Foreman
    form_class = ForemanForm
    success_url = '/folder1'
    #def get_context_data(self, *args, **kwargs):
    #    content = super().get_context_data(*args, **kwargs)
    #    obj = cn
class ClientEditView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    success_url = '/folder2'

class MaterialEditView(LoginRequiredMixin, UpdateView):
    model = Material
    form_class = MaterialForm
    success_url = '/material_detail/{id}'


class SalaryEditView(LoginRequiredMixin, UpdateView):
    model = Salary
    form_class = SalaryForm
    success_url = '/salary_detail/{id}'
