from django.urls import path
from core.views import home, dashboard

app_name="core"

urlpatterns = [
    
    path('dashboard/', dashboard, name='dashboard'),    
]