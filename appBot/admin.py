from django.contrib import admin
from django.db import models

from .models import user_details,ChatMesage

# Register your models here.
admin.site.register(user_details)
admin.site.register(ChatMesage)
