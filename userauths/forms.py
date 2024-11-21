from django import forms   # import forms
from django.contrib.auth.forms import UserCreationForm   # Library Create Form
from userauths.models import User     # import models from app userauths


# widget = froms.TextInput() -> input in templates

class UserRegisterForm(UserCreationForm):
    full_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control' , 'placeholder':'Name'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control' , 'placeholder':'Email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control' , 'placeholder':'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control' , 'placeholder':'Again password'}))

    class Meta:
        model = User
        fields = ['full_name','email','password1','password2']


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control' , 'placeholder':'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control' , 'placeholder':'Password'}))

    class Meta:
        model = User
        fields = ['email','password']
