from django.urls import path

from .views import (home_prodotti_chimici,
                    ProdottoChimicoCreateView, ProdottoChimicoUpdateView, delete_prodotto_chimico,
                    PrezzoProdottoCreateView, PrezzoProdottoUpdateView, delete_prezzo_prodotto_chimico,
                    SchedaTecnicaCreateView, SchedaTecnicaUpdateView, delete_scheda_tecnica,
                    
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
    
    
]