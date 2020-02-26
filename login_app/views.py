from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt
import requests
from django_plotly_dash import DjangoDash
import dash
import dash_core_components as dcc
import dash_html_components as html
from login_app.graph_apps import *


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
    pollution_url = 'https://api.waqi.info/feed/{}/?token=7d948b48a98a28662fa192ada26908dab5923434'
    
    if request.method=='POST':
        city = request.POST['city']
    else:
        city = 'Seattle'

    pollution_r = requests.get(pollution_url.format(city)).json()
    try:
        print(pollution_r)
    except KeyError:
        messages.error(request, "City name not found.")
        return redirect ('/homepage')
    aqi = pollution_r['data']['aqi']
    # this is the checks for the color and impact of the AQI
    if aqi < 50:
        color = '#096'
        impact = "Good"
    elif aqi < 100:
        color = '#ffde33'
        impact = "Moderate"
    elif aqi <150:
        color = '#ff9933'
        impact = "Unhealthy for sensative groups"
    elif aqi < 200:
        color = '#c03'
        impact = "Unhealthy"
    elif aqi < 300:
        color = '#609'
        impact = "Very unhealthy"
    elif aqi < 500:
        color = '#7e0023'
        impact = "Hazardous"

  

    city_AQI = {
        'city' : city,
        'aqi' : aqi,
        'impact': impact,
        'color' : color,
    }

    weather_url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=6aac762c309ab62e1a9c2663d6aff64a'


    weather_r = requests.get(weather_url.format(city)).json()

    try:
        print(weather_r)
    except KeyError:
        messages.error(request, "City name not found.")
        return redirect ('/homepage')

    city_weather = {
        'city': city,
        'temperature':weather_r['main']['temp'],
        'icon': weather_r['weather'][0]['icon']
    }
    
    context = {
        'city_weather':city_weather,
        'city_AQI' : city_AQI
    }
    return render(request, 'homepage.html', context)

def saved_cities(request):
    this_user = user.objects.get(id=request.session['userid'])
    these_cities = City.objects.filter(added_by = this_user)
    context = {
        'cities':these_cities
    }
    return render(request, 'saved_cities.html', context)

def save_new_city(request):
    this_user = user.objects.get(id=request.session['userid'])

    City.objects.create(city_name=request.POST['savecity'], temp= int(float(request.POST['temp'])), aqi = int(request.POST['aqi']), added_by=this_user)

    return redirect('/homepage')

def my_cities_plot(request):
    this_user = user.objects.get(id=request.session['userid'])
    context = {
        'user': this_user
    }
    return render(request, 'my_plot.html')