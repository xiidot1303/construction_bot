from django.contrib import admin
from app.models import *
class ObjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'price')
admin.site.register(Object, ObjectAdmin)
admin.site.register(Foreman)
admin.site.register(Material)
admin.site.register(Salary)
admin.site.register(Client)
admin.site.register(Bot_users)

