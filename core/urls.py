from core.views import dashboard
from django.urls import path

from .utils import update_numero_riga_down, update_numero_riga_up

app_name="core"

urlpatterns = [
    
    path('dashboard/', dashboard, name='dashboard'),    
      
    path('update_numero_riga_down/', update_numero_riga_down, name='update_numero_riga_down'),    
    path('update_numero_riga_up/', update_numero_riga_up, name='update_numero_riga_up'),    
     
]