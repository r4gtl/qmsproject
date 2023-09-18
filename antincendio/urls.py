from django.urls import path
from .views import *




app_name="antincendio"



urlpatterns = [

    # Home
    path("", antincendio_home, name="antincendio_home"), 

    # Estintori
    path('aggiungi_estintore/', EstintoreCreateView.as_view(), name="aggiungi_estintore"), 
    path('modifica_estintore/<int:pk>/', EstintoreUpdateView.as_view(), name="modifica_estintore"), 
    path('delete_estintore/<int:pk>', delete_estintore, name="delete_estintore"),

    # Idranti
    path('aggiungi_idrante/', IdranteCreateView.as_view(), name="aggiungi_idrante"), 
    path('modifica_idrante/<int:pk>/', IdranteUpdateView.as_view(), name="modifica_idrante"), 
    path('delete_idrante/<int:pk>', delete_idrante, name="delete_idrante"),

    # Porte/Uscite
    path('aggiungi_porta_uscita/', PortaUscitaCreateView.as_view(), name="aggiungi_porta_uscita"), 
    path('modifica_porta_uscita/<int:pk>/', PortaUscitaUpdateView.as_view(), name="modifica_porta_uscita"), 
    path('delete_porta_uscita/<int:pk>', delete_porta_uscita, name="delete_porta_uscita"),
    
    # Attrezzatura
    path('aggiungi_attrezzatura_antincendio/', AttrezzaturaAntincendioCreateView.as_view(), name="aggiungi_attrezzatura_antincendio"), 
    path('modifica_attrezzatura_antincendio/<int:pk>/', AttrezzaturaAntincendioUpdateView.as_view(), name="modifica_attrezzatura_antincendio"), 
    path('delete_attrezzatura_antincendio/<int:pk>', delete_attrezzatura_antincendio, name="delete_attrezzatura_antincendio"),
    
    # Registri Antincendio
    path("registri_antincendio/", registro_controlli_home, name="registro_controlli_home"),
    path('registri_antincendio/aggiungi_registro_controlli/', RegistroControlliAntincendioCreateView.as_view(), name="aggiungi_registro_controlli"), 
    path('registri_antincendio/modifica_registro_controlli/<int:pk>/', RegistroControlliAntincendioUpdateView.as_view(), name="modifica_registro_controlli"), 
    path('registri_antincendio/delete_registro_controlli/<int:pk>', delete_registro_controlli, name="delete_registro_controlli"),
    
]