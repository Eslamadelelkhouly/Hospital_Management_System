from django.shortcuts import render , redirect
from django.contrib import messages
from django.contrib.auth import authenticate , login , logout
from userauths import forms as userauths_forms
# Create your views here.

def register_view(request):
    # if request.user.is_authenticated:
    #     messages.success(request , "You are Already loggged in")
    #     return redirect("/")
    
    form = userauths_forms.UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        full_name = form.cleaned_data.get("full_name")
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user_ = authenticate(email=email,password=password)
        login(request,user_)
        messages.success(request,"Account created successfully")
        return redirect("/")
    
    context = {
        "form":form
    }

    return render(request,"userauths/sign-up.html",context)