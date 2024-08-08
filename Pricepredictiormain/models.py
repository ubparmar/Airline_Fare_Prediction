# forms.py
from django import forms
from django.contrib.auth.models import User
from django.db import models

class ProfileEditForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), required=False)
    password_confirm = forms.CharField(widget=forms.PasswordInput(), required=False)
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password']
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        
        if password and password != password_confirm:
            self.add_error('password_confirm', "Passwords do not match")
        
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user
class Contact(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)  # Email is optional
    subject = models.CharField(max_length=100)
    message = models.TextField()

    def __str__(self):
        return self.full_name