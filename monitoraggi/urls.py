from django.urls import path
from monitoraggi.views import (dashboard_monitoraggi,
                               MonitoraggioAcquaCreateView, MonitoraggioAcquaUpdateView, delete_monitoraggio_acqua,                                     
                               MonitoraggioGasCreateView, MonitoraggioGasUpdateView, delete_monitoraggio_gas,
                               MonitoraggioEnergiaElettricaCreateView, MonitoraggioEnergiaElettricaUpdateView, delete_monitoraggio_energia_elettrica,
                               DatoProduzioneCreateView, DatoProduzioneUpdateView, delete_lettura_dato_produzione,
                                    )
from .charts import produzione_ultimo_anno

app_name="monitoraggi"

urlpatterns = [
    
    # Home Monitoraggi
    path('', dashboard_monitoraggi, name='dashboard_monitoraggi'),    

    # Monitoraggio Acqua    
    path('inserisci_lettura_acqua/', MonitoraggioAcquaCreateView.as_view(), name="inserisci_lettura_acqua"), 
    path('modifica_lettura_acqua/<int:pk>/', MonitoraggioAcquaUpdateView.as_view(), name="modifica_lettura_acqua"), 
    path('delete_monitoraggio_acqua/<int:pk>', delete_monitoraggio_acqua, name="delete_monitoraggio_acqua"),

    # Monitoraggio Gas    
    path('inserisci_lettura_gas/', MonitoraggioGasCreateView.as_view(), name="inserisci_lettura_gas"), 
    path('modifica_lettura_gas/<int:pk>/', MonitoraggioGasUpdateView.as_view(), name="modifica_lettura_gas"), 
    path('delete_monitoraggio_gas/<int:pk>', delete_monitoraggio_gas, name="delete_monitoraggio_gas"),

    # Monitoraggio Energia Elettrica    
    path('inserisci_lettura_energia_elettrica/', MonitoraggioEnergiaElettricaCreateView.as_view(), name="inserisci_lettura_energia_elettrica"), 
    path('modifica_lettura_energia_elettrica/<int:pk>/', MonitoraggioEnergiaElettricaUpdateView.as_view(), name="modifica_lettura_energia_elettrica"), 
    path('delete_monitoraggio_energia_elettrica/<int:pk>', delete_monitoraggio_gas, name="delete_monitoraggio_energia_elettrica"),

    # Dati produzione    
    path('inserisci_lettura_dato_produzione/', DatoProduzioneCreateView.as_view(), name="inserisci_lettura_dato_produzione"), 
    path('modifica_lettura_dato_produzione/<int:pk>/', DatoProduzioneUpdateView.as_view(), name="modifica_lettura_dato_produzione"), 
    path('delete_lettura_dato_produzione/<int:pk>', delete_lettura_dato_produzione, name="delete_lettura_dato_produzione"),
    
    # Charts
    path('produzione_ultimo_anno/', produzione_ultimo_anno, name='produzione_ultimo_anno'),
    
]