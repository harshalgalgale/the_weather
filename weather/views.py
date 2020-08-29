from django.shortcuts import render

def index(request):
    return render(request, 'weather/index.html') #returns the index.html template