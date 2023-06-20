from django.urls import path
from .views import (autorizzazioni_home, 
                    AutorizzazioneCreateView, AutorizzazioneUpdateView, delete_autorizzazione,
                    DettaglioScadenzaAutorizzazioneCreateView, DettaglioScadenzaAutorizzazioneUpdateView, delete_dettaglio_autorizzazione,
                    stampa_registro_autorizzazioni,
                    
                    )

app_name="autorizzazioni"

urlpatterns = [
    
    # Home Autorizzazioni
    path('', autorizzazioni_home, name='autorizzazioni_home'),    

    # Manage Autorizzazioni
    path('crea_autorizzazione/', AutorizzazioneCreateView.as_view(), name="crea_autorizzazione"), 
    path('modifica_autorizzazione/<int:pk>/', AutorizzazioneUpdateView.as_view(), name="modifica_autorizzazione"), 
    path('delete_autorizzazione/<int:pk>', delete_autorizzazione, name="delete_autorizzazione"),

    # Manage Rinnovi
    path('<int:fk_autorizzazione>/aggiungi_dettaglio_autorizzazione/', DettaglioScadenzaAutorizzazioneCreateView.as_view(), name="aggiungi_dettaglio_autorizzazione"), 
    path('<int:fk_autorizzazione>/modifica_dettaglio_autorizzazione/<int:pk>/', DettaglioScadenzaAutorizzazioneUpdateView.as_view(), name="modifica_dettaglio_autorizzazione"), 
    path('delete_dettaglio_autorizzazione/<int:pk>', delete_dettaglio_autorizzazione, name="delete_dettaglio_autorizzazione"),

    # Stampe
    path('stampa_registro_autorizzazioni/', stampa_registro_autorizzazioni, name="stampa_registro_autorizzazioni"), 
]