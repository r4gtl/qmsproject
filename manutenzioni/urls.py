from django.urls import path
from .views import (dashboard_manutenzioni, 
                    AttrezzaturaCreateView, AttrezzaturaUpdateView, delete_attrezzatura,
                    ManutenzioneOrdinariaCreateView, ManutenzioneOrdinariaUpdateView, delete_manutenzione_ordinaria,
                    )

app_name="manutenzioni"

urlpatterns = [
    
    # Home Procedure
    path('', dashboard_manutenzioni, name='dashboard_manutenzioni'),    

    # Manage Attrezzatura
    path('crea_attrezzatura/', AttrezzaturaCreateView.as_view(), name="crea_attrezzatura"), 
    path('modifica_attrezzatura/<int:pk>/', AttrezzaturaUpdateView.as_view(), name="modifica_attrezzatura"), 
    path('delete_attrezzatura/<int:pk>', delete_attrezzatura, name="delete_attrezzatura"),

    # Manage Manutenzione Ordinaria
    path('<int:fk_attrezzatura>/aggiungi_manutenzione_ordinaria/', ManutenzioneOrdinariaCreateView.as_view(), name="aggiungi_manutenzione_ordinaria"), 
    path('<int:fk_attrezzatura>/modifica_manutenzione_ordinaria/<int:pk>/', ManutenzioneOrdinariaUpdateView.as_view(), name="modifica_manutenzione_ordinaria"), 
    path('delete_manutenzione_ordinaria/<int:pk>', delete_manutenzione_ordinaria, name="delete_manutenzione_ordinaria"),

]