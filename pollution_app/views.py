from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt

def pollution(request):
    return render(request,'pollution.html')