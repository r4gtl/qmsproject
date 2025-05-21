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
]