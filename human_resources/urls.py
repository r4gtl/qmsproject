from django.urls import path

from . import views

app_name = 'human_resources'

urlpatterns = [
    path('human_resources/', views.human_resources_home, name="human_resources"),
    path('update_human_resource/<int:pk>/', views.update_human_resource, name="update-human-resource"),
    path('create_human_resource/', views.add_new_operator, name="create-human-resource"),    
]