from rest_framework import viewsets, filters
from .models import Articolo, ElencoTest, FaseLavoro, DettaglioFaseLavoro
from .serializers import (
    ArticoloSerializer,
    ElencoTestSerializer,
    FaseLavoroSerializer,
    DettaglioFaseLavoroSerializer,
)
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ArticoloFilter
from rest_framework.permissions import IsAuthenticated


class ArticoloViewSet(viewsets.ModelViewSet):
    queryset = Articolo.objects.all().order_by("descrizione")
    serializer_class = ArticoloSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = ArticoloFilter
    search_fields = ["descrizione"]
    ordering_fields = ["descrizione"]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save()


class ElencoTestViewSet(viewsets.ModelViewSet):
    queryset = ElencoTest.objects.all().order_by("descrizione")
    serializer_class = ElencoTestSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save()


class FaseLavoroViewSet(viewsets.ModelViewSet):
    queryset = FaseLavoro.objects.all().order_by("descrizione")
    serializer_class = FaseLavoroSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save()


class DettaglioFaseLavoroViewSet(viewsets.ModelViewSet):
    queryset = DettaglioFaseLavoro.objects.all()
    serializer_class = DettaglioFaseLavoroSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
