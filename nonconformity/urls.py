from django.urls import path
from .views import (home_rapporti_nc,
                    RapportoNCCreateView, RapportoNCUpdateView, delete_rapporto_nc,
                    RapportoAuditCreateView, RapportoAuditUpdateView, delete_rapporto_audit,
                    
                    )



app_name="nonconformity"

urlpatterns = [
    # Home Rapporti NC
    path('', home_rapporti_nc, name='home_rapporti_nc'),

    # Rapporti NC
    path('aggiungi_rapporto_nc/', RapportoNCCreateView.as_view(), name="aggiungi_rapporto_nc"), 
    path('modifica_rapporto_nc/<int:pk>/', RapportoNCUpdateView.as_view(), name="modifica_rapporto_nc"), 
    path('delete_rapporto_nc/<int:pk>', delete_rapporto_nc, name="delete_rapporto_nc"),

    # Rapporti Audit
    path('aggiungi_rapporto_audit/', RapportoAuditCreateView.as_view(), name="aggiungi_rapporto_audit"), 
    path('modifica_rapporto_audit/<int:pk>/', RapportoAuditUpdateView.as_view(), name="modifica_rapporto_audit"), 
    path('delete_rapporto_audit/<int:pk>', delete_rapporto_audit, name="delete_rapporto_audit"),
    
]