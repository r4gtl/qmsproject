from django.urls import path
from .views import *


app_name="ricette"

urlpatterns = [
    
    # Home Ricette
    path('', home_ricette, name='home_ricette'),  
    
    # Tabelle Generiche
    path('tabelle_generiche/', tabelle_generiche, name='tabelle_generiche'), 
    
    
    # Operazione Ricette
    path('aggiungi_operazione/', OperazioneRicetteCreateView.as_view(), name="aggiungi_operazione"), 
    path('modifica_operazione/<int:pk>/', OperazioneRicetteUpdateView.as_view(), name="modifica_operazione"), 
    path('delete_operazione/<int:pk>', delete_operazione, name="delete_operazione"),
    

    
    
]