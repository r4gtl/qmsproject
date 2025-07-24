from rest_framework.routers import DefaultRouter
from .api import ArticoloViewSet, ElencoTestViewSet

router = DefaultRouter()
router.register("articoli", ArticoloViewSet)
router.register(r"elenco-test", ElencoTestViewSet)

urlpatterns = router.urls
