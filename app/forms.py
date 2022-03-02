from django.forms import ModelForm
from app.models import *
from django import forms


class ObjForm(ModelForm):
    class Meta:
        model = Object
        fields = {'title', 'price_material_summ', 'price_material_dollar', 'price_salary_summ', 'price_salary_dollar'}
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'price_material_summ': forms.TextInput(attrs={'class': 'form-control'}),
            'price_material_dollar': forms.TextInput(attrs={'class': 'form-control'}),
            'price_salary_summ': forms.TextInput(attrs={'class': 'form-control'}),
            'price_salary_dollar': forms.TextInput(attrs={'class': 'form-control'})

        }
        labels = {
            'title': 'Название',
            'price_material_summ': 'Остаток денег для материалов (Сумм)',
            'price_material_dollar': 'Остаток денег для материалов ($)',
            'price_salary_summ': 'Остаток денег для иш хакки (Сумм)',
            'price_salary_dollar': 'Остаток денег для иш хакки ($)'
        }
    field_order = ['title', 'price_material_summ', 'price_material_dollar', 'price_salary_summ', 'price_salary_dollar']

class ForemanForm(ModelForm):
    class Meta:
        model = Foreman
        fields = {'name', 'login', 'password', 'obj', 'account_summ', 'account_dollar'}
        labels = {
            'name': 'Имя',
            'login': 'Логин',
            'password': 'Пароль',
            'obj': 'Объекты (Выберите несколько объектов с помощью Ctrl)',
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
        fields = {'name', 'login', 'password', 'obj', 'type'}
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'login': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.TextInput(attrs={'class': 'form-control'}),
            'obj': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}, choices=[('Квартира', 'Квартира'), ('Участка', 'Участка')]),
        }
        labels = {
            'name': 'Имя',
            'login': 'Логин',
            'password': 'Пароль',
            'obj': 'Объекты',
            'type': 'Тип'
        }
    field_order = ['name', 'login', 'password', 'type', 'obj']



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
        fields = {'title', 'measurement', 'amount', 'summ_or_dollar', 'price', 'type', 'category'}
        labels = {
            'title': 'Названия',
            'measurement': 'Единицу измерения',
            'amount': 'Количество',
            'summ_or_dollar': 'Валюта',
            'price': 'Цена',
            'type': 'Тип', 
            'category': 'Категория'
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'measurement': forms.Select(attrs={'class': 'form-control'}, choices=[('м', 'м'), ('кг', 'кг'), ('м^3', 'м^3'), ('м^2', 'м^2'), ('шт', 'шт')]),
            'amount': forms.TextInput(attrs={'class': 'form-control'}),
            'summ_or_dollar': forms.Select(attrs={'class': 'form-control'}, choices=[('суммы', 'суммы'), ('доллары', 'доллары')]),
            'price': forms.TextInput(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}, choices=[('Квартира', 'Квартира'), ('Участка', 'Участка')]),
            'category': forms.Select(attrs={'class': 'form-control'})
        }
    field_order = ['title', 'category', 'measurement', 'amount', 'summ_or_dollar', 'price', 'type']

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = {'title'}
        labels = {
            'title': 'Названия'
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
        }


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