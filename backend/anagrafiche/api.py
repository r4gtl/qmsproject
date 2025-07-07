from rest_framework import viewsets, filters
from .models import Cliente, Fornitore
from .serializers import ClienteSerializer, FornitoreSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .filters import FornitoreFilterFE


class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer


class FornitoreViewSet(viewsets.ModelViewSet):
    queryset = Fornitore.objects.all().order_by("ragionesociale")
    serializer_class = FornitoreSerializer
    filterset_class = FornitoreFilterFE
