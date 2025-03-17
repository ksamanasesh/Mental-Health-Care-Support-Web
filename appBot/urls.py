"""
URL configuration for mental_Health_Bot project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path
from . import views

urlpatterns = [
    path('test',views.testing,name='Testing'),
    path('',views.home,name='home'),
    path('about',views.about,name='about'),
    path('service',views.service,name='service'),
    path('design',views.design,name='design'),
    path('contact',views.contact,name='contact'),
    path('signUp',views.signUp,name='signUp'),
    path('signIn',views.signIn,name='signIn'),
    path('signOut',views.signOut,name='signOut'),
    path('details',views.user_profile,name='details'),
    path('user_profile_view',views.user_profile_view,name='user_profile_view'),
    path('chatbot/chat/', views.chat_view, name='g'),
    path('chat/', views.chat_page, name='chat'),
    path('dashboard/', views.chatbot_dashboard, name='chatbot_dashboard'),
    path('get_chat_data/', views.get_chat_data, name='get_chat_data'),
]
