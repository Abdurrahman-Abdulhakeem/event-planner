from django import forms

from .models import *
import re

class EventForm(forms.ModelForm):
    
    class Meta:
        model = Event
        fields = '__all__'
        exclude = ('user',)
        

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ('username', 'full_name', 'email', 'password', 'bio', )
        
    def clean_password(self):
        password = self.cleaned_data.get('password')
        
        if not re.search(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d@$!%*?&]{8,}$', password):
            raise forms.ValidationError('Password must be at least 8 characters long, contain letters and numbers, and can include special characters.')
        return password
    
class UpdateUserForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ('image', 'username', 'full_name', 'email', 'bio', )