from django.urls import path
from manualeprocedure.views import (procedure_home, 
                                    ProceduraCreateView, ProceduraUpdateView, delete_procedura,
                                    RevisioneProceduraCreateView, RevisioneProceduraUpdateView, delete_revisione_procedura,
                                    ModuloCreateView, ModuloUpdateView, delete_modulo,
                                    RevisioneModuloCreateView, RevisioneModuloUpdateView, delete_revisione_modulo
                                    )

app_name="manualeprocedure"

urlpatterns = [
    
    # Home Procedure
    path('', procedure_home, name='procedure_home'),    

    # Manage Procedure
    path('crea_procedura/', ProceduraCreateView.as_view(), name="crea_procedura"), 
    path('modifica_procedura/<int:pk>/', ProceduraUpdateView.as_view(), name="modifica_procedura"), 
    path('delete_procedura/<int:pk>', delete_procedura, name="delete_procedura"),

    # Manage Revisioni Procedure
    path('<int:fk_procedura>/crea_revisione_procedura/', RevisioneProceduraCreateView.as_view(), name="crea_revisione_procedura"), 
    path('<int:fk_procedura>/modifica_revisione_procedura/<int:pk>/', RevisioneProceduraUpdateView.as_view(), name="modifica_revisione_procedura"), 
    path('delete_revisione_procedura/<int:pk>', delete_revisione_procedura, name="delete_revisione_procedura"),

    # Manage moduli
    path('<int:pk>/crea_modulo/', ModuloCreateView.as_view(), name="crea_modulo"), 
    path('<int:fk_procedura>/modifica_modulo/<int:pk>/', ModuloUpdateView.as_view(), name="modifica_modulo"),     
    path('delete_modulo/<int:pk>', delete_modulo, name="delete_modulo"),
    
    # Manage revisione moduli
    path('<int:fk_modulo>/crea_revisione_modulo/', RevisioneModuloCreateView.as_view(), name="crea_revisione_modulo"), 
    path('<int:fk_modulo>/modifica_revisione_modulo/<int:pk>/', RevisioneModuloUpdateView.as_view(), name="modifica_revisione_modulo"), 
    path('delete_revisione_modulo/<int:pk>', delete_revisione_modulo, name="delete_revisione_modulo"),
]