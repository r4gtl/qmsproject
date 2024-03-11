from django.urls import path

from .reports import *
from .utils import *
from .views import *

app_name="ricette"

urlpatterns = [
    
    # Home Ricette
    path('', home_ricette, name='home_ricette'),  
    path('ricette_rifinizione/', home_ricette_rifinizione, name='home_ricette_rifinizione'),  
    path('ricette_bagnato/', home_ricette_bagnato, name='home_ricette_bagnato'),  
    path('ricette_colori_rifinizione/', home_ricette_colori_rifinizione, name='home_ricette_colori_rifinizione'),  
    
    # Tabelle Generiche
    path('tabelle_generiche/', tabelle_generiche, name='tabelle_generiche'), 
    
    
    # Operazione Ricette
    path('aggiungi_operazione/', OperazioneRicetteCreateView.as_view(), name="aggiungi_operazione"), 
    path('modifica_operazione/<int:pk>/', OperazioneRicetteUpdateView.as_view(), name="modifica_operazione"), 
    path('delete_operazione/<int:pk>', delete_operazione, name="delete_operazione"),

    # Ricette Rifinizione
    path('aggiungi_ricetta_rifinizione/', RicettaRifinizioneCreateView.as_view(), name="aggiungi_ricetta_rifinizione"), 
    path('modifica_ricetta_rifinizione/<int:pk>/', RicettaRifinizioneUpdateView.as_view(), name="modifica_ricetta_rifinizione"), 
    path('modifica_dettaglio_ricetta_rifinizione_with_focus_button/<int:pk>/<str:focus_button>/', RicettaRifinizioneUpdateView.as_view(), name="modifica_dettaglio_ricetta_rifinizione_with_focus_button"), 
    path('delete_ricetta_rifinizione/<int:pk>', delete_ricetta_rifinizione, name="delete_ricetta_rifinizione"),
    

    # Dettaglio Ricette Rifinizione
    path('<int:fk_ricetta_rifinizione>/aggiungi_dettaglio_ricetta_rifinizione/', DettaglioRicettaRifinizioneCreateView.as_view(), name="aggiungi_dettaglio_ricetta_rifinizione"), 
    path('<int:fk_ricetta_rifinizione>/modifica_dettaglio_ricetta_rifinizione/<int:pk>/', DettaglioRicettaRifinizioneUpdateView.as_view(), name="modifica_dettaglio_ricetta_rifinizione"), 
    path('delete_dettaglio_ricetta_rifinizione/<int:pk>', delete_dettaglio_ricetta_rifinizione, name="delete_dettaglio_ricetta_rifinizione"),
    

    # Ricette Colore Rifinizione
    path('aggiungi_ricetta_colore_rifinizione/', RicettaColoreRifinizioneCreateView.as_view(), name="aggiungi_ricetta_colore_rifinizione"), 
    path('modifica_ricetta_colore_rifinizione/<int:pk>/', RicettaColoreRifinizioneUpdateView.as_view(), name="modifica_ricetta_colore_rifinizione"), 
    path('delete_ricetta_colore_rifinizione/<int:pk>', delete_ricetta_colore_rifinizione, name="delete_ricetta_colore_rifinizione"),

    # Dettaglio Ricette Colore Rifinizione
    path('<int:fk_ricetta_colore_rifinizione>/aggiungi_dettaglio_ricetta_colore_rifinizione/', DettaglioRicettaColoreRifinizioneCreateView.as_view(), name="aggiungi_dettaglio_ricetta_colore_rifinizione"), 
    path('<int:fk_ricetta_colore_rifinizione>/modifica_dettaglio_ricetta_colore_rifinizione/<int:pk>/', DettaglioRicettaColoreRifinizioneUpdateView.as_view(), name="modifica_dettaglio_ricetta_colore_rifinizione"), 
    path('delete_dettaglio_ricetta_colore_rifinizione/<int:pk>', delete_dettaglio_ricetta_colore_rifinizione, name="delete_dettaglio_ricetta_colore_rifinizione"),

    # Ricette bagnato
    path('aggiungi_ricetta_bagnato/', RicettaBagnatoCreateView.as_view(), name="aggiungi_ricetta_bagnato"), 
    path('modifica_ricetta_bagnato/<int:pk>/', RicettaBagnatoUpdateView.as_view(), name="modifica_ricetta_bagnato"), 
    path('delete_ricetta_bagnato/<int:pk>', delete_ricetta_bagnato, name="delete_ricetta_bagnato"),

    # Dettaglio Ricette Bagnato
    path('<int:fk_ricetta_bagnato>/aggiungi_dettaglio_ricetta_bagnato/', DettaglioRicettaBagnatoCreateView.as_view(), name="aggiungi_dettaglio_ricetta_bagnato"), 
    path('<int:fk_ricetta_bagnato>/modifica_dettaglio_ricetta_bagnato/<int:pk>/', DettaglioRicettaBagnatoUpdateView.as_view(), name="modifica_dettaglio_ricetta_bagnato"), 
    path('delete_dettaglio_ricetta_bagnato/<int:pk>', delete_dettaglio_ricetta_bagnato, name="delete_dettaglio_ricetta_bagnato"),
    
    
    # Stampa ricette
    path('ricetta_rifinizione_print/<int:pk>', ricetta_rifinizione_print, name="ricetta_rifinizione_print"),
    path('ricetta_bagnato_print/<int:pk>', ricetta_bagnato_print, name="ricetta_bagnato_print"),
    
    
    # Automatismi
    path('accoda_dettaglio_ricetta_rifinizione/', accoda_dettaglio_ricetta_rifinizione, name="accoda_dettaglio_ricetta_rifinizione"),
    path('accoda_dettaglio_ricetta_colore_rifinizione/', accoda_dettaglio_ricetta_colore_rifinizione, name="accoda_dettaglio_ricetta_colore_rifinizione"),

    path('accoda_dettaglio_ricetta_bagnato/', accoda_dettaglio_ricetta_bagnato, name="accoda_dettaglio_ricetta_bagnato"),
    
    
]
    
    
