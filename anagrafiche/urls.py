from django.urls import path
from .views import (home_fornitori,
                    # aggiungi_fornitore,
                    CreateSupplier,
                    # vedi_fornitore,
                    ListaFornitoriView,
                    FacilityCreateView,
                    aggiungi_facility_details,
                    edit_facility_details,
                    FacilityUpdateView,
                    add_facility_contact,
                    UpdateSupplier,
                    AddLwgCertificate,
                    UpdateLwgCertificate,
                    AddXrTranferValue

                    )

app_name="anagrafiche"



urlpatterns = [
    # path("home_fornitori/", home_fornitori, name="home_fornitori"),
    path("home_fornitori/", ListaFornitoriView.as_view(), name="home_fornitori"),
    #path("aggiungi_fornitore/", aggiungi_fornitore, name="aggiungi_fornitore"),
    path("aggiungi_fornitore/", CreateSupplier.as_view(), name="aggiungi_fornitore"),
    # path("vedi_fornitore/<int:pk>", vedi_fornitore, name="vedi_fornitore"),
    path("vedi_fornitore/<int:pk>", UpdateSupplier.as_view(), name="vedi_fornitore"),
    path("fornitore/<int:fk_fornitore>/aggiungi_lwg/", AddLwgCertificate.as_view(), name="aggiungi_lwg"),
    path("modifica_lwg/<int:pk>", UpdateLwgCertificate.as_view(), name="modifica_lwg"),
    path("modifica_lwg/<int:pk>/add_transf_value/", AddXrTranferValue.as_view(), name="add_transf_value"),
    #path("aggiungi_facility_details/", aggiungi_facility_details, name="aggiungi_facility_details"),
    path("aggiungi_facility_details/", FacilityCreateView.as_view(), name="aggiungi_facility_details"),
    #path("edit_facility_details/<int:pk>", FacilityUpdateView.as_view(), name="edit_facility_details"),
    path("edit_facility_details/<int:pk>", edit_facility_details, name="edit_facility_details"),
    path("<int:pk>/add_facility_contact", add_facility_contact, name="add_facility_contact"),
    
]