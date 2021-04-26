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
        fields = {'name', 'login', 'password', 'obj', 'account_summ', 'account_dollar'}
        labels = {
            'name': 'Имя',
            'login': 'Логин',
            'password': 'Пароль',
            'obj': 'Объекты',
            'account_summ': 'Счёт (сумм)',
            'account_dollar': 'Счёт (доллар)'
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'login': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.TextInput(attrs={'class': 'form-control'}),
            'obj': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'account_summ': forms.TextInput(attrs={'class': 'form-control'}),
            'account_dollar': forms.TextInput(attrs={'class': 'form-control'}),
        }
    field_order = ['name', 'login', 'password', 'obj', 'account_summ', 'account_dollar']

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



class Material_titleForm(ModelForm):
    class Meta:
        model = Material_title
        fields = {'title'}
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
        }
    field_order = ['title']


class Salary_titleForm(ModelForm):
    class Meta:
        model = Salary_title
        fields = {'title'}
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
        }
    field_order = ['title']

class MaterialForm(ModelForm):
    class Meta:
        model = Material
        fields = {'title', 'measurement', 'amount', 'summ_or_dollar', 'price', 'type'}
        labels = {
            'title': 'Названия',
            'measurement': 'Единицу измерения',
            'amount': 'Количество',
            'summ_or_dollar': 'Валюта',
            'price': 'Цена',
            'type': 'Тип'
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'measurement': forms.Select(attrs={'class': 'form-control'}, choices=[('м', 'м'), ('кг', 'кг'), ('м^3', 'м^3'), ('м^2', 'м^2')]),
            'amount': forms.TextInput(attrs={'class': 'form-control'}),
            'summ_or_dollar': forms.Select(attrs={'class': 'form-control'}, choices=[('суммы', 'суммы'), ('доллары', 'доллары')]),
            'price': forms.TextInput(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}, choices=[('Квартира', 'Квартира'), ('Участка', 'Участка')]),
        }
    field_order = ['title', 'measurement', 'amount', 'summ_or_dollar', 'price', 'type']


class SalaryForm(ModelForm):
    class Meta:
        model = Material
        fields = {'title', 'summ_or_dollar', 'price', 'type'}
        labels = {
            'title': 'Названия',
            'summ_or_dollar': 'Валюта',
            'price': 'Цена',
            'type': 'Тип'
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'summ_or_dollar': forms.Select(attrs={'class': 'form-control'}, choices=[('суммы', 'суммы'), ('доллары', 'доллары')]),
            'price': forms.TextInput(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}, choices=[('Квартира', 'Квартира'), ('Участка', 'Участка')]),
        }
    field_order = ['title', 'summ_or_dollar', 'price', 'type']