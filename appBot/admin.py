from django.contrib import admin
from django.db import models

from .models import UserDetails,ChatMessage
# Register your models here.

class user_details_admin(admin.ModelAdmin):
    detail_list = ['full_name','age','gender','ph_number','mail_id','occup']

admin.site.register(UserDetails,user_details_admin)
admin.site.register(ChatMessage)
