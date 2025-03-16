from django.db import models
from django.contrib.auth.models import User

class UserDetails(models.Model):  # Changed to PascalCase (Django convention)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="details")  # Link with User model
    full_name = models.CharField(max_length=50)
    age = models.IntegerField()
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    ph_number = models.CharField(max_length=15, unique=True)  # Renamed to be clearer
    mail_id = models.EmailField(unique=True)  # Ensures only valid emails
    occup = models.CharField(max_length=25)

    def __str__(self):
        return self.full_name


class ChatMessage(models.Model):  # Fixed class name typo
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="chats")  # related_name for reverse lookup
    user_message = models.TextField()  # Improved field names
    bot_response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)  # auto_now_add to preserve original timestamp

    def __str__(self):
        return f"Chat with {self.user.username} at {self.timestamp.strftime('%Y-%m-%d %H:%M')}"
