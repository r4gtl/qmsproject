from django.urls import path
from .views import (home_fornitori,
                    # aggiungi_fornitore,
                    CreateSupplier,                    
                    # vedi_fornitore,
                    ListaFornitoriView,
                    FacilityCreateView,
                    aggiungi_facility_details,
                    # edit_facility_details,
                    FacilityUpdateView,
                    delete_facility_contact,
                    add_facility_contact,
                    FacilityContactUpdateView,
                    UpdateSupplier,
                    AddLwgCertificate,
                    UpdateLwgCertificate,                    
                    delete_certificato,
                    XrTransferValueCreateView,
                    XrTransferValueUpdateView,
                    XrTransferValueDeleteView,
                    TransferValueListView,
                    TransferValueCreateView,
                    TransferValueUpdateView,
                    ClienteCreateView, ClienteListView, ClienteUpdateView, ListaClienteView
                    )
from .charts import get_country_count, get_country_count_client


app_name="anagrafiche"



urlpatterns = [

    # Facility
    path("aggiungi_facility_details/", FacilityCreateView.as_view(), name="aggiungi_facility_details"),    
    path("edit_facility_details/<int:pk>", FacilityUpdateView.as_view(), name="edit_facility_details"),
    path("<int:pk>/add_facility_contact", add_facility_contact, name="add_facility_contact"),
    path("<int:pk>/modifica_facility_contact/<int:id>", FacilityContactUpdateView.as_view(), name="modifica_facility_contact"),
    path("delete_facility_contact/<int:pk>", delete_facility_contact, name="delete_facility_contact"),

    # Clienti
    path("home_clienti/", ListaClienteView.as_view(), name="home_clienti"),
    path("aggiungi_cliente/", ClienteCreateView.as_view(), name="aggiungi_cliente"),
    path("modifica_cliente/<int:pk>", ClienteUpdateView.as_view(), name="modifica_cliente"),
    
    # Fornitori
    path("home_fornitori/", home_fornitori, name="home_fornitori"),    
    path("aggiungi_fornitore/", CreateSupplier.as_view(), name="aggiungi_fornitore"),    
    path("vedi_fornitore/<int:pk>", UpdateSupplier.as_view(), name="vedi_fornitore"),
    path("fornitore/<int:fk_fornitore>/aggiungi_lwg/", AddLwgCertificate.as_view(), name="aggiungi_lwg"),
    path("modifica_lwg/<int:pk>", UpdateLwgCertificate.as_view(), name="modifica_lwg"),    
    path("delete_lwg/<int:pk>", delete_certificato, name="delete_lwg"),
    path("modifica_lwg/<int:pk>/add_transf_value/", XrTransferValueCreateView.as_view(), name="add_transf_value"),
    path("edit_transf_value/<int:id>", XrTransferValueUpdateView.as_view(), name="edit_transf_value"),
    path("delete_transf_value/<int:id>", XrTransferValueDeleteView.as_view(), name="delete_transf_value"),

    # Generiche - Transfer Values
    path("transfer_values_list/", TransferValueListView.as_view(), name="transfer_values_list"),
    path("add_transfer_values/", TransferValueCreateView.as_view(), name="add_transfer_values"),
    path("edit_transfer_values/<int:pk>", TransferValueUpdateView.as_view(), name="edit_transfer_values"),

    # Charts
    path('get_country_count/', get_country_count, name='get_country_count'),
    path('get_country_count_client/', get_country_count_client, name='get_country_count_client'),
    

    
]