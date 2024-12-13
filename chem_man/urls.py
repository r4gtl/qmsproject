from django.urls import path

from .utils import (check_if_svhc, get_imballaggi, get_prodotto_chimico,
                    get_solvente, get_sostanza_details, get_symbol_image_url,
                    get_ultimo_prezzo, search_sostanza)
from .views import *

#from .views import *



app_name = 'chem_man'

urlpatterns = [
    
    # Home Prodotti Chimici
    path('', home_prodotti_chimici, name="home_prodotti_chimici"),
    
    # Prodotti Chimici
    path('aggiungi_prodotto_chimico/', ProdottoChimicoCreateView.as_view(), name="aggiungi_prodotto_chimico"), 
    path('modifica_prodotto_chimico/<int:pk>/', ProdottoChimicoUpdateView.as_view(), name="modifica_prodotto_chimico"), 
    path('modifica_prodotto_chimico_with_focus_button/<int:pk>/<str:focus_button>/', ProdottoChimicoUpdateView.as_view(), name="modifica_prodotto_chimico_with_focus_button"), 
    path('delete_prodotto_chimico/<int:pk>', delete_prodotto_chimico, name="delete_prodotto_chimico"),
    
    # Prezzi Prodotti Chimici
    path('<int:fk_prodottochimico>/aggiungi_prezzo_prodotto_chimico/', PrezzoProdottoCreateView.as_view(), name="aggiungi_prezzo_prodotto_chimico"), 
    path('<int:fk_prodottochimico>/modifica_prezzo_prodotto_chimico/<int:pk>/', PrezzoProdottoUpdateView.as_view(), name="modifica_prezzo_prodotto_chimico"), 
    path('delete_prezzo_prodotto_chimico/<int:pk>', delete_prezzo_prodotto_chimico, name="delete_prezzo_prodotto_chimico"),
    
    # Schede Tecniche
    path('<int:fk_prodottochimico>/aggiungi_scheda_tecnica/', SchedaTecnicaCreateView.as_view(), name="aggiungi_scheda_tecnica"), 
    path('<int:fk_prodottochimico>/modifica_scheda_tecnica/<int:pk>/', SchedaTecnicaUpdateView.as_view(), name="modifica_scheda_tecnica"), 
    path('delete_scheda_tecnica/<int:pk>', delete_scheda_tecnica, name="delete_scheda_tecnica"),
    
    # Tabelle Generiche
    path('tabelle_generiche/', tabelle_generiche, name="tabelle_generiche"),
    
    # Sostanza
    path('aggiungi_sostanza/', SostanzaCreateView.as_view(), name="aggiungi_sostanza"), 
    path('modifica_sostanza/<int:pk>/', SostanzaUpdateView.as_view(), name="modifica_sostanza"), 
    path('delete_sostanza/<int:pk>', delete_sostanza, name="delete_sostanza"),
    
    # Sostanza SVHC
    path('aggiungi_sostanza_svhc/', SostanzaSVHCCreateView.as_view(), name="aggiungi_sostanza_svhc"), 
    path('modifica_sostanza_svhc/<int:pk>/', SostanzaSVHCUpdateView.as_view(), name="modifica_sostanza_svhc"), 
    path('delete_sostanza_svhc/<int:pk>', delete_sostanza_svhc, name="delete_sostanza_svhc"),
    
    # Hazard Statement
    path('aggiungi_hazard_statement/', HazardStatementCreateView.as_view(), name="aggiungi_hazard_statement"), 
    path('modifica_hazard_statement/<int:pk>/', HazardStatementUpdateView.as_view(), name="modifica_hazard_statement"), 
    path('delete_hazard_statement/<int:pk>', delete_hazard_statement, name="delete_hazard_statement"),
    
    # Precautionary Statement
    path('aggiungi_precautionary_statement/', PrecautionaryStatementCreateView.as_view(), name="aggiungi_precautionary_statement"), 
    path('modifica_precautionary_statement/<int:pk>/', PrecautionaryStatementUpdateView.as_view(), name="modifica_precautionary_statement"), 
    path('delete_precautionary_statement/<int:pk>', delete_precautionary_statement, name="delete_precautionary_statement"),

    # Simboli GHS
    path('aggiungi_simbolo_ghs/', SimboloGHSCreateView.as_view(), name="aggiungi_simbolo_ghs"), 
    path('modifica_simbolo_ghs/<int:pk>/', SimboloGHSUpdateView.as_view(), name="modifica_simbolo_ghs"), 
    path('delete_simbolo_ghs/<int:pk>', delete_simbolo_ghs, name="delete_simbolo_ghs"),

    # Imballaggi PC
    path('aggiungi_imballaggio_pc/', ImballaggioPCCreateView.as_view(), name="aggiungi_imballaggio_pc"), 
    path('modifica_imballaggio_pc/<int:pk>/', ImballaggioPCUpdateView.as_view(), name="modifica_imballaggio_pc"), 
    path('delete_imballaggio_pc/<int:pk>', delete_imballaggio_pc, name="delete_imballaggio_pc"),
    
    # Schede Sicurezza
    path('<int:fk_prodottochimico>/aggiungi_scheda_sicurezza/', SchedaSicurezzaCreateView.as_view(), name="aggiungi_scheda_sicurezza"), 
    path('<int:fk_prodottochimico>/modifica_scheda_sicurezza/<int:pk>/', SchedaSicurezzaUpdateView.as_view(), name="modifica_scheda_sicurezza"), 
    path('<int:fk_prodottochimico>/modifica_scheda_sicurezza_with_focus_button/<int:pk>/<str:focus_button>/', SchedaSicurezzaUpdateView.as_view(), name='modifica_scheda_sicurezza_with_focus_button'),
    path('delete_scheda_sicurezza/<int:pk>', delete_scheda_sicurezza, name="delete_scheda_sicurezza"),
    
    # Simbolo_ghs_sds
    path('<int:fk_sds>/aggiungi_simbolo_ghs_sds/', SimboloGHS_SDSCreateView.as_view(), name="aggiungi_simbolo_ghs_sds"), 
    path('<int:fk_sds>/modifica_simbolo_ghs_sds/<int:pk>/', SimboloGHS_SDSUpdateView.as_view(), name="modifica_simbolo_ghs_sds"), 
    path('delete_simbolo_ghs_sds/<int:pk>', delete_simbolo_ghs_sds, name="delete_simbolo_ghs_sds"),

    # Hazard statement_sds
    path('<int:fk_sds>/aggiungi_hazard_statement_sds/', HazardStatement_SDSCreateView.as_view(), name="aggiungi_hazard_statement_sds"), 
    path('<int:fk_sds>/modifica_hazard_statement_sds/<int:pk>/', HazardStatement_SDSUpdateView.as_view(), name="modifica_hazard_statement_sds"), 
    path('delete_hazard_statement_sds/<int:pk>', delete_hazard_statement_sds, name="delete_hazard_statement_sds"),

    # Precautionary statement_sds
    path('<int:fk_sds>/aggiungi_precautionary_statement_sds/', PrecautionaryStatement_SDSCreateView.as_view(), name="aggiungi_precautionary_statement_sds"), 
    path('<int:fk_sds>/modifica_precautionary_statement_sds/<int:pk>/', PrecautionaryStatement_SDSUpdateView.as_view(), name="modifica_precautionary_statement_sds"), 
    path('delete_precautionary_statement_sds/<int:pk>', delete_precautionary_statement_sds, name="delete_precautionary_statement_sds"),

    # Sostanza sds
    path('<int:fk_sds>/aggiungi_sostanza_sds/', Sostanza_SDSCreateView.as_view(), name="aggiungi_sostanza_sds"), 
    path('<int:fk_sds>/modifica_sostanza_sds/<int:pk>/', Sostanza_SDSUpdateView.as_view(), name="modifica_sostanza_sds"), 
    path('delete_sostanza_sds/<int:pk>', delete_sostanza_sds, name="delete_sostanza_sds"),

    # Dashboard Acquisti
    path('dashboard_acquisti/', dashboard_acquisti_prodotti_chimici, name="dashboard_acquisti_prodotti_chimici"),

    # Home Ordini
    path('ordini/', home_ordini_prodotti_chimici, name="home_ordini_prodotti_chimici"),
    
    # Home Acquisti
    path('acquisti/', home_acquisti_prodotti_chimici, name="home_acquisti_prodotti_chimici"),
    
    # Acquisti - Ordini
    path('aggiungi_ordine_prodotto_chimico/', OrdineProdottoChimicoCreateView.as_view(), name="aggiungi_ordine_prodotto_chimico"), 
    path('modifica_ordine_prodotto_chimico/<int:pk>/', OrdineProdottoChimicoUpdateView.as_view(), name="modifica_ordine_prodotto_chimico"), 
    path('modifica_ordine_prodotto_chimico_with_focus/<int:pk>/<str:focus_button>/', OrdineProdottoChimicoUpdateView.as_view(), name="modifica_ordine_prodotto_chimico_with_focus"), 
    path('delete_ordine_prodotto_chimico/<int:pk>', delete_ordine_prodotto_chimico, name="delete_ordine_prodotto_chimico"),
    
    # Dettaglio Ordini
    path('<int:fk_ordine>/aggiungi_dettaglio_ordine_prodotto_chimico/', DettaglioOrdineProdottoChimicoCreateView.as_view(), name="aggiungi_dettaglio_ordine_prodotto_chimico"), 
    path('<int:fk_ordine>/modifica_dettaglio_ordine_prodotto_chimico/<int:pk>/', DettaglioOrdineProdottoChimicoUpdateView.as_view(), name="modifica_dettaglio_ordine_prodotto_chimico"), 
    path('delete_dettaglio_ordine_prodotto_chimico/<int:pk>', delete_dettaglio_ordine_prodotto_chimico, name="delete_dettaglio_ordine_prodotto_chimico"),

    # Acquisti - Documenti Acquisto
    path('aggiungi_acquisto_prodotto_chimico/', AcquistoProdottoChimicoCreateView.as_view(), name="aggiungi_acquisto_prodotto_chimico"), 
    path('modifica_acquisto_prodotto_chimico/<int:pk>/', AcquistoProdottoChimicoUpdateView.as_view(), name="modifica_acquisto_prodotto_chimico"), 
    path('delete_acquisto_prodotto_chimico/<int:pk>', delete_acquisto_prodotto_chimico, name="delete_acquisto_prodotto_chimico"),
    
    # Dettaglio Acquisto
    path('<int:fk_acquisto>/aggiungi_dettaglio_acquisto_prodotto_chimico/', DettaglioAcquistoProdottoChimicoCreateView.as_view(), name="aggiungi_dettaglio_acquisto_prodotto_chimico"), 
    path('<int:fk_acquisto>/modifica_dettaglio_acquisto_prodotto_chimico/<int:pk>/', DettaglioAcquistoProdottoChimicoUpdateView.as_view(), name="modifica_dettaglio_acquisto_prodotto_chimico"), 
    path('delete_dettaglio_acquisto_prodotto_chimico/<int:pk>', delete_dettaglio_acquisto_prodotto_chimico, name="delete_dettaglio_acquisto_prodotto_chimico"),
        
    # Utilities
    # il primo serve per ottenere l'immagine del simbolo di pericolo o comunque cambiando la selezione in un campo options
    path('get_symbol_image_url/', get_symbol_image_url, name="get_symbol_image_url"),
    path('search_sostanza/', search_sostanza, name="search_sostanza"),
    path('get_sostanza_details/', get_sostanza_details, name="get_sostanza_details"),
    path('check_if_svhc/', check_if_svhc, name='check_if_svhc'),
    path('get_prodotto_chimico/', get_prodotto_chimico, name='get_prodotto_chimico'),
    path('get_ultimo_prezzo/', get_ultimo_prezzo, name='get_ultimo_prezzo'),
    path('get_solvente/', get_solvente, name='get_solvente'),
    path('get_imballaggi/', get_imballaggi, name='get_imballaggi'),

    # Stampe
    path('stampa_ordine/<int:pk>/', stampa_ordine, name='stampa_ordine'),
    path('ordine/<int:ordine_id>/report/', generate_order_report, name='ordine_report'),
    
    # Controllo dettaglio ordine    
    path('controlla_dettagli_ordine/<int:pk>/', controlla_dettagli_ordine, name='controlla_dettagli_ordine'),

    

    
]