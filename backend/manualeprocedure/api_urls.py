"""
URL routing for Manuale Procedure API.

Base path: /api/manualeprocedure/
"""
from rest_framework.routers import DefaultRouter
from .api import (
    SezioneLWGViewSet,
    ProceduraViewSet,
    RevisioneProceduraViewSet,
    ModuloViewSet,
    RevisioneModuloViewSet,
)

router = DefaultRouter()

router.register(r'sezioni-lwg', SezioneLWGViewSet, basename='sezionelwg')
router.register(r'procedure', ProceduraViewSet, basename='procedura')
router.register(r'revisioni-procedure', RevisioneProceduraViewSet, basename='revisioneprocedura')
router.register(r'moduli', ModuloViewSet, basename='modulo')
router.register(r'revisioni-moduli', RevisioneModuloViewSet, basename='revisionemodulo')

urlpatterns = router.urls
