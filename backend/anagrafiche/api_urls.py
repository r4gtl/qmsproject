from rest_framework.routers import DefaultRouter
from .api import ClienteViewSet, FornitoreViewSet, LWGFornitoreViewSet

router = DefaultRouter()
router.register("clienti", ClienteViewSet, basename="cliente")
router.register("fornitori", FornitoreViewSet, basename="fornitore")
router.register("lwgfornitori", LWGFornitoreViewSet, basename="lwgfornitore")

urlpatterns = router.urls
