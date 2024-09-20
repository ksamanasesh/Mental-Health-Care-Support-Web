from django import forms
from .models import user_details
# Create your models here.

class userForm(forms.ModelForm):
    class Meta:
        model = user_details
        fields = ['full_name','age','gender','ph_number','mail_id','occup']