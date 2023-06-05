from django.urls import path

from .views import (human_resources_home,
                    update_human_resource, HRUpdateView,
                    add_new_operator,
                    tabelle_generiche,
                    tabelle_generiche_formazione,
                    dashboard_formazione,
                    WardCreateView, WardUpdateView, delete_ward,
                    RoleCreateView, RoleUpdateView, delete_role,
                    AreaFormazioneCreateView, AreaFormazioneUpdateView, delete_area_formazione,
                    CorsoFormazioneCreateView, CorsoFormazioneUpdateView, delete_corso_formazione,
                    RegistroFormazioneCreateView, RegistroFormazioneUpdateView, delete_registro_formazione,
                    DettaglioRegistroFormazioneCreateView, DettaglioRegistroFormazioneUpdateView, delete_dettaglio_registro_formazione, 
                    ore_formazione
                    
                    )

app_name = 'human_resources'

urlpatterns = [
    
    # Tabelle generiche
    path('tabelle_generiche/', tabelle_generiche, name="tabelle_generiche"),  
    path('tabelle_generiche_formazione/', tabelle_generiche_formazione, name="tabelle_generiche_formazione"),  
    
    # Human Resources
    path('', human_resources_home, name="human_resources"),
    path('update_human_resource/<int:pk>/', HRUpdateView.as_view(), name="update-human-resource"),
    path('create_human_resource/', add_new_operator, name="create-human-resource"), 
    
    # Dashboard formazione 
    path('dashboard_formazione/', dashboard_formazione, name="dashboard_formazione"), 
    # Charts
    path('ore_formazione/', ore_formazione, name='ore_formazione'),


    # Ward 
    path('create_ward/', WardCreateView.as_view(), name="create_ward"),  
    path('update_ward/<int:pk>', WardUpdateView.as_view(), name="update_ward"),  
    path('delete_ward/<int:pk>', delete_ward, name="delete_ward"),  

    # Role
    path('create_role/', RoleCreateView.as_view(), name="create_role"),  
    path('update_role/<int:pk>', RoleUpdateView.as_view(), name="update_role"),  
    path('delete_role/<int:pk>', delete_role, name="delete_role"),
    
    # Area Formazione
    path('crea_area_formazione/', AreaFormazioneCreateView.as_view(), name="crea_area_formazione"),  
    path('modifica_area_formazione/<int:pk>', AreaFormazioneUpdateView.as_view(), name="modifica_area_formazione"),  
    path('delete_area_formazione/<int:pk>', delete_area_formazione, name="delete_area_formazione"),
    
    # Corso Formazione
    path('crea_corso_formazione/', CorsoFormazioneCreateView.as_view(), name="crea_corso_formazione"),  
    path('modifica_corso_formazione/<int:pk>', CorsoFormazioneUpdateView.as_view(), name="modifica_corso_formazione"),  
    path('delete_corso_formazione/<int:pk>', delete_corso_formazione, name="delete_corso_formazione"),
    
    # Registro Formazione
    path('crea_registro_formazione/', RegistroFormazioneCreateView.as_view(), name="crea_registro_formazione"),  
    path('modifica_registro_formazione/<int:pk>', RegistroFormazioneUpdateView.as_view(), name="modifica_registro_formazione"),  
    path('delete_registro_formazione/<int:pk>', delete_registro_formazione, name="delete_registro_formazione"),
    
    # Dettaglio Registro Formazione
    path('<int:pk>/crea_dettaglio_registro_formazione/', DettaglioRegistroFormazioneCreateView.as_view(), name="crea_dettaglio_registro_formazione"),  
    path('<int:pk>/modifica_dettaglio_registro_formazione/<int:id>', DettaglioRegistroFormazioneUpdateView.as_view(), name="modifica_dettaglio_registro_formazione"),  
    path('delete_dettaglio_registro_formazione/<int:pk>', delete_dettaglio_registro_formazione, name="delete_dettaglio_registro_formazione"),
    
    
    
]