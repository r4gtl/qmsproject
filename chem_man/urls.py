from django.urls import path

from .views import (home_prodotti_chimici, tabelle_generiche,
                    ProdottoChimicoCreateView, ProdottoChimicoUpdateView, delete_prodotto_chimico,
                    PrezzoProdottoCreateView, PrezzoProdottoUpdateView, delete_prezzo_prodotto_chimico,
                    SchedaTecnicaCreateView, SchedaTecnicaUpdateView, delete_scheda_tecnica,
                    SostanzaCreateView, SostanzaUpdateView, delete_sostanza,
                    SostanzaSVHCCreateView, SostanzaSVHCUpdateView, delete_sostanza_svhc,
                    HazardStatementCreateView, HazardStatementUpdateView, delete_hazard_statement,
                    PrecautionaryStatementCreateView, PrecautionaryStatementUpdateView, delete_precautionary_statement,
                    
                    )




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
    
    
]