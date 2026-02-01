from rest_framework.routers import DefaultRouter
from .api import (
    ArticoloViewSet,
    ElencoTestViewSet,
    FaseLavoroViewSet,
    DettaglioFaseLavoroViewSet,
    LavorazioneEsternaViewSet,
    # Procedure ViewSets
    ProceduraViewSet,
    DettaglioProceduraViewSet,
    CaratteristicaProceduraViewSet,
)

router = DefaultRouter()
router.register("articoli", ArticoloViewSet)
router.register(r"elenco-test", ElencoTestViewSet)
router.register(r"fasi-lavoro", FaseLavoroViewSet)
router.register(
    r"fasi-lavoro-dettaglio", DettaglioFaseLavoroViewSet, basename="faselavoro-dettagli"
)
router.register(r"lavorazioni-esterne", LavorazioneEsternaViewSet)

# Procedure endpoints
router.register(r"procedure", ProceduraViewSet, basename="procedure")
router.register(r"dettagli-procedura", DettaglioProceduraViewSet, basename="dettagli-procedura")
router.register(r"caratteristiche-procedura", CaratteristicaProceduraViewSet, basename="caratteristiche-procedura")


urlpatterns = router.urls
