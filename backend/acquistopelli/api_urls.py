from rest_framework.routers import DefaultRouter
from .api import (
    TipoAnimaleViewSet, TipoGrezzoViewSet, SceltaViewSet,
    LwgRegioneViewSet, LwgSubregioneViewSet, NazioneViewSet,
    LottoViewSet, SceltaLottoViewSet, LottoOrigineViewSet,
)

router = DefaultRouter()

# Tabelle generiche
router.register("tipoanimali", TipoAnimaleViewSet)
router.register("tipogrezzi", TipoGrezzoViewSet)
router.register("scelte", SceltaViewSet)

# LWG / Nazioni
router.register("regioni", LwgRegioneViewSet)
router.register("subregioni", LwgSubregioneViewSet)
router.register("nazioni", NazioneViewSet)

# Lotti
router.register("lotti", LottoViewSet, basename="lotto")
router.register("scelte-lotto", SceltaLottoViewSet,
                basename="sceltalotto")
router.register("lotto-origini", LottoOrigineViewSet,
                basename="lottoorigine")

urlpatterns = router.urls
