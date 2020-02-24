from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt

def index(request):
    return render(request,'index.html')

def register(request):
    errors = user.objects.reg_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags="reg")
        return redirect('/') 
    else:
        new_user = user.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode() )
        request.session['userid'] = new_user.id
    return redirect(f'/homepage')

def logout(request):
    request.session.clear()
    return redirect('/')

def login(request):
    errors = user.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags="log")
        return redirect('/')
    else:
        request.session['userid'] = user.objects.get(email=request.POST['email']).id
    return redirect("/homepage")
# ------------------------------------------------------------------------------------------------------------------end login/logout and registration form

def homepage(request):
    return render(request, 'homepage.html')

def saved_cities(request):
    return render(request, 'saved_cities.html')