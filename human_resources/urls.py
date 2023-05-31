from django.urls import path

from .views import (human_resources_home,
                    update_human_resource,
                    add_new_operator,
                    tabelle_generiche,
                    WardCreateView, WardUpdateView, delete_ward,
                    RoleCreateView, RoleUpdateView, delete_role,
                    )

app_name = 'human_resources'

urlpatterns = [
    path('', human_resources_home, name="human_resources"),
    path('update_human_resource/<int:pk>/', update_human_resource, name="update-human-resource"),
    path('create_human_resource/', add_new_operator, name="create-human-resource"),  

    # Tabelle generiche
    path('tabelle_generiche/', tabelle_generiche, name="tabelle_generiche"),  


    # Ward 
    path('create_ward/', WardCreateView.as_view(), name="create_ward"),  
    path('update_ward/<int:pk>', WardUpdateView.as_view(), name="update_ward"),  
    path('delete_ward/<int:pk>', delete_ward, name="delete_ward"),  

    # Role
    path('create_role/', RoleCreateView.as_view(), name="create_role"),  
    path('update_role/<int:pk>', RoleUpdateView.as_view(), name="update_role"),  
    path('delete_role/<int:pk>', delete_role, name="delete_role"),  
    
    
]