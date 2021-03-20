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