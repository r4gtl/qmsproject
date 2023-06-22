from django.urls import path
from .views import (gestione_rifiuti_home,
)



app_name="gestionerifiuti"



urlpatterns = [

    # Home
    path("", gestione_rifiuti_home, name="gestione_rifiuti_home"),    
    
    

    
]