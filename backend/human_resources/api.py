"""
ViewSets per Human Resources API.

Endpoints:
- /api/human-resources/dipendenti/          HumanResource CRUD + search
- /api/human-resources/centri-di-lavoro/    CentrodiLavoro CRUD
- /api/human-resources/reparti/             Ward CRUD
- /api/human-resources/mansioni/            Role CRUD
- /api/human-resources/valutazioni/         ValutazioneOperatore CRUD (filtro per fk_hr)
"""
from rest_framework import viewsets, filters, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db import IntegrityError
from django.db.models import Q
from django.db.models.deletion import ProtectedError

from .models import (
    HumanResource,
    CentrodiLavoro,
    Ward,
    Role,
    ValutazioneOperatore,
    Safety_Role,
    HR_Safety,
    RegistroOreLavoro,
)
from .serializers import (
    HumanResourceListSerializer,
    HumanResourceDetailSerializer,
    HumanResourceWriteSerializer,
    CentrodiLavoroSerializer,
    WardSerializer,
    RoleSerializer,
    ValutazioneOperatoreSerializer,
    SafetyRoleSerializer,
    HRSafetySerializer,
    RegistroOreLavoroListSerializer,
    RegistroOreLavoroDetailSerializer,
    RegistroOreLavoroWriteSerializer,
)


# =============================================================================
# HUMAN RESOURCE (DIPENDENTI)
# =============================================================================

class HumanResourceViewSet(viewsets.ModelViewSet):
    """
    ViewSet per Dipendenti (HumanResource).

    Endpoints:
    - GET /dipendenti/                  Lista paginata, ordinata per -dataassunzione
    - GET /dipendenti/?q=mario          Ricerca per nome/cognome (icontains, OR)
    - GET /dipendenti/{id}/             Dettaglio dipendente
    - POST /dipendenti/                 Crea dipendente
    - PATCH /dipendenti/{id}/           Modifica dipendente
    - DELETE /dipendenti/{id}/          Elimina dipendente

    Query params:
    - q: cerca per nome O cognome (case insensitive)
    - ordering: campo ordinamento (es: cognomedipendente, -dataassunzione)
    """
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = [
        "cognomedipendente",
        "nomedipendente",
        "dataassunzione",
        "datadimissioni",
    ]
    ordering = ["-dataassunzione"]  # Default ordering

    def get_queryset(self):
        """
        Queryset con ricerca custom via param 'q'.
        """
        qs = HumanResource.objects.select_related("fk_mansione", "fk_reparto")

        # Filtro ricerca per nome/cognome
        q = self.request.query_params.get("q", "").strip()
        if q:
            qs = qs.filter(
                Q(nomedipendente__icontains=q) |
                Q(cognomedipendente__icontains=q)
            )

        return qs

    def get_serializer_class(self):
        """
        Serializer diverso per list vs detail vs write.
        """
        if self.action == "list":
            return HumanResourceListSerializer
        elif self.action in ["create", "update", "partial_update"]:
            return HumanResourceWriteSerializer
        return HumanResourceDetailSerializer

    def create(self, request, *args, **kwargs):
        """Override per ritornare il detail serializer dopo create."""
        write_serializer = self.get_serializer(data=request.data)
        write_serializer.is_valid(raise_exception=True)
        instance = write_serializer.save()
        # Ritorna con detail serializer per avere tutti i campi
        detail_serializer = HumanResourceDetailSerializer(instance)
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
        detail_serializer = HumanResourceDetailSerializer(instance)
        return Response(detail_serializer.data)


# =============================================================================
# CENTRO DI LAVORO
# =============================================================================

class CentrodiLavoroViewSet(viewsets.ModelViewSet):
    """
    ViewSet per CentrodiLavoro (tabella generica).
    CRUD semplice, ordinato per description.
    """
    queryset = CentrodiLavoro.objects.all().order_by("description")
    serializer_class = CentrodiLavoroSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["description"]
    ordering_fields = ["description"]

    def destroy(self, request, *args, **kwargs):
        """Handle ProtectedError/IntegrityError when deleting a centro in use."""
        try:
            return super().destroy(request, *args, **kwargs)
        except (ProtectedError, IntegrityError):
            return Response(
                {"detail": "Impossibile eliminare: elemento in uso."},
                status=status.HTTP_409_CONFLICT
            )


# =============================================================================
# WARD (REPARTI)
# =============================================================================

class WardViewSet(viewsets.ModelViewSet):
    """
    ViewSet per Ward/Reparti (tabella generica).
    CRUD semplice, ordinato per description.
    """
    queryset = Ward.objects.all().order_by("description")
    serializer_class = WardSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["description"]
    ordering_fields = ["description"]

    def destroy(self, request, *args, **kwargs):
        """Handle ProtectedError/IntegrityError when deleting a reparto in use."""
        try:
            return super().destroy(request, *args, **kwargs)
        except (ProtectedError, IntegrityError):
            return Response(
                {"detail": "Impossibile eliminare: elemento in uso."},
                status=status.HTTP_409_CONFLICT
            )


# =============================================================================
# ROLE (MANSIONI)
# =============================================================================

class RoleViewSet(viewsets.ModelViewSet):
    """
    ViewSet per Role/Mansioni (tabella generica).
    CRUD con FK opzionale a reparto.
    """
    queryset = Role.objects.select_related("fk_reparto").order_by("description")
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["fk_reparto"]
    search_fields = ["description"]
    ordering_fields = ["description"]

    def destroy(self, request, *args, **kwargs):
        """Handle ProtectedError/IntegrityError when deleting a mansione in use."""
        try:
            return super().destroy(request, *args, **kwargs)
        except (ProtectedError, IntegrityError):
            return Response(
                {"detail": "Impossibile eliminare: elemento in uso."},
                status=status.HTTP_409_CONFLICT
            )


# =============================================================================
# VALUTAZIONE OPERATORE
# =============================================================================

class ValutazioneOperatoreViewSet(viewsets.ModelViewSet):
    """
    ViewSet per ValutazioneOperatore.

    Endpoints:
    - GET /valutazioni/                     Lista tutte le valutazioni
    - GET /valutazioni/?fk_hr=123           Lista valutazioni di un dipendente
    - GET /valutazioni/{id}/                Dettaglio valutazione
    - POST /valutazioni/                    Crea valutazione
    - PATCH /valutazioni/{id}/              Modifica valutazione
    - DELETE /valutazioni/{id}/             Elimina valutazione
    """
    serializer_class = ValutazioneOperatoreSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["fk_hr", "fk_centro_di_lavoro", "valutazione"]
    ordering_fields = ["fk_hr", "fk_centro_di_lavoro", "created_at"]
    ordering = ["fk_hr", "fk_centro_di_lavoro"]

    def get_queryset(self):
        return ValutazioneOperatore.objects.select_related(
            "fk_hr", "fk_centro_di_lavoro"
        )

    def create(self, request, *args, **kwargs):
        """Handle IntegrityError from unique constraint."""
        try:
            return super().create(request, *args, **kwargs)
        except IntegrityError:
            return Response(
                {"detail": "Esiste già una valutazione per questo dipendente e centro di lavoro."},
                status=status.HTTP_409_CONFLICT
            )

    def update(self, request, *args, **kwargs):
        """Handle IntegrityError from unique constraint."""
        try:
            return super().update(request, *args, **kwargs)
        except IntegrityError:
            return Response(
                {"detail": "Esiste già una valutazione per questo dipendente e centro di lavoro."},
                status=status.HTTP_409_CONFLICT
            )


# =============================================================================
# SAFETY ROLE (INCARICHI SICUREZZA)
# =============================================================================

class SafetyRoleViewSet(viewsets.ModelViewSet):
    """
    ViewSet per Safety_Role (Incarichi Sicurezza).
    CRUD semplice, ordinato per descrizione.
    """
    queryset = Safety_Role.objects.all().order_by("descrizione")
    serializer_class = SafetyRoleSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["descrizione"]
    ordering_fields = ["descrizione"]

    def destroy(self, request, *args, **kwargs):
        """Handle ProtectedError/IntegrityError when deleting."""
        try:
            return super().destroy(request, *args, **kwargs)
        except (ProtectedError, IntegrityError):
            return Response(
                {"detail": "Impossibile eliminare: elemento in uso."},
                status=status.HTTP_409_CONFLICT
            )


# =============================================================================
# HR SAFETY (INCARICHI SICUREZZA PER DIPENDENTE)
# =============================================================================

class HRSafetyViewSet(viewsets.ModelViewSet):
    """
    ViewSet per HR_Safety (Incarichi Sicurezza per dipendente).

    Endpoints:
    - GET /hr-safety/                     Lista tutti gli incarichi
    - GET /hr-safety/?fk_hr=123           Lista incarichi di un dipendente
    - GET /hr-safety/{id}/                Dettaglio incarico
    - POST /hr-safety/                    Crea incarico
    - PATCH /hr-safety/{id}/              Modifica incarico
    - DELETE /hr-safety/{id}/             Elimina incarico
    """
    serializer_class = HRSafetySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["fk_hr", "fk_safety_role"]
    ordering_fields = ["data_inizio_incarico", "data_fine_incarico"]
    ordering = ["fk_hr", "-data_inizio_incarico"]  # Default: per dipendente, più recenti prima

    def get_queryset(self):
        return HR_Safety.objects.select_related(
            "fk_hr", "fk_safety_role"
        ).order_by("fk_hr", "-data_inizio_incarico")

    def create(self, request, *args, **kwargs):
        """Handle ValidationError for overlap."""
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            # ValidationError già gestito dal serializer
            # Qui catturiamo solo per sicurezza
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    def update(self, request, *args, **kwargs):
        """Handle ValidationError for overlap."""
        try:
            return super().update(request, *args, **kwargs)
        except Exception as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


# =============================================================================
# REGISTRO ORE LAVORO
# =============================================================================

class RegistroOreLavoroViewSet(viewsets.ModelViewSet):
    """
    ViewSet per Registro Ore Lavoro.

    Endpoints:
    - GET /registro-ore-lavoro/              Lista paginata (ordinata -entry_year, -entry_month)
    - GET /registro-ore-lavoro/?entry_year=  Filtra per anno
    - GET /registro-ore-lavoro/{id}/         Dettaglio
    - POST /registro-ore-lavoro/             Crea registro
    - PATCH /registro-ore-lavoro/{id}/       Modifica registro
    - DELETE /registro-ore-lavoro/{id}/      Elimina registro
    """
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["entry_year", "entry_month"]
    ordering_fields = ["entry_year", "entry_month"]
    ordering = ["-entry_year", "-entry_month"]

    def get_queryset(self):
        return RegistroOreLavoro.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return RegistroOreLavoroListSerializer
        elif self.action in ["create", "update", "partial_update"]:
            return RegistroOreLavoroWriteSerializer
        return RegistroOreLavoroDetailSerializer

    def create(self, request, *args, **kwargs):
        """Override per ritornare il detail serializer dopo create."""
        write_serializer = self.get_serializer(data=request.data)
        write_serializer.is_valid(raise_exception=True)
        instance = write_serializer.save()
        detail_serializer = RegistroOreLavoroDetailSerializer(instance)
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
        detail_serializer = RegistroOreLavoroDetailSerializer(instance)
        return Response(detail_serializer.data)
