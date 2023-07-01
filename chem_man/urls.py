from django.urls import path

from .views import (home_prodotti_chimici,
                    
                    )




app_name = 'chem_man'

urlpatterns = [
    
    # Prodotti Chimici
    path('', home_prodotti_chimici, name="home_prodotti_chimici"),
    
]