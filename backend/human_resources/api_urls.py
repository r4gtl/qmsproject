"""
URL routing per Human Resources API.

Base path: /api/human-resources/

Endpoints registrati:
- /dipendenti/              HumanResource CRUD + search
- /centri-di-lavoro/        CentrodiLavoro CRUD
- /reparti/                 Ward CRUD
- /mansioni/                Role CRUD
- /valutazioni/             ValutazioneOperatore CRUD
- /registro-ore-lavoro/     RegistroOreLavoro CRUD
- /aree-formazione/         AreaFormazione CRUD
- /corsi-formazione/        CorsoFormazione CRUD
- /registri-formazione/     RegistroFormazione CRUD (dashboard)
- /dettagli-formazione/     DettaglioRegistroFormazione CRUD + /current/
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
    RegistroOreLavoroViewSet,
    AreaFormazioneViewSet,
    CorsoFormazioneViewSet,
    RegistroFormazioneViewSet,
    DettaglioRegistroFormazioneViewSet,
)

router = DefaultRouter()

# Dipendenti
router.register(r"dipendenti", HumanResourceViewSet, basename="dipendente")

# Tabelle generiche
router.register(
    r"centri-di-lavoro", CentrodiLavoroViewSet, basename="centrodilavoro"
)
router.register(r"reparti", WardViewSet, basename="reparto")
router.register(r"mansioni", RoleViewSet, basename="mansione")
router.register(
    r"incarichi-sicurezza", SafetyRoleViewSet, basename="incarichisicurezza"
)

# Incarichi sicurezza per dipendente
router.register(r"hr-safety", HRSafetyViewSet, basename="hrsafety")

# Valutazioni
router.register(r"valutazioni", ValutazioneOperatoreViewSet, basename="valutazione")

# Registro Ore Lavoro
router.register(
    r"registro-ore-lavoro", RegistroOreLavoroViewSet, basename="registroorelavoro"
)

# Formazione
router.register(
    r"aree-formazione", AreaFormazioneViewSet, basename="areaformazione"
)
router.register(
    r"corsi-formazione", CorsoFormazioneViewSet, basename="corsoformazione"
)
router.register(
    r"registri-formazione", RegistroFormazioneViewSet, basename="registroformazione"
)
router.register(
    r"dettagli-formazione",
    DettaglioRegistroFormazioneViewSet,
    basename="dettaglioformazione"
)

urlpatterns = router.urls
