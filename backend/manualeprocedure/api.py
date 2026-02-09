"""
DRF ViewSets for Manuale Procedure API.
"""
from rest_framework import viewsets, filters, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q

from .models import SezioneLWG, Procedura, RevisioneProcedura, Modulo, RevisioneModulo
from .serializers import (
    SezioneLWGSerializer,
    ProceduraListSerializer,
    ProceduraDetailSerializer,
    ProceduraWriteSerializer,
    RevisioneProceduraSerializer,
    ModuloSerializer,
    RevisioneModuloSerializer,
)


class SezioneLWGViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for SezioneLWG (read-only).
    Populated by fixture data.json.
    """
    queryset = SezioneLWG.objects.all().order_by('lwgsection')
    serializer_class = SezioneLWGSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None  # No pagination for lookup data


class ProceduraViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Procedura.

    Filters:
    - descrizione (icontains)
    - fk_lwgsection (exact)
    - include_deleted (query param to show is_eliminata=True)

    Ordering: -data_procedura (default)
    """
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['fk_lwgsection']
    search_fields = ['descrizione', 'identificativo']
    ordering_fields = ['data_procedura', 'identificativo', 'created_at']
    ordering = ['-data_procedura']

    def get_queryset(self):
        qs = Procedura.objects.select_related('fk_lwgsection')

        # Exclude soft-deleted by default
        include_deleted = self.request.query_params.get('include_deleted', '').lower() in ['1', 'true']
        if not include_deleted:
            qs = qs.filter(is_eliminata=False)

        return qs

    def get_serializer_class(self):
        if self.action == 'list':
            return ProceduraListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return ProceduraWriteSerializer
        return ProceduraDetailSerializer

    def create(self, request, *args, **kwargs):
        write_serializer = self.get_serializer(data=request.data)
        write_serializer.is_valid(raise_exception=True)
        instance = write_serializer.save()
        detail_serializer = ProceduraDetailSerializer(instance, context={'request': request})
        return Response(detail_serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        write_serializer = self.get_serializer(instance, data=request.data, partial=partial)
        write_serializer.is_valid(raise_exception=True)
        instance = write_serializer.save()
        detail_serializer = ProceduraDetailSerializer(instance, context={'request': request})
        return Response(detail_serializer.data)


class RevisioneProceduraViewSet(viewsets.ModelViewSet):
    """
    ViewSet for RevisioneProcedura (supports file upload).

    Filter by fk_procedura.
    Ordering: -data_revisione (default).
    """
    serializer_class = RevisioneProceduraSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['fk_procedura']
    ordering_fields = ['data_revisione', 'n_revisione', 'created_at']
    ordering = ['-data_revisione']

    def get_queryset(self):
        return RevisioneProcedura.objects.select_related('fk_procedura')


class ModuloViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Modulo.

    Filter by fk_procedura.
    Ordering: -data_modulo (default).
    """
    serializer_class = ModuloSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['fk_procedura']
    ordering_fields = ['data_modulo', 'identificativo', 'created_at']
    ordering = ['-data_modulo']

    def get_queryset(self):
        return Modulo.objects.select_related('fk_procedura')


class RevisioneModuloViewSet(viewsets.ModelViewSet):
    """
    ViewSet for RevisioneModulo (supports file upload).

    Filter by fk_modulo.
    Ordering: -data_revisione (default).
    """
    serializer_class = RevisioneModuloSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['fk_modulo']
    ordering_fields = ['data_revisione', 'n_revisione', 'created_at']
    ordering = ['-data_revisione']

    def get_queryset(self):
        return RevisioneModulo.objects.select_related('fk_modulo')
