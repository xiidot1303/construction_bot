from django.contrib import admin
from app.models import *
class ObjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'price')

class ForemanAdmin(admin.ModelAdmin):
    list_display = ('name', 'login', 'account_summ', 'account_dollar')

class MaterialAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'title', 'summ_or_dollar', 'price', 'obj')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)

class SalaryAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'title', 'summ_or_dollar', 'price', 'obj')

class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'login')

class IncomingAdmin(admin.ModelAdmin):
    list_display = ('client', 'object')


class Bot_usersAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'who', 'login')

class transfer_moneyAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'foreman', 'object', 'transfered')

admin.site.register(Object, ObjectAdmin)
admin.site.register(Foreman, ForemanAdmin)
admin.site.register(Material, MaterialAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Salary, SalaryAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Bot_users, Bot_usersAdmin)
admin.site.register(transfer_money, transfer_moneyAdmin)
admin.site.register(Incoming, IncomingAdmin)
