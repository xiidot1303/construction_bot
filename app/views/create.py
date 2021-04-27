from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from app.forms import *
from app.models import *
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
    