from django.urls import path
from .views import (articoli_home,
                    
                    )

app_name="articoli"



urlpatterns = [

    # Home Articoli
    path("", articoli_home, name="articoli_home"),    
    

    
]