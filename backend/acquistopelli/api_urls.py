from rest_framework.routers import DefaultRouter
from .api import TipoAnimaleViewSet, TipoGrezzoViewSet

router = DefaultRouter()
router.register("tipoanimali", TipoAnimaleViewSet)
router.register("tipogrezzi", TipoGrezzoViewSet)

urlpatterns = router.urls
