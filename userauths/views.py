from django.shortcuts import render , redirect
from django.contrib import messages
from userauths import forms as userauths_forms
# Create your views here.

def register_view(request):
    if request.user.is_authenticated:
        messages.success(request , "You are Already loggged in")
        return redirect("/")
    
    form = userauths_forms.UserRegisterForm()
    
    context = {
        "form":form
    }

    return render(request,"userauths/sign-up.html",context)