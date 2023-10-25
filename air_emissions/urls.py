from django.urls import path
from .views import *



app_name="air_emissions"



urlpatterns = [

    
    # Clienti
    path("home/", dashboard_emissions, name="home"),
    
    

    
]