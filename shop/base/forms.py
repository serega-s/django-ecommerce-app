from .models import Customer
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms.forms import Form
from django.forms.models import ModelForm


class UserCreateForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'password1', 'password2', 'first_name')


class UserLoginForm(Form):
    username = forms.CharField(label='Email')
    password = forms.CharField(label='Password', widget = forms.PasswordInput)


class EditCustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email']