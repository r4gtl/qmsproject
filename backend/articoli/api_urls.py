from rest_framework.routers import DefaultRouter
from .api import ArticoloViewSet, ElencoTestViewSet, FaseLavoroViewSet

router = DefaultRouter()
router.register("articoli", ArticoloViewSet)
router.register(r"elenco-test", ElencoTestViewSet)
router.register(r"fasi-lavoro", FaseLavoroViewSet)

urlpatterns = router.urls
