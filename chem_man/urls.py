from django.urls import path



from .views import (home_prodotti_chimici, tabelle_generiche,
                    ProdottoChimicoCreateView, ProdottoChimicoUpdateView, delete_prodotto_chimico,
                    PrezzoProdottoCreateView, PrezzoProdottoUpdateView, delete_prezzo_prodotto_chimico,
                    SchedaTecnicaCreateView, SchedaTecnicaUpdateView, delete_scheda_tecnica,
                    SostanzaCreateView, SostanzaUpdateView, delete_sostanza,
                    SostanzaSVHCCreateView, SostanzaSVHCUpdateView, delete_sostanza_svhc,
                    HazardStatementCreateView, HazardStatementUpdateView, delete_hazard_statement,
                    PrecautionaryStatementCreateView, PrecautionaryStatementUpdateView, delete_precautionary_statement,
                    SimboloGHSCreateView, SimboloGHSUpdateView, delete_simbolo_ghs,
                    SchedaSicurezzaCreateView, SchedaSicurezzaUpdateView, delete_scheda_sicurezza,
                    SimboloGHS_SDSCreateView, SimboloGHS_SDSUpdateView, delete_simbolo_ghs_sds,
                    HazardStatement_SDSCreateView, HazardStatement_SDSUpdateView, delete_hazard_statement_sds,
                    PrecautionaryStatement_SDSCreateView, PrecautionaryStatement_SDSUpdateView, delete_precautionary_statement_sds,
                    Sostanza_SDSCreateView, Sostanza_SDSUpdateView, delete_sostanza_sds,
                    
                    )

from .utils import get_symbol_image_url, search_sostanza


app_name = 'chem_man'

urlpatterns = [
    
    # Home Prodotti Chimici
    path('', home_prodotti_chimici, name="home_prodotti_chimici"),
    
    # Prodotti Chimici
    path('aggiungi_prodotto_chimico/', ProdottoChimicoCreateView.as_view(), name="aggiungi_prodotto_chimico"), 
    path('modifica_prodotto_chimico/<int:pk>/', ProdottoChimicoUpdateView.as_view(), name="modifica_prodotto_chimico"), 
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
    
    # Schede Sicurezza
    path('<int:fk_prodottochimico>/aggiungi_scheda_sicurezza/', SchedaSicurezzaCreateView.as_view(), name="aggiungi_scheda_sicurezza"), 
    path('<int:fk_prodottochimico>/modifica_scheda_sicurezza/<int:pk>/', SchedaSicurezzaUpdateView.as_view(), name="modifica_scheda_sicurezza"), 
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

    # Utilities
    # il primo serve per ottenere l'immagine del simbolo di pericolo o comunque cambiando la selezione in un campo options
    path('get_symbol_image_url/', get_symbol_image_url, name="get_symbol_image_url"),
    path('search_sostanza/', search_sostanza, name="search_sostanza"),
    

    
]