from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("search/", views.get_locations, name="searching"),
    path("weather/", views.local_weather, name="local")
]