from django import forms   # import forms
from django.contrib.auth.forms import UserCreationForm   # Library Create Form
from userauths.models import User     # import models from app userauths


# widget = froms.TextInput() -> input in templates

USER_TYPE = [
    ("Doctor" , "Doctor"),
    ("Patient" , "Patient"),
]

class UserRegisterForm(UserCreationForm):
    full_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control' , 'placeholder':'Eslam adel'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control' , 'placeholder':'eslam@gmail.com'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control' , 'placeholder':'***********'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control' , 'placeholder':'***********'}))
    user_type = forms.ChoiceField(choices=USER_TYPE , widget=forms.Select(attrs={'class':'form-select' }))

    class Meta:
        model = User
        fields = ['full_name','email','password1','password2', 'user_type']


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control' , 'placeholder':'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control' , 'placeholder':'Password'}))

    class Meta:
        model = User
        fields = ['email','password']
