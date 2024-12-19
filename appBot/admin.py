from django.contrib import admin
from django.db import models

from .models import user_details,ChatMesage

# Register your models here.

class user_details_admin(admin.ModelAdmin):
    detail_list = ['full_name','age','gender','ph_number','mail_id','occup']

admin.site.register(user_details,user_details_admin)
admin.site.register(ChatMesage)
