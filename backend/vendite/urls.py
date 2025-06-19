from django.urls import path

from .views import *

app_name = "vendite"

urlpatterns = [
    # Home Ordini Cliente
    path("", home_ordini_cliente, name="home_ordini_cliente"),
    path("aggiungi_ordine_cliente/", OrdineClienteCreateView.as_view(), name="aggiungi_ordine_cliente"),
    path("modifica_ordine_cliente/<int:pk>/", OrdineClienteUpdateView.as_view(), name="modifica_ordine_cliente"),
    path(
        "modifica_ordine_cliente_with_focus_button/<int:pk>/<str:focus_button>/",
        OrdineClienteUpdateView.as_view(),
        name="modifica_ordine_cliente_with_focus_button",
    ),
    path('delete_ordine_cliente/<int:pk>',
        delete_ordine_cliente,
        name="delete_ordine_cliente"),  

    path("<int:fk_ordine>/aggiungi_dettaglio_ordine/", DettaglioOrdineClienteCreateView.as_view(), name="aggiungi_dettaglio_ordine"),
    path("<int:fk_ordine>/modifica_dettaglio_ordine/<int:pk>", DettaglioOrdineClienteUpdateView.as_view(), name="modifica_dettaglio_ordine"),
    path('delete_dettaglio_ordine_cliente/<int:pk>',
        delete_dettaglio_ordine_cliente,
        name="delete_dettaglio_ordine_cliente"),  
    
    path("schede_lavorazione/", home_schede_lavorazione, name="home_schede_lavorazione"),
    path("aggiungi_scheda_lavorazione/", SchedaLavorazioneCreateView.as_view(), name="aggiungi_scheda_lavorazione"),
    path("modifica_scheda_lavorazione/<int:pk>/", SchedaLavorazioneUpdateView.as_view(), name="modifica_scheda_lavorazione"),
    path(
        "modifica_scheda_lavorazione_with_focus_button/<int:pk>/<str:focus_button>/",
        OrdineClienteUpdateView.as_view(),
        name="modifica_scheda_lavorazione_with_focus_button",
    ),
    path('delete_scheda_lavorazione/<int:pk>',
        delete_scheda_lavorazione,
        name="delete_scheda_lavorazione"),  

    path("<int:fk_schedalavorazione>/aggiungi_dettaglio_scheda/", XRScelteSchedeCreateView.as_view(), name="aggiungi_dettaglio_scheda"),
    path("<int:fk_schedalavorazione>/modifica_dettaglio_scheda/<int:pk>", XRScelteSchedeUpdateView.as_view(), name="modifica_dettaglio_scheda"),
    path('delete_dettaglio_scheda/<int:pk>',
        delete_dettaglio_scheda,
        name="delete_dettaglio_scheda"),  

    path('xrscelte/nuova/', XRScelteSchedeCreateView.as_view(), name="nuova_xrscelta"),
    path('xrscelte/<int:pk>/modifica/', XRScelteSchedeUpdateView.as_view(), name="modifica_xrscelta"),
]