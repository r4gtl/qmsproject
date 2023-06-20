from django.urls import path
from .views import (autorizzazioni_home, 
                    AutorizzazioneCreateView, AutorizzazioneUpdateView, delete_autorizzazione,
                    DettaglioScadenzaAutorizzazioneCreateView, DettaglioScadenzaAutorizzazioneUpdateView, delete_dettaglio_autorizzazione,
                    ParametroAutorizzazioneCreateView, ParametroAutorizzazioneUpdateView, delete_parametro,
                    CampoApplicazioneCreateView, CampoApplicazioneUpdateView, delete_campo_applicazione,
                    tabelle_generiche_autorizzazioni,
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

    # Tabelle generiche
    path('tabelle_generiche_autorizzazioni/', tabelle_generiche_autorizzazioni, name="tabelle_generiche_autorizzazioni"),

    # Manage Parametri
    path('crea_parametro/', ParametroAutorizzazioneCreateView.as_view(), name="crea_parametro"), 
    path('modifica_parametro/<int:pk>/', ParametroAutorizzazioneUpdateView.as_view(), name="modifica_parametro"), 
    path('delete_parametro/<int:pk>', delete_parametro, name="delete_parametro"),

    # Manage Campi Applicazione
    path('crea_campo_applicazione/', CampoApplicazioneCreateView.as_view(), name="crea_campo_applicazione"), 
    path('modifica_campo_applicazione/<int:pk>/', CampoApplicazioneUpdateView.as_view(), name="modifica_campo_applicazione"), 
    path('delete_campo_applicazione/<int:pk>', delete_campo_applicazione, name="delete_campo_applicazione"),

    # Stampe
    path('stampa_registro_autorizzazioni/', stampa_registro_autorizzazioni, name="stampa_registro_autorizzazioni"), 
]