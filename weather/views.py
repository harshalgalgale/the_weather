from django.shortcuts import render
import requests

from the_weather.settings import OW_API_KEY
from weather import OPENWEATHER_API
from weather.forms import CityForm
from weather.models import City


def index(request):
    unit = 'metric'
    cities = City.objects.all().order_by('name')

    # only true if form is submitted
    if request.method == 'POST':
        # add actual request data to form for processing
        form = CityForm(request.POST)
        # will validate and save if validate
        form.save()

    form = CityForm()
    weather_data = []

    for city in cities:
        #request the API data and convert the JSON to Python data types
        response = requests.get(OPENWEATHER_API.format(city.name, unit, OW_API_KEY))
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

    context = {'weather_data': weather_data, 'form': form}

    #returns the index.html template
    return render(request, 'weather/index.html', context)
