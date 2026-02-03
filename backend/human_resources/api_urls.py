"""
URL routing per Human Resources API.

Base path: /api/human-resources/

Endpoints registrati:
- /dipendenti/           HumanResource CRUD + search
- /centri-di-lavoro/     CentrodiLavoro CRUD
- /reparti/              Ward CRUD
- /mansioni/             Role CRUD
- /valutazioni/          ValutazioneOperatore CRUD
"""
from rest_framework.routers import DefaultRouter
from .api import (
    HumanResourceViewSet,
    CentrodiLavoroViewSet,
    WardViewSet,
    RoleViewSet,
    ValutazioneOperatoreViewSet,
    SafetyRoleViewSet,
    HRSafetyViewSet,
)

router = DefaultRouter()

# Dipendenti
router.register(r"dipendenti", HumanResourceViewSet, basename="dipendente")

# Tabelle generiche
router.register(r"centri-di-lavoro", CentrodiLavoroViewSet, basename="centrodilavoro")
router.register(r"reparti", WardViewSet, basename="reparto")
router.register(r"mansioni", RoleViewSet, basename="mansione")
router.register(r"incarichi-sicurezza", SafetyRoleViewSet, basename="incarichisicurezza")

# Incarichi sicurezza per dipendente
router.register(r"hr-safety", HRSafetyViewSet, basename="hrsafety")

# Valutazioni
router.register(r"valutazioni", ValutazioneOperatoreViewSet, basename="valutazione")

urlpatterns = router.urls
