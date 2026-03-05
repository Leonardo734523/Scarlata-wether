from django.shortcuts import render
import main

# Create your views here.


def get_locations(request): # Processes city and state variables too return geocoding data, then renders date in show-result.html

    city_name = request.POST.get("city")

    state_code = request.POST.get("state")

    if not city_name or not state_code :
        return render(request, "input-error.html")
    
    state_code = state_code.upper()

    locations = main.get_geocoding(city_name, state_code) # Can return a error message if the function fails

    if isinstance(locations, int): # Checks for error message
        error_message = main.api_error_handling(locations)
        return render(request, "server-error.html", {"error": error_message})

    organized_locations = main.organize_geocoding(locations)

    return render(request, "show-result.html", {"locations": organized_locations})



def home(request):

    return render(request, "home.html")



def local_weather(request): # Processes lat and lon variables too return weather forecast data, then renders date in show-weather.html

    lat = request.POST.get("lat")

    lon = request.POST.get("lon")

    weather = main.get_weather_forecast(lat, lon) # Can return a error message if the function fails

    if isinstance(weather, int): # Checks for error message
        error_message = main.api_error_handling(weather)
        return render(request, "server-error.html", {"error": error_message})

    organized_weather = main.organize_weather(weather)

    return render(request, "show-weather.html", {"weather": organized_weather})