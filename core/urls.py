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

       
     
]