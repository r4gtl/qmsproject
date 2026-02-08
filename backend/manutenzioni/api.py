"""
ViewSets per Manutenzioni API.

Endpoints:
- /api/manutenzioni/attrezzature/                  Attrezzatura CRUD + search
- /api/manutenzioni/manutenzioni-straordinarie/    ManutenzioneStraordinaria CRUD (filtro per fk_attrezzatura)
- /api/manutenzioni/manutenzioni-ordinarie/        ManutenzioneOrdinaria CRUD (filtro per fk_attrezzatura)
- /api/manutenzioni/tarature/                      Taratura CRUD (filtro per fk_attrezzatura)
- /api/manutenzioni/controlli-periodici/           ControlloPeriodico CRUD (filtro per fk_attrezzatura)
"""
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db import IntegrityError
from django.db.models import Q
from django.db.models.deletion import ProtectedError
from django.http import HttpResponse, Http404
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
import os

from .models import (
    Attrezzatura,
    ManutenzioneStraordinaria,
    ManutenzioneOrdinaria,
    Taratura,
    ControlloPeriodico,
)
from .serializers import (
    AttrezzaturaListSerializer,
    AttrezzaturaDetailSerializer,
    AttrezzaturaWriteSerializer,
    ManutenzioneStraordinariaSerializer,
    ManutenzioneOrdinariaSerializer,
    TaraturaSerializer,
    ControlloPeriodicoSerializer,
)


# =============================================================================
# ATTREZZATURA
# =============================================================================

class AttrezzaturaViewSet(viewsets.ModelViewSet):
    """
    ViewSet per Attrezzature.

    Endpoints:
    - GET /attrezzature/                  Lista paginata, ordinata per codice_attrezzatura
    - GET /attrezzature/?q=compressore    Ricerca per codice/descrizione/modello (icontains, OR)
    - GET /attrezzature/?is_dismesso=     Filtra per stato dismissione
    - GET /attrezzature/{id}/             Dettaglio attrezzatura
    - POST /attrezzature/                 Crea attrezzatura (supporta multipart per image)
    - PATCH /attrezzature/{id}/           Modifica attrezzatura
    - DELETE /attrezzature/{id}/          Elimina attrezzatura

    Query params:
    - q: cerca per codice, descrizione O modello (case insensitive)
    - is_dismesso: true/false
    - is_taratura: true/false
    - fk_ward: filtra per reparto
    - ordering: campo ordinamento (es: codice_attrezzatura, descrizione)
    """
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["is_dismesso", "is_taratura", "fk_ward", "fk_human_resource"]
    ordering_fields = [
        "codice_attrezzatura",
        "descrizione",
        "modello",
        "data_dismissione",
        "created_at",
    ]
    ordering = ["codice_attrezzatura"]  # Default ordering

    def get_queryset(self):
        """
        Queryset con ricerca custom via param 'q'.
        Filtra automaticamente per company dell'utente.
        """
        company = self.request.user.profile.company
        qs = Attrezzatura.objects.filter(company=company).select_related(
            "fk_ward", "fk_human_resource"
        )

        # Filtro ricerca per codice/descrizione/modello
        q = self.request.query_params.get("q", "").strip()
        if q:
            qs = qs.filter(
                Q(codice_attrezzatura__icontains=q) |
                Q(descrizione__icontains=q) |
                Q(modello__icontains=q)
            )

        return qs

    def get_serializer_class(self):
        """
        Serializer diverso per list vs detail vs write.
        """
        if self.action == "list":
            return AttrezzaturaListSerializer
        elif self.action in ["create", "update", "partial_update"]:
            return AttrezzaturaWriteSerializer
        return AttrezzaturaDetailSerializer

    def create(self, request, *args, **kwargs):
        """Override per ritornare il detail serializer dopo create."""
        write_serializer = self.get_serializer(data=request.data)
        write_serializer.is_valid(raise_exception=True)
        instance = write_serializer.save()
        # Ritorna con detail serializer per avere tutti i campi
        detail_serializer = AttrezzaturaDetailSerializer(instance, context={'request': request})
        return Response(detail_serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """Override per ritornare il detail serializer dopo update."""
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        write_serializer = self.get_serializer(
            instance, data=request.data, partial=partial
        )
        write_serializer.is_valid(raise_exception=True)
        instance = write_serializer.save()
        detail_serializer = AttrezzaturaDetailSerializer(instance, context={'request': request})
        return Response(detail_serializer.data)

    def destroy(self, request, *args, **kwargs):
        """Handle ProtectedError when deleting attrezzatura with related records."""
        try:
            return super().destroy(request, *args, **kwargs)
        except (ProtectedError, IntegrityError):
            return Response(
                {"detail": "Impossibile eliminare: attrezzatura ha manutenzioni/tarature/controlli associati."},
                status=status.HTTP_409_CONFLICT
            )


# =============================================================================
# MANUTENZIONE STRAORDINARIA
# =============================================================================

class ManutenzioneStraordinariaViewSet(viewsets.ModelViewSet):
    """
    ViewSet per ManutenzioneStraordinaria.

    Endpoints:
    - GET /manutenzioni-straordinarie/                     Lista tutte
    - GET /manutenzioni-straordinarie/?fk_attrezzatura=123 Filtra per attrezzatura
    - GET /manutenzioni-straordinarie/{id}/                Dettaglio
    - POST /manutenzioni-straordinarie/                    Crea
    - PATCH /manutenzioni-straordinarie/{id}/              Modifica
    - DELETE /manutenzioni-straordinarie/{id}/             Elimina
    """
    serializer_class = ManutenzioneStraordinariaSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["fk_attrezzatura", "fk_fornitore"]
    ordering_fields = ["data_manutenzione", "importo", "created_at"]
    ordering = ["-data_manutenzione"]  # Default: più recenti prima

    def get_queryset(self):
        company = self.request.user.profile.company
        return ManutenzioneStraordinaria.objects.filter(company=company).select_related(
            "fk_attrezzatura", "fk_fornitore"
        )


# =============================================================================
# MANUTENZIONE ORDINARIA
# =============================================================================

class ManutenzioneOrdinariaViewSet(viewsets.ModelViewSet):
    """
    ViewSet per ManutenzioneOrdinaria.

    Endpoints:
    - GET /manutenzioni-ordinarie/                     Lista tutte
    - GET /manutenzioni-ordinarie/?fk_attrezzatura=123 Filtra per attrezzatura
    - GET /manutenzioni-ordinarie/{id}/                Dettaglio
    - POST /manutenzioni-ordinarie/                    Crea
    - PATCH /manutenzioni-ordinarie/{id}/              Modifica
    - DELETE /manutenzioni-ordinarie/{id}/             Elimina
    """
    serializer_class = ManutenzioneOrdinariaSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["fk_attrezzatura", "fk_fornitore", "is_eseguita"]
    ordering_fields = ["data_manutenzione", "prossima_scadenza", "created_at"]
    ordering = ["-data_manutenzione"]  # Default: più recenti prima

    def get_queryset(self):
        company = self.request.user.profile.company
        return ManutenzioneOrdinaria.objects.filter(company=company).select_related(
            "fk_attrezzatura", "fk_fornitore"
        )


# =============================================================================
# TARATURA
# =============================================================================

class TaraturaViewSet(viewsets.ModelViewSet):
    """
    ViewSet per Taratura.

    Endpoints:
    - GET /tarature/                     Lista tutte
    - GET /tarature/?fk_attrezzatura=123 Filtra per attrezzatura
    - GET /tarature/{id}/                Dettaglio
    - POST /tarature/                    Crea (supporta multipart per documento)
    - PATCH /tarature/{id}/              Modifica
    - DELETE /tarature/{id}/             Elimina
    """
    serializer_class = TaraturaSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["fk_attrezzatura", "fk_fornitore", "is_conforme"]
    ordering_fields = ["data_taratura", "prossima_scadenza", "created_at"]
    ordering = ["-data_taratura"]  # Default: più recenti prima

    def get_queryset(self):
        company = self.request.user.profile.company
        return Taratura.objects.filter(company=company).select_related(
            "fk_attrezzatura", "fk_fornitore"
        )

    @action(detail=True, methods=['get'], url_path='download')
    def download(self, request, pk=None):
        """
        Protected download endpoint for Taratura documento.
        Uses X-Accel-Redirect for efficient file serving via NGINX.

        Security: Only users with access to this Taratura (via company filter)
        can download the documento.

        GET /api/manutenzioni/tarature/{id}/download/
        """
        # get_object() uses get_queryset() which is already filtered by company
        taratura = self.get_object()

        # Check if documento exists
        if not taratura.documento:
            raise Http404("Nessun documento associato a questa taratura")

        # Get documento file name
        documento_name = taratura.documento.name
        if not documento_name:
            raise Http404("Nessun documento associato a questa taratura")

        # X-Accel-Redirect path (NGINX internal location)
        # documento_name is relative to MEDIA_ROOT (e.g., "tarature/doc_123.pdf")
        protected_path = f"/protected-media/{documento_name}"

        # Extract filename for Content-Disposition
        filename = os.path.basename(documento_name)

        # Return empty response with X-Accel-Redirect header
        # NGINX will handle the actual file serving
        response = HttpResponse()
        response['X-Accel-Redirect'] = protected_path
        response['Content-Disposition'] = f'inline; filename="{filename}"'

        # Optional: Set content type based on file extension
        if filename.lower().endswith('.pdf'):
            response['Content-Type'] = 'application/pdf'

        return response


# =============================================================================
# CONTROLLO PERIODICO
# =============================================================================

class ControlloPeriodicoViewSet(viewsets.ModelViewSet):
    """
    ViewSet per ControlloPeriodico.

    Endpoints:
    - GET /controlli-periodici/                     Lista tutti
    - GET /controlli-periodici/?fk_attrezzatura=123 Filtra per attrezzatura
    - GET /controlli-periodici/{id}/                Dettaglio
    - POST /controlli-periodici/                    Crea
    - PATCH /controlli-periodici/{id}/              Modifica
    - DELETE /controlli-periodici/{id}/             Elimina
    """
    serializer_class = ControlloPeriodicoSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["fk_attrezzatura", "fk_human_resource", "is_eseguita"]
    ordering_fields = ["data_controllo", "prossima_scadenza", "created_at"]
    ordering = ["-data_controllo"]  # Default: più recenti prima

    def get_queryset(self):
        company = self.request.user.profile.company
        return ControlloPeriodico.objects.filter(company=company).select_related(
            "fk_attrezzatura", "fk_human_resource"
        )
