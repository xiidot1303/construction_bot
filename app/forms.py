from django.forms import ModelForm
from app.models import *
from django import forms


class ObjForm(ModelForm):
    class Meta:
        model = Object
        fields = {'title', 'price_summ', 'price_dollar'}
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'price_summ': forms.TextInput(attrs={'class': 'form-control'}),
            'price_dollar': forms.TextInput(attrs={'class': 'form-control'})

        }
        labels = {
            'title': 'Название',
            'price_summ': 'Остаток денег (Сумм)',
            'price_dollar': 'Остаток денег (Доллар)'
        }
    field_order = ['title', 'price_summ', 'price_dollar']

class ForemanForm(ModelForm):
    class Meta:
        model = Foreman
        fields = {'name', 'login', 'password', 'obj'}
        labels = {
            'name': 'Имя',
            'login': 'Логин',
            'password': 'Пароль',
            'obj': 'Объекты'
        }
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
        labels = {
            'name': 'Имя',
            'login': 'Логин',
            'password': 'Пароль',
            'obj': 'Объекты'
        }
    field_order = ['name', 'login', 'password', 'obj']