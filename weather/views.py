from django.shortcuts import render
import requests

from weather import OPENWEATHER_API
from weather.models import City


def index(request):
    unit = 'metric'
    api_key = 'YOUR_API_KEY'
    cities = City.objects.all().order_by('name')
    weather_data = []

    for city in cities:
        #request the API data and convert the JSON to Python data types
        response = requests.get(OPENWEATHER_API.format(city.name, unit, api_key))
        if response.status_code == 200:
            city_weather = response.json()
            weather = {
                'city': city.name,
                'temperature': city_weather['main']['temp'],
                'temperature_unit': 'C',
                'description': city_weather['weather'][0]['description'],
                'icon': city_weather['weather'][0]['icon']
            }
        else:
            weather = {
                'city': city.name,
                'temperature': 'Not Available',
                'temperature_unit': '',
                'description': 'Not Available',
                'icon': ''
            }
        weather_data.append(weather)

    context = {'weather_data': weather_data}

    #returns the index.html template
    return render(request, 'weather/index.html', context)
