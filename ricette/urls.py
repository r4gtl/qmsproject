from django.urls import path

from .provareports import *
from .reports import *
from .utils import *
from .views import *

app_name = "ricette"

urlpatterns = [
    # Home Ricette
    path("", home_ricette, name="home_ricette"),
    path(
        "ricette_rifinizione/",
        home_ricette_rifinizione,
        name="home_ricette_rifinizione",
    ),
    path("ricette_bagnato/", home_ricette_bagnato, name="home_ricette_bagnato"),
    path(
        "ricette_colori_rifinizione/",
        home_ricette_colori_rifinizione,
        name="home_ricette_colori_rifinizione",
    ),
    path(
        "ricette_colori_bagnato/",
        home_ricette_colori_bagnato,
        name="home_ricette_colori_bagnato",
    ),
    # Tabelle Generiche
    path("tabelle_generiche/", tabelle_generiche, name="tabelle_generiche"),
    # Operazione Ricette
    path(
        "aggiungi_operazione/",
        OperazioneRicetteCreateView.as_view(),
        name="aggiungi_operazione",
    ),
    path(
        "modifica_operazione/<int:pk>/",
        OperazioneRicetteUpdateView.as_view(),
        name="modifica_operazione",
    ),
    path("delete_operazione/<int:pk>", delete_operazione, name="delete_operazione"),
    # Ricette Rifinizione
    path(
        "aggiungi_ricetta_rifinizione/",
        RicettaRifinizioneCreateView.as_view(),
        name="aggiungi_ricetta_rifinizione",
    ),
    path(
        "modifica_ricetta_rifinizione/<int:pk>/",
        RicettaRifinizioneUpdateView.as_view(),
        name="modifica_ricetta_rifinizione",
    ),
    path(
        "modifica_dettaglio_ricetta_rifinizione_with_focus_button/<int:pk>/<str:focus_button>/",
        RicettaRifinizioneUpdateView.as_view(),
        name="modifica_dettaglio_ricetta_rifinizione_with_focus_button",
    ),
    path(
        "delete_ricetta_rifinizione/<int:pk>",
        delete_ricetta_rifinizione,
        name="delete_ricetta_rifinizione",
    ),
    # Dettaglio Ricette Rifinizione
    path(
        "<int:fk_ricetta_rifinizione>/aggiungi_dettaglio_ricetta_rifinizione/",
        DettaglioRicettaRifinizioneCreateView.as_view(),
        name="aggiungi_dettaglio_ricetta_rifinizione",
    ),
    path(
        "<int:fk_ricetta_rifinizione>/modifica_dettaglio_ricetta_rifinizione/<int:pk>/",
        DettaglioRicettaRifinizioneUpdateView.as_view(),
        name="modifica_dettaglio_ricetta_rifinizione",
    ),
    path(
        "delete_dettaglio_ricetta_rifinizione/<int:pk>",
        delete_dettaglio_ricetta_rifinizione,
        name="delete_dettaglio_ricetta_rifinizione",
    ),
    # Ricette Colore Rifinizione
    path(
        "aggiungi_ricetta_colore_rifinizione/",
        RicettaColoreRifinizioneCreateView.as_view(),
        name="aggiungi_ricetta_colore_rifinizione",
    ),
    path(
        "modifica_ricetta_colore_rifinizione/<int:pk>/",
        RicettaColoreRifinizioneUpdateView.as_view(),
        name="modifica_ricetta_colore_rifinizione",
    ),
    path(
        "modifica_ricetta_colore_rifinizione_with_focus_button/<int:pk>/<str:focus_button>/",
        RicettaColoreRifinizioneUpdateView.as_view(),
        name="modifica_ricetta_colore_rifinizione_with_focus_button",
    ),
    path(
        "delete_ricetta_colore_rifinizione/<int:pk>",
        delete_ricetta_colore_rifinizione,
        name="delete_ricetta_colore_rifinizione",
    ),
    # Dettaglio Ricette Colore Rifinizione
    path(
        "<int:fk_ricetta_colore_rifinizione>/aggiungi_dettaglio_ricetta_colore_rifinizione/",
        DettaglioRicettaColoreRifinizioneCreateView.as_view(),
        name="aggiungi_dettaglio_ricetta_colore_rifinizione",
    ),
    path(
        "<int:fk_ricetta_colore_rifinizione>/modifica_dettaglio_ricetta_colore_rifinizione/<int:pk>/",
        DettaglioRicettaColoreRifinizioneUpdateView.as_view(),
        name="modifica_dettaglio_ricetta_colore_rifinizione",
    ),
    path(
        "delete_dettaglio_ricetta_colore_rifinizione/<int:pk>",
        delete_dettaglio_ricetta_colore_rifinizione,
        name="delete_dettaglio_ricetta_colore_rifinizione",
    ),
    # Ricette bagnato
    path(
        "aggiungi_ricetta_bagnato/",
        RicettaBagnatoCreateView.as_view(),
        name="aggiungi_ricetta_bagnato",
    ),
    path(
        "modifica_ricetta_bagnato/<int:pk>/",
        RicettaBagnatoUpdateView.as_view(),
        name="modifica_ricetta_bagnato",
    ),
    path(
        "delete_ricetta_bagnato/<int:pk>",
        delete_ricetta_bagnato,
        name="delete_ricetta_bagnato",
    ),
    # Dettaglio Ricette Bagnato
    path(
        "<int:fk_ricetta_bagnato>/aggiungi_dettaglio_ricetta_bagnato/",
        DettaglioRicettaBagnatoCreateView.as_view(),
        name="aggiungi_dettaglio_ricetta_bagnato",
    ),
    path(
        "<int:fk_ricetta_bagnato>/modifica_dettaglio_ricetta_bagnato/<int:pk>/",
        DettaglioRicettaBagnatoUpdateView.as_view(),
        name="modifica_dettaglio_ricetta_bagnato",
    ),
    path(
        "delete_dettaglio_ricetta_bagnato/<int:pk>",
        delete_dettaglio_ricetta_bagnato,
        name="delete_dettaglio_ricetta_bagnato",
    ),
    # Ricette Colore Bagnato
    path(
        "aggiungi_ricetta_colore_bagnato/",
        RicettaColoreBagnatoCreateView.as_view(),
        name="aggiungi_ricetta_colore_bagnato",
    ),
    path(
        "modifica_ricetta_colore_bagnato/<int:pk>/",
        RicettaColoreBagnatoUpdateView.as_view(),
        name="modifica_ricetta_colore_bagnato",
    ),
    path(
        "modifica_ricetta_colore_bagnato_with_focus_button/<int:pk>/<str:focus_button>/",
        RicettaColoreBagnatoUpdateView.as_view(),
        name="modifica_ricetta_colore_bagnato_with_focus_button",
    ),
    path(
        "delete_ricetta_colore_bagnato/<int:pk>",
        delete_ricetta_colore_bagnato,
        name="delete_ricetta_colore_bagnato",
    ),
    # Dettaglio Ricette Colore Bagnato
    path(
        "<int:fk_ricetta_colore_bagnato>/aggiungi_dettaglio_ricetta_colore_bagnato/",
        DettaglioRicettaColoreBagnatoCreateView.as_view(),
        name="aggiungi_dettaglio_ricetta_colore_bagnato",
    ),
    path(
        "<int:fk_ricetta_colore_bagnato>/modifica_dettaglio_ricetta_colore_bagnato/<int:pk>/",
        DettaglioRicettaColoreBagnatoUpdateView.as_view(),
        name="modifica_dettaglio_ricetta_colore_bagnato",
    ),
    path(
        "delete_dettaglio_ricetta_colore_bagnato/<int:pk>",
        delete_dettaglio_ricetta_colore_bagnato,
        name="delete_dettaglio_ricetta_colore_bagnato",
    ),
    # XRFondoColore
    path(
        "<int:numero_ricetta>/aggiungi_xr_fondo_colore/",
        XRFondoColoreCreateView.as_view(),
        name="aggiungi_xr_fondo_colore",
    ),
    path(
        "<int:numero_ricetta>/modifica_xr_fondo_colore/<int:pk>/",
        XRFondoColoreUpdateView.as_view(),
        name="modifica_xr_fondo_colore",
    ),
    path(
        "delete_xr_fondo_colore/<int:pk>",
        delete_xr_fondo_colore,
        name="delete_xr_fondo_colore",
    ),
    # Stampa ricette
    path(
        "ricetta_rifinizione_print/<int:pk>",
        ricetta_rifinizione_print,
        name="ricetta_rifinizione_print",
    ),
    path(
        "ricetta_colore_rifinizione_print/<int:pk>",
        ricetta_colore_rifinizione_print,
        name="ricetta_colore_rifinizione_print",
    ),
    path(
        "ricetta_bagnato_print/<int:pk>",
        ricetta_bagnato_print,
        name="ricetta_bagnato_print",
    ),
    path(
        "ricetta_colore_bagnato_print/<int:pk>",
        ricetta_colore_bagnato_print,
        name="ricetta_colore_bagnato_print",
    ),
    # Automatismi
    path(
        "accoda_dettaglio_ricetta_rifinizione/",
        accoda_dettaglio_ricetta_rifinizione,
        name="accoda_dettaglio_ricetta_rifinizione",
    ),
    path(
        "accoda_dettaglio_ricetta_colore_rifinizione/",
        accoda_dettaglio_ricetta_colore_rifinizione,
        name="accoda_dettaglio_ricetta_colore_rifinizione",
    ),
    path(
        "accoda_dettaglio_ricetta_bagnato/",
        accoda_dettaglio_ricetta_bagnato,
        name="accoda_dettaglio_ricetta_bagnato",
    ),
    path(
        "accoda_dettaglio_ricetta_colore_bagnato/",
        accoda_dettaglio_ricetta_colore_bagnato,
        name="accoda_dettaglio_ricetta_colore_bagnato",
    ),

    path(
        "stampa_jasper/<pk>/",
        ricetta_rifinizione_jasper,
        name="stampa_jasper",
    ),
]
