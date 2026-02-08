"""
URL routing per Manutenzioni API.

Base path: /api/manutenzioni/

Endpoints registrati:
- /attrezzature/                  Attrezzatura CRUD + search
- /manutenzioni-straordinarie/    ManutenzioneStraordinaria CRUD
- /manutenzioni-ordinarie/        ManutenzioneOrdinaria CRUD
- /tarature/                      Taratura CRUD
- /controlli-periodici/           ControlloPeriodico CRUD
"""
from rest_framework.routers import DefaultRouter
from .api import (
    AttrezzaturaViewSet,
    ManutenzioneStraordinariaViewSet,
    ManutenzioneOrdinariaViewSet,
    TaraturaViewSet,
    ControlloPeriodicoViewSet,
)

router = DefaultRouter()

# Attrezzature
router.register(r"attrezzature", AttrezzaturaViewSet, basename="attrezzatura")

# Manutenzioni straordinarie
router.register(
    r"manutenzioni-straordinarie",
    ManutenzioneStraordinariaViewSet,
    basename="manutenzionestraordinaria"
)

# Manutenzioni ordinarie
router.register(
    r"manutenzioni-ordinarie",
    ManutenzioneOrdinariaViewSet,
    basename="manutenzioneordinaria"
)

# Tarature
router.register(r"tarature", TaraturaViewSet, basename="taratura")

# Controlli periodici
router.register(
    r"controlli-periodici",
    ControlloPeriodicoViewSet,
    basename="controlloperiodico"
)

urlpatterns = router.urls
