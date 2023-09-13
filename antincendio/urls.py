from django.urls import path
from .views import *




app_name="antincendio"



urlpatterns = [

    # Home
    path("", antincendio_home, name="antincendio_home"), 
    

    
]