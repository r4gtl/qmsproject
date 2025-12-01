from rest_framework.routers import DefaultRouter
from .api import ClienteViewSet, FornitoreViewSet

router = DefaultRouter()
router.register("clienti", ClienteViewSet, basename="cliente")
router.register("fornitori", FornitoreViewSet, basename="fornitore")

urlpatterns = router.urls
