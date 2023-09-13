from django.urls import path
from .views import home_ricette


app_name="ricette"

urlpatterns = [
    
    # Home Ricette
    path('', home_ricette, name='home_ricette'),    

    
    
]