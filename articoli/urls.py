from django.urls import path
from .views import (articoli_home,
                    ArticoloCreateView, ArticoloUpdateView,
                    
                    )

app_name="articoli"



urlpatterns = [

    # Home Articoli
    path("", articoli_home, name="articoli_home"),    
    path("crea_articolo/", ArticoloCreateView.as_view(), name="crea_articolo"),    
    path("modifica_articolo/<int:pk>", ArticoloUpdateView.as_view(), name="modifica_articolo"),    
    

    
]