from django.db import models

# Create your models here.

class user_details(models.Model):
    full_name = models.CharField(max_length=30)
    age  = models.IntegerField(max_length=100)
    gender = models.CharField(max_length=10)
    ph_number = models.IntegerField(max_length=10)
    mail_id = models.CharField()
    occup = models.CharField(max_length=30)

