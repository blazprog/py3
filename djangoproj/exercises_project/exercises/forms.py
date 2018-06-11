__author__ = 'blazko'

from django import forms
from django.contrib.auth.models import User
from .models import Subject


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class SubjectForm(forms.ModelForm):

    class Meta:
        model = Subject
        fields = ("language", "subject") 

