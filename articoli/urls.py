from django.urls import path
from .views import *

app_name="articoli"



urlpatterns = [

    # Home Articoli
    path("", articoli_home, name="articoli_home"),    
    path("crea_articolo/", ArticoloCreateView.as_view(), name="crea_articolo"),    
    path("modifica_articolo/<int:pk>", ArticoloUpdateView.as_view(), name="modifica_articolo"),    
    path("delete_articolo/<int:pk>", delete_articolo, name="delete_articolo"), 
    
    # Home Colori
    path("colori/", colori_home, name="colori_home"),    
    path("colori/crea_colore/", ColoreCreateView.as_view(), name="crea_colore"),    
    path("colori/modifica_colore/<int:pk>", ColoreUpdateView.as_view(), name="modifica_colore"),    
    path("colori/delete_colore/<int:pk>", delete_colore, name="delete_colore"),    
    
    # Tabelle Generiche
    path("tabelle_generiche/", tabelle_generiche, name="tabelle_generiche"),

    # Fasi di Lavoro       
    path("crea_fase_lavoro/", FaseLavoroCreateView.as_view(), name="crea_fase_lavoro"),    
    path("modifica_fase_lavoro/<int:pk>", FaseLavoroUpdateView.as_view(), name="modifica_fase_lavoro"),    
    path("delete_fase_lavoro/<int:pk>", delete_fase_lavoro, name="delete_fase_lavoro"), 
    
    # Elenco Test      
    path("crea_test/", ElencoTestCreateView.as_view(), name="crea_test"),    
    path("modifica_test/<int:pk>", ElencoTestUpdateView.as_view(), name="modifica_test"),    
    path("delete_test/<int:pk>", delete_test, name="delete_test"), 

    
]