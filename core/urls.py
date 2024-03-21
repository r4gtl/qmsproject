from core.views import dashboard
from django.urls import path

from .dash_charts import *
from .searches import *
from .utils import update_row_numbers

app_name="core"

urlpatterns = [
    
    path('dashboard/', dashboard, name='dashboard'),    
      
    
    path('update_row_numbers/<str:app_name>/<str:model_name>/', update_row_numbers, name='update_row_numbers'),



    # Ricerche
    path('search_articolo/', search_articolo, name='search_articolo'),
    path('search_colore/', search_colore, name='search_colore'),
    path('search_revisione_rifinizione/', search_revisione_rifinizione, name='search_revisione_rifinizione'),
    path('search_revisione_colore_rifinizione/', search_revisione_colore_rifinizione, name='search_revisione_colore_rifinizione'),
    path('search_prodotto_chimico/', search_prodotto_chimico, name='search_prodotto_chimico'),
    path('search_ghs_symbol/', search_ghs_symbol, name='search_ghs_symbol'),
    path('search_hazard_statement/', search_hazard_statement, name='search_hazard_statement'),
    path('search_precautionary_statement/', search_precautionary_statement, name='search_precautionary_statement'),
    path('search_chem_supplier/', search_chem_supplier, name='search_chem_supplier'),
    path('search_supplier/', search_supplier, name='search_supplier'),
    path('search_outsourcing/', search_outsourcing, name='search_outsourcing'),

    path('search_revisione_bagnato/', search_revisione_bagnato, name="search_revisione_bagnato"), # Ricette Bagnato


    path('search_fase_lavoro/', search_fase_lavoro, name="search_fase_lavoro"), # Fase lavoro
    
    
    #Grafici dashboard
    path('produzione_intervallo_date/', produzione_intervallo_date, name="produzione_intervallo_date"),

       
     
]