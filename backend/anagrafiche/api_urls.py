from rest_framework.routers import DefaultRouter
from .api import ClienteViewSet, FornitoreViewSet

router = DefaultRouter()
router = DefaultRouter()
router.register("clienti", ClienteViewSet)
router.register("fornitori", FornitoreViewSet)


urlpatterns = router.urls
