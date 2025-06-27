from rest_framework import viewsets
from .models import Cliente, Fornitore
from .serializers import ClienteSerializer, FornitoreSerializer


class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer


class FornitoreViewSet(viewsets.ModelViewSet):
    queryset = Fornitore.objects.all()
    serializer_class = FornitoreSerializer
