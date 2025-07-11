from rest_framework import viewsets
from .models import TipoAnimale, TipoGrezzo
from .serializers import TipoAnimaleSerializer, TipoGrezzoSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class TipoAnimaleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TipoAnimale.objects.all().order_by("descrizione")
    serializer_class = TipoAnimaleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class TipoGrezzoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TipoGrezzo.objects.all().order_by("descrizione")
    serializer_class = TipoGrezzoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
