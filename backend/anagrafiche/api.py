from rest_framework import viewsets, filters
from .models import Cliente, Fornitore
from .serializers import ClienteSerializer, FornitoreSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .filters import FornitoreFilterFE, ClienteFilterFE
from rest_framework.permissions import IsAuthenticated


class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all().order_by("ragionesociale")
    serializer_class = ClienteSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = ClienteFilterFE
    search_fields = ["ragionesociale"]
    ordering_fields = ["ragionesociale"]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save()


class FornitoreViewSet(viewsets.ModelViewSet):
    queryset = Fornitore.objects.all().order_by("ragionesociale")
    serializer_class = FornitoreSerializer
    filterset_class = FornitoreFilterFE

    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save()
