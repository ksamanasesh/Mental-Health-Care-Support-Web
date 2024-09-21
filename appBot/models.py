from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class user_details(models.Model):
    full_name = models.CharField()
    age  = models.IntegerField()
    gender = models.CharField()
    ph_number = models.IntegerField()
    mail_id = models.CharField()
    occup = models.CharField()

class ChatMesage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_msg = models.TextField()
    bot_resp = models.TextField()
    timestamp = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return (f"chat with {self.user.username} at {self.timestamp}")

