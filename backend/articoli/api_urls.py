from rest_framework.routers import DefaultRouter
from .api import (
    ArticoloViewSet,
    ElencoTestViewSet,
    FaseLavoroViewSet,
    DettaglioFaseLavoroViewSet,
)

router = DefaultRouter()
router.register("articoli", ArticoloViewSet)
router.register(r"elenco-test", ElencoTestViewSet)
router.register(r"fasi-lavoro", FaseLavoroViewSet)
router.register(
    r"fasi-lavoro-dettaglio", DettaglioFaseLavoroViewSet, basename="faselavoro-dettagli"
)


urlpatterns = router.urls
