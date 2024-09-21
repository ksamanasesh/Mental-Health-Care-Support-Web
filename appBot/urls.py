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
    path('admin/', admin.site.urls),
    path('test',views.testing,name='Testing'),
    path('home',views.home,name='MHCS Home'),
    path('signUp',views.signUp,name='MHCS SignUp'),
    path('signIn',views.signIn,name='MHCS SignIn'),
    path('signOut',views.signOut,name='MHCS SignOut'),
    path('details',views.user_profile,name='User Details'),
    path('user_profile_view',views.user_profile_view,name='View Details'),
    path('',views.chat_interface, name='chat_interface'),  # To render the chat UI
    path('chat/',views.chat, name='chat'),  # To handle chat requests (POST)
]
