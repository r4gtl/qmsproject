from django.urls import path

from .views import *

app_name="air_emissions"



urlpatterns = [

    
    # Dashboard
    path("dashboard/", dashboard_emissions, name="dashboard_emissions"),

    # Punti di Emissione
    path("aggiungi_punto_emissione/", PuntoEmissioneCreateView.as_view(), name="aggiungi_punto_emissione"),
    path("modifica_punto_emissione/<int:pk>", PuntoEmissioneUpdateView.as_view(), name="modifica_punto_emissione"),
    path("delete_punto_emissione/<int:pk>", delete_punto_emissione, name="delete_punto_emissione"),
    
    # Registro Analisi
    path("<int:fk_punto_emissione>/aggiungi_registro_analisi/", RegistroControlloAnaliticoCreateView.as_view(), name="aggiungi_registro_analisi"),
    path("<int:fk_punto_emissione>/modifica_registro_analisi/<int:pk>", RegistroControlloAnaliticoUpdateView.as_view(), name="modifica_registro_analisi"),
    path("delete_registro_analisi/<int:pk>", delete_registro_analisi, name="delete_registro_analisi"),

    # Stampe
    path("registro_controlli_analitici/", registro_controlli_analitici, name="registro_controlli_analitici"),
    

    
]