from core.views import dashboard
from django.urls import path

from .searches import *
from .utils import (update_numero_riga_down, update_numero_riga_up,
                    update_row_numbers)

app_name="core"

urlpatterns = [
    
    path('dashboard/', dashboard, name='dashboard'),    
      
    path('update_numero_riga_down/', update_numero_riga_down, name='update_numero_riga_down'),    
    path('update_numero_riga_up/', update_numero_riga_up, name='update_numero_riga_up'), 
    path('update_row_numbers/<str:app_name>/<str:model_name>/', update_row_numbers, name='update_row_numbers'),



    # Ricerche
    path('search_articolo/', search_articolo, name='search_articolo'),
    path('search_colore/', search_colore, name='search_colore'),
    path('search_revisione_rifinizione/', search_revisione_rifinizione, name='search_revisione_rifinizione'),
    path('search_revisione_colore_rifinizione/', search_revisione_colore_rifinizione, name='search_revisione_colore_rifinizione'),
    path('search_prodotto_chimico_rifinizione/', search_prodotto_chimico_rifinizione, name='search_prodotto_chimico_rifinizione'),
    path('search_ghs_symbol/', search_ghs_symbol, name='search_ghs_symbol'),
    path('search_hazard_statement/', search_hazard_statement, name='search_hazard_statement'),
    path('search_precautionary_statement/', search_precautionary_statement, name='search_precautionary_statement'),

    path('search_revisione_bagnato/', search_revisione_bagnato, name="search_revisione_bagnato"), # Ricette Bagnato

       
     
]