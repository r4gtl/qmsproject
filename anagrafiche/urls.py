from django.urls import path
from .views import home_fornitori, aggiungi_fornitore, CreateSupplier, vedi_fornitore, ListaFornitoriView

app_name="anagrafiche"



urlpatterns = [
    # path("home_fornitori/", home_fornitori, name="home_fornitori"),
    path("home_fornitori/", ListaFornitoriView.as_view(), name="home_fornitori"),
    # path("aggiungi_fornitore/", aggiungi_fornitore, name="aggiungi_fornitore"),
    path("aggiungi_fornitore/", CreateSupplier.as_view(), name="aggiungi_fornitore"),
    path("vedi_fornitore/<int:pk>", vedi_fornitore, name="vedi_fornitore"),
    
]