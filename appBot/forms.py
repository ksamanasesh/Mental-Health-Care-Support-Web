from django import forms
from .models import UserDetails
# Create your models here.

class userForm(forms.ModelForm):
    class Meta:
        model = UserDetails
        fields = ['full_name','age','gender','ph_number','mail_id','occup']