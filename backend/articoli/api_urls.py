from rest_framework.routers import DefaultRouter
from .api import (
    ArticoloViewSet,
    ElencoTestViewSet,
    FaseLavoroViewSet,
    DettaglioFaseLavoroViewSet,
    LavorazioneEsternaViewSet,
)

router = DefaultRouter()
router.register("articoli", ArticoloViewSet)
router.register(r"elenco-test", ElencoTestViewSet)
router.register(r"fasi-lavoro", FaseLavoroViewSet)
router.register(
    r"fasi-lavoro-dettaglio", DettaglioFaseLavoroViewSet, basename="faselavoro-dettagli"
)
router.register(r"lavorazioni-esterne", LavorazioneEsternaViewSet)


urlpatterns = router.urls
