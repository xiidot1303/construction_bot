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
from dotenv import load_dotenv
import os
basedir = os.path.abspath(os.path.dirname(''))
load_dotenv(os.path.join(basedir, '.env'))
TOKEN = os.environ.get('TOKEN')
urlpatterns = [
    
    path('admin/', admin.site.urls),
    path('accounts/login/', LoginView.as_view()),
    path('main/', main_menu),
    path('', main_menu),
    #start bot
    path(TOKEN, bot_webhook, name='bot'),
    ## Objects
    path('create_obj', ObjCreateView.as_view(), name='create_obj'),
    path('update_obj/<int:pk>/', ObjEditView.as_view(), name='update_obj'),
    
    # Foremans
    path('create_foreman', ForemanCreateView.as_view(), name='create_foreman'),
    path('update_foreman/<int:pk>/', ForemanEditView.as_view(), name='update_foreman'),

    #Clients
    path('create_client', ClientCreateView.as_view(), name='create_client'),
    path('update_client/<int:pk>/', ClientEditView.as_view(), name = 'udpate_client'),

    #requests
    path('folder1', folder_foremans, name='folder_foremans'),
    path('folder2', folder_clients, name='folder_clients'),

    #material
    path('material/<str:obj>/', material, name='material'),


    #salary
    path('salary/<str:obj>/', salary, name='salary'),
]
