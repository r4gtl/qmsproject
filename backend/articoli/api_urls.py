from rest_framework.routers import DefaultRouter
from .api import ArticoloViewSet

router = DefaultRouter()
router.register("articoli", ArticoloViewSet)

urlpatterns = router.urls
