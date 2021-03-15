from django.forms import ModelForm
from app.models import *
from django import forms


class ObjForm(ModelForm):
    class Meta:
        model = Object
        fields = {'title', 'price'}
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.TextInput(attrs={'class': 'form-control'})
        }
    field_order = ['title', 'price']

class ForemanForm(ModelForm):
    class Meta:
        model = Foreman
        fields = {'name', 'login', 'password', 'obj'}
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'login': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.TextInput(attrs={'class': 'form-control'}),
            'obj': forms.SelectMultiple(attrs={'class': 'form-control'})
        }
    field_order = ['name', 'login', 'password', 'obj']

class ClientForm(ModelForm):
    class Meta:
        model = Client
        fields = {'name', 'login', 'password', 'obj'}
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'login': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.TextInput(attrs={'class': 'form-control'}),
            'obj': forms.SelectMultiple(attrs={'class': 'form-control'})
        }
    field_order = ['name', 'login', 'password', 'obj']