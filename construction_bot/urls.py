"""construction_bot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeDoneView, PasswordChangeView
from django.urls import path
from app.views.main import *
from app.views.create import *
from app.views.update import *
from app.views.detail import *
from app.views.delete import *
from dotenv import load_dotenv
import os
from django.conf import settings
from django.conf.urls.static import static
basedir = os.path.abspath(os.path.dirname(''))
load_dotenv(os.path.join(basedir, '.env'))
TOKEN = os.environ.get('TOKEN')
urlpatterns = [
    
    path('admin/', admin.site.urls),
    path('accounts/login/', LoginView.as_view()),
    path('main/', objects),
    path('', objects, name='main'),
    #start bot
    path(TOKEN, bot_webhook, name='bot'),
    
    
    ## Objects
    path('objects', objects, name='objects'),
    path('create_obj', ObjCreateView.as_view(), name='create_obj'),
    path('update_obj/<int:pk>/', ObjEditView.as_view(), name='update_obj'),
    path('object_detail/<int:pk>/', ObjDetailView.as_view()),
    path('delete_object/<int:pk>/', delete_object, name='delete_object'),


    # Foremans
    path('create_foreman', ForemanCreateView.as_view(), name='create_foreman'),
    path('update_foreman/<int:pk>/', ForemanEditView.as_view(), name='update_foreman'),
    path('foreman_detail/<int:pk>', ForemanDetailView.as_view()),
    path('delete_foreman/<int:pk>/', delete_foreman, name='delete_foreman'),
    
    #Clients
    path('create_client', ClientCreateView.as_view(), name='create_client'),
    path('update_client/<int:pk>/', ClientEditView.as_view(), name = 'update_client'),
    path('client_detail/<int:pk>', ClientDetailView.as_view()),
    path('delete_client/<int:pk>/', delete_client, name='delete_client'),
    #requests
    path('folder1', folder_foremans, name='folder_foremans'),
    path('folder2', folder_clients, name='folder_clients'),

    #material
    path('material/<str:obj>/', material, name='material'),
    path('sort_material/<str:obj>/<str:type>/', sort_material, name='sort_material'),
    path('delete_material/<int:pk>/', delete_material, name='delete_material'),
    path('create_material/<str:object>/', create_material, name='create_material'),
    path('update_material/<int:pk>/', MaterialEditView.as_view()),
    path('material_detail/<int:pk>/', MaterialDetailView.as_view()),
    
    #salary
    path('salary/<str:obj>/', salary, name='salary'),
    path('sort_salary/<str:obj>/<str:title>/<str:type>/', sort_salary, name='sort_salary'),
    path('delete_salary/<int:pk>/', delete_salary, name='delete_salary'),
    path('create_salary/<str:object>/', create_salary, name='create_salary'),
    path('update_salary/<int:pk>/', SalaryEditView.as_view()),
    path('salary_detail/<int:pk>/', SalaryDetailView.as_view()),
    #material_title
    path('material_titles', material_title, name='material_titles'),
    path('create_material_title', Material_titleCreateView.as_view(), name='create_material_title'),
    path('delete_material_title/<int:pk>', delete_material_title, name = 'delete_material_title'),

    #salary_title
    path('salary_titles', salary_title, name='salary_titles'),
    path('create_salary_title', Salary_titleCreateView.as_view(), name='create_salary_title'),
    path('delete_salary_title/<int:pk>', delete_salary_title, name = 'delete_salary_title'),

    # get files
    path('get_excel/<str:file_path>', get_excel, name='get_excel'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

