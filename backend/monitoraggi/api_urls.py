"""
URL routing per Monitoraggi API.

Base path: /api/monitoraggi/

Endpoints registrati:
- /acqua/                  MonitoraggioAcqua CRUD
- /gas/                    MonitoraggioGas CRUD
- /energia-elettrica/      MonitoraggioEnergiaElettrica CRUD
- /dati-produzione/        DatoProduzione CRUD
"""
from rest_framework.routers import DefaultRouter
from .api import (
    MonitoraggioAcquaViewSet,
    MonitoraggioGasViewSet,
    MonitoraggioEnergiaElettricaViewSet,
    DatoProduzioneViewSet,
)

router = DefaultRouter()

# Monitoraggi
router.register(r"acqua", MonitoraggioAcquaViewSet, basename="monitoraggio-acqua")
router.register(r"gas", MonitoraggioGasViewSet, basename="monitoraggio-gas")
router.register(
    r"energia-elettrica",
    MonitoraggioEnergiaElettricaViewSet,
    basename="monitoraggio-energia-elettrica"
)
router.register(
    r"dati-produzione",
    DatoProduzioneViewSet,
    basename="dato-produzione"
)

urlpatterns = router.urls
