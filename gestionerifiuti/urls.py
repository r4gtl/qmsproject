from django.urls import path
from .views import (gestione_rifiuti_home, tabelle_generiche,
                    MovimentoRifiutiCreateView, MovimentoRifiutiUpdateView, delete_movimento_rifiuti,
                    CodiceCERCreateView, CodiceCERUpdateView, delete_codice_cer,
                    CodiceSmaltRecCreateView, CodiceSmaltRecUpdateView, delete_codice_smaltrec,
                    performance_triennio,
                    
)

from .utils import get_descrizione_cer, get_descrizione_smaltrec

from .charts import cer_last_year


app_name="gestionerifiuti"



urlpatterns = [

    # Home
    path("", gestione_rifiuti_home, name="gestione_rifiuti_home"), 
    
    # Tabelle generiche
    path('tabelle_generiche/', tabelle_generiche, name="tabelle_generiche"),
    
    # Manage Movimenti
    path('crea_movimento_rifiuti/', MovimentoRifiutiCreateView.as_view(), name="crea_movimento_rifiuti"), 
    path('modifica_movimento_rifiuti/<int:pk>/', MovimentoRifiutiUpdateView.as_view(), name="modifica_movimento_rifiuti"), 
    path('delete_movimento_rifiuti/<int:pk>', delete_movimento_rifiuti, name="delete_movimento_rifiuti"),
    
    # Manage Codici CER
    path('crea_codice_cer/', CodiceCERCreateView.as_view(), name="crea_codice_cer"), 
    path('modifica_codice_cer/<int:pk>/', CodiceCERUpdateView.as_view(), name="modifica_codice_cer"), 
    path('delete_codice_cer/<int:pk>', delete_codice_cer, name="delete_codice_cer"),
    
    # Manage Codici Smalt/Rec
    path('crea_codice_smaltrec/', CodiceSmaltRecCreateView.as_view(), name="crea_codice_smaltrec"), 
    path('modifica_codice_smaltrec/<int:pk>/', CodiceSmaltRecUpdateView.as_view(), name="modifica_codice_smaltrec"), 
    path('delete_codice_smaltrec/<int:pk>', delete_codice_smaltrec, name="delete_codice_smaltrec"),
            
    # Utils
    path('get_descrizione_cer/', get_descrizione_cer, name='get_descrizione_cer'),
    path('get_descrizione_smaltrec/', get_descrizione_smaltrec, name='get_descrizione_smaltrec'),

    # Charts
    path('cer_last_year/', cer_last_year, name='cer_last_year'),
    
    # Stampe
    path('performance_triennio/', performance_triennio, name='performance_triennio'),

    
]