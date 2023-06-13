from django.urls import path
from .views import (dashboard_manutenzioni, 
                    AttrezzaturaCreateView, AttrezzaturaUpdateView, delete_attrezzatura,
                    )

app_name="manutenzioni"

urlpatterns = [
    
    # Home Procedure
    path('', dashboard_manutenzioni, name='dashboard_manutenzioni'),    

    # Manage Attrezzatura
    path('crea_attrezzatura/', AttrezzaturaCreateView.as_view(), name="crea_attrezzatura"), 
    path('modifica_attrezzatura/<int:pk>/', AttrezzaturaUpdateView.as_view(), name="modifica_attrezzatura"), 
    path('delete_attrezzatura/<int:pk>', delete_attrezzatura, name="delete_attrezzatura"),

]