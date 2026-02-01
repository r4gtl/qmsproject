from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import (
    Articolo,
    ElencoTest,
    FaseLavoro,
    DettaglioFaseLavoro,
    LavorazioneEsterna,
    Procedura,
    DettaglioProcedura,
    CaratteristicaProcedura,
)
from .serializers import (
    ArticoloSerializer,
    ElencoTestSerializer,
    FaseLavoroSerializer,
    DettaglioFaseLavoroSerializer,
    LavorazioneEsternaSerializer,
    # Procedure serializers
    ProceduraListSerializer,
    ProceduraDetailSerializer,
    ProceduraCreateSerializer,
    ProceduraCloneSerializer,
    DettaglioProceduraSerializer,
    DettaglioProceduraWriteSerializer,
    CaratteristicaProceduraSerializer,
    ReorderDettagliSerializer,
    ReorderCaratteristicheSerializer,
)
from .services.procedure import (
    reorder_dettagli,
    reorder_caratteristiche,
    get_next_dettaglio_numero_riga,
    get_next_caratteristica_numero_riga,
    DomainValidationError,
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


class LavorazioneEsternaViewSet(viewsets.ModelViewSet):
    queryset = LavorazioneEsterna.objects.all().order_by("descrizione")
    serializer_class = LavorazioneEsternaSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save()


# =============================================================================
# PROCEDURE VIEWSETS
# =============================================================================

class ProceduraViewSet(viewsets.ModelViewSet):
    """
    ViewSet per Procedura.

    Endpoints:
    - GET /procedure/?fk_articolo=X         Lista procedure per articolo
    - POST /procedure/                       Crea nuova revisione (usa service)
    - GET /procedure/{id}/                   Dettaglio con righe annidate
    - PATCH /procedure/{id}/                 Modifica campi editabili
    - POST /procedure/{id}/clone/            Clona come nuova revisione
    - POST /procedure/{id}/reorder-dettagli/ Riordina le righe
    """
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["fk_articolo"]
    ordering_fields = ["nr_procedura", "nr_revisione", "created_at"]
    ordering = ["-nr_procedura", "-nr_revisione"]

    def get_queryset(self):
        """
        Queryset ottimizzato per evitare N+1.

        Per retrieve (detail): prefetch dettagli + caratteristiche annidate.
        Per list: solo conteggio dettagli (no nested).
        """
        from django.db.models import Prefetch

        qs = Procedura.objects.select_related("fk_articolo", "created_by")

        if self.action in ["retrieve", "clone"]:
            # Prefetch completo per detail view
            qs = qs.prefetch_related(
                Prefetch(
                    "dettagli",
                    queryset=DettaglioProcedura.objects.select_related(
                        "fk_faselavoro", "fk_fornitore"
                    ).prefetch_related(
                        Prefetch(
                            "caratteristiche",
                            queryset=CaratteristicaProcedura.objects.select_related(
                                "fk_fornitore",
                                "fk_lavorazione_esterna",
                                "fk_dettaglio_fase_lavoro",
                            ).order_by("numero_riga")
                        )
                    ).order_by("numero_riga")
                )
            )
        else:
            # Per list: solo prefetch leggero per count
            qs = qs.prefetch_related("dettagli")

        return qs

    def get_serializer_class(self):
        if self.action == "list":
            return ProceduraListSerializer
        elif self.action == "create":
            return ProceduraCreateSerializer
        elif self.action == "clone":
            return ProceduraCloneSerializer
        elif self.action == "reorder_dettagli":
            return ReorderDettagliSerializer
        return ProceduraDetailSerializer

    def perform_update(self, serializer):
        # Solo note e data_revisione sono editabili
        serializer.save()

    @action(detail=True, methods=["post"])
    def clone(self, request, pk=None):
        """
        Clona la procedura come nuova revisione.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.context["procedura_id"] = pk
        serializer.is_valid(raise_exception=True)
        nuova_procedura = serializer.save()
        return Response(
            ProceduraDetailSerializer(nuova_procedura).data,
            status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=["post"], url_path="reorder-dettagli")
    def reorder_dettagli(self, request, pk=None):
        """
        Riordina i dettagli della procedura.

        Body: { "ordered_ids": [12, 9, 10] }
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            updated = reorder_dettagli(
                procedura_id=pk,
                ordered_ids=serializer.validated_data["ordered_ids"]
            )
            return Response(
                DettaglioProceduraSerializer(updated, many=True).data
            )
        except DomainValidationError as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class DettaglioProceduraViewSet(viewsets.ModelViewSet):
    """
    ViewSet per DettaglioProcedura (righe).

    Endpoints:
    - GET /dettagli-procedura/?fk_procedura=X  Lista righe
    - POST /dettagli-procedura/                 Crea riga
    - GET/PATCH/DELETE /dettagli-procedura/{id}/
    - POST /dettagli-procedura/{id}/reorder-caratteristiche/
    """
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["fk_procedura"]
    ordering = ["numero_riga"]

    def get_queryset(self):
        """
        Queryset ottimizzato per evitare N+1.
        Include prefetch completo per caratteristiche nested.
        """
        from django.db.models import Prefetch

        return DettaglioProcedura.objects.select_related(
            "fk_procedura", "fk_faselavoro", "fk_fornitore", "created_by"
        ).prefetch_related(
            Prefetch(
                "caratteristiche",
                queryset=CaratteristicaProcedura.objects.select_related(
                    "fk_fornitore",
                    "fk_lavorazione_esterna",
                    "fk_dettaglio_fase_lavoro",
                ).order_by("numero_riga")
            )
        )

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return DettaglioProceduraWriteSerializer
        elif self.action == "reorder_caratteristiche":
            return ReorderCaratteristicheSerializer
        return DettaglioProceduraSerializer

    def perform_create(self, serializer):
        # Auto-assegna numero_riga se non specificato
        if "numero_riga" not in serializer.validated_data:
            procedura_id = serializer.validated_data["fk_procedura"].id
            serializer.validated_data["numero_riga"] = get_next_dettaglio_numero_riga(procedura_id)
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=["post"], url_path="reorder-caratteristiche")
    def reorder_caratteristiche(self, request, pk=None):
        """
        Riordina le caratteristiche del dettaglio.

        Body: { "ordered_ids": [5, 3, 7] }
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            updated = reorder_caratteristiche(
                dettaglio_id=pk,
                ordered_ids=serializer.validated_data["ordered_ids"]
            )
            return Response(
                CaratteristicaProceduraSerializer(updated, many=True).data
            )
        except DomainValidationError as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class CaratteristicaProceduraViewSet(viewsets.ModelViewSet):
    """
    ViewSet per CaratteristicaProcedura.

    Endpoints:
    - GET /caratteristiche-procedura/?fk_dettaglio_procedura=X
    - POST/PATCH/DELETE standard
    """
    permission_classes = [IsAuthenticated]
    serializer_class = CaratteristicaProceduraSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["fk_dettaglio_procedura"]
    ordering = ["numero_riga"]

    def get_queryset(self):
        return CaratteristicaProcedura.objects.select_related(
            "fk_dettaglio_procedura",
            "fk_fornitore",
            "fk_lavorazione_esterna",
            "fk_dettaglio_fase_lavoro",
            "created_by",
        )

    def perform_create(self, serializer):
        # Auto-assegna numero_riga se non specificato
        if "numero_riga" not in serializer.validated_data:
            dettaglio_id = serializer.validated_data["fk_dettaglio_procedura"].id
            serializer.validated_data["numero_riga"] = get_next_caratteristica_numero_riga(dettaglio_id)
        serializer.save(created_by=self.request.user)
