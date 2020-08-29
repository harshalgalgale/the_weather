from django.shortcuts import render
import requests

from weather import OPENWEATHER_API


def index(request):
    unit = 'metric'
    city = 'London'
    api_key = 'YOUR_API_KEY'
    #request the API data and convert the JSON to Python data types
    response = requests.get(OPENWEATHER_API.format(city, unit, api_key))
    if response.status_code == 200:
        city_weather = response.json()
        weather = {
            'city': city,
            'temperature': city_weather['main']['temp'],
            'temperature_unit': 'C',
            'description': city_weather['weather'][0]['description'],
            'icon': city_weather['weather'][0]['icon']
        }
    else:
        weather = {
            'city': city,
            'temperature': 'Not Available',
            'temperature_unit': '',
            'description': 'Not Available',
            'icon': ''
        }
    context = {'weather': weather}

    #returns the index.html template
    return render(request, 'weather/index.html', context)
