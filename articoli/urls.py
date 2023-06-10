from django.urls import path
from .views import (articoli_home,
                    ArticoloCreateView, ArticoloUpdateView, delete_articolo,
                    
                    )

app_name="articoli"



urlpatterns = [

    # Home Articoli
    path("", articoli_home, name="articoli_home"),    
    path("crea_articolo/", ArticoloCreateView.as_view(), name="crea_articolo"),    
    path("modifica_articolo/<int:pk>", ArticoloUpdateView.as_view(), name="modifica_articolo"),    
    path("delete_articolo/<int:pk>", delete_articolo, name="delete_articolo"),    
    

    
]