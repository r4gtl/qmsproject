from django.urls import path

from .reports import *
from .utils import *
from .views import *

app_name="ricette"

urlpatterns = [
    
    # Home Ricette
    path('', home_ricette, name='home_ricette'),  
    path('ricette_rifinizione/', home_ricette_rifinizione, name='home_ricette_rifinizione'),  
    
    # Tabelle Generiche
    path('tabelle_generiche/', tabelle_generiche, name='tabelle_generiche'), 
    
    
    # Operazione Ricette
    path('aggiungi_operazione/', OperazioneRicetteCreateView.as_view(), name="aggiungi_operazione"), 
    path('modifica_operazione/<int:pk>/', OperazioneRicetteUpdateView.as_view(), name="modifica_operazione"), 
    path('delete_operazione/<int:pk>', delete_operazione, name="delete_operazione"),

    # Ricette Rifinizione
    path('aggiungi_ricetta_rifinizione/', RicettaRifinizioneCreateView.as_view(), name="aggiungi_ricetta_rifinizione"), 
    path('modifica_ricetta_rifinizione/<int:pk>/', RicettaRifinizioneUpdateView.as_view(), name="modifica_ricetta_rifinizione"), 
    path('delete_ricetta_rifinizione/<int:pk>', delete_ricetta_rifinizione, name="delete_ricetta_rifinizione"),
    path('aggiungi_revisione_rifinizione/', RevisioneRicettaRifinizioneCreateView.as_view(), name="aggiungi_revisione_rifinizione"), 

    # Dettaglio Ricette Rifinizione
    path('<int:fk_ricetta_rifinizione>/aggiungi_dettaglio_ricetta_rifinizione/', DettaglioRicettaRifinizioneCreateView.as_view(), name="aggiungi_dettaglio_ricetta_rifinizione"), 
    path('<int:fk_ricetta_rifinizione>/modifica_dettaglio_ricetta_rifinizione/<int:pk>/', DettaglioRicettaRifinizioneUpdateView.as_view(), name="modifica_dettaglio_ricetta_rifinizione"), 
    path('delete_dettaglio_ricetta_rifinizione/<int:pk>', delete_dettaglio_ricetta_rifinizione, name="delete_dettaglio_ricetta_rifinizione"),
    
    # Cerca prodotto chimico
    path('search_prodotto_chimico/', search_prodotto_chimico, name="search_prodotto_chimico"),


    # Stampa ricette
    path('ricetta_rifinizione_print/<int:pk>', ricetta_rifinizione_print, name="ricetta_rifinizione_print"),
    
    
]
    
    
