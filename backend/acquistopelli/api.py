from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .models import (
    TipoAnimale, TipoGrezzo, Scelta,
    LwgRegione, LwgSubregione, Nazione,
    Lotto, SceltaLotto, LottoOrigine,
)
from .serializers import (
    TipoAnimaleSerializer, TipoGrezzoSerializer,
    SceltaSerializer,
    LwgRegioneSerializer, LwgSubregioneSerializer,
    NazioneSerializer,
    LottoListSerializer, LottoDetailSerializer,
    LottoWriteSerializer,
    SceltaLottoSerializer, LottoOrigineSerializer,
)


# =============================================================================
# TABELLE GENERICHE
# =============================================================================

class TipoAnimaleViewSet(viewsets.ModelViewSet):
    queryset = TipoAnimale.objects.all()
    serializer_class = TipoAnimaleSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [
        filters.SearchFilter, filters.OrderingFilter,
    ]
    search_fields = ["descrizione"]
    ordering = ["descrizione"]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class TipoGrezzoViewSet(viewsets.ModelViewSet):
    queryset = TipoGrezzo.objects.all()
    serializer_class = TipoGrezzoSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [
        filters.SearchFilter, filters.OrderingFilter,
    ]
    search_fields = ["descrizione"]
    ordering = ["descrizione"]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class SceltaViewSet(viewsets.ModelViewSet):
    queryset = Scelta.objects.all()
    serializer_class = SceltaSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [
        filters.SearchFilter, filters.OrderingFilter,
    ]
    search_fields = ["descrizione"]
    ordering = ["descrizione"]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


# =========================================================
# LWG REGIONI / SUBREGIONI / NAZIONI
# =========================================================

class LwgRegioneViewSet(viewsets.ModelViewSet):
    queryset = LwgRegione.objects.all()
    serializer_class = LwgRegioneSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [
        filters.SearchFilter, filters.OrderingFilter,
    ]
    search_fields = ["nome_regione"]
    ordering = ["nome_regione"]


class LwgSubregioneViewSet(viewsets.ModelViewSet):
    queryset = LwgSubregione.objects.select_related(
        "regione",
    ).all()
    serializer_class = LwgSubregioneSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["regione"]
    search_fields = ["nome_subregione"]
    ordering = ["nome_subregione"]


class NazioneViewSet(viewsets.ModelViewSet):
    queryset = Nazione.objects.select_related(
        "regione", "subregione",
    ).all()
    serializer_class = NazioneSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["regione", "subregione"]
    search_fields = ["descrizione", "sigla", "sigla_estesa"]
    ordering = ["descrizione"]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


# =========================================================
# LOTTO
# =========================================================

class LottoViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = [
        "fk_fornitore", "fk_tipoanimale", "fk_tipogrezzo",
    ]
    search_fields = ["identificativo"]
    ordering_fields = ["data_acquisto", "identificativo"]
    ordering = ["-data_acquisto"]

    def get_queryset(self):
        qs = Lotto.objects.select_related(
            "fk_fornitore", "fk_tipoanimale",
            "fk_tipogrezzo", "fk_macello",
        )
        if self.action == "retrieve":
            qs = qs.prefetch_related(
                "sceltalotto_set__fk_scelta",
                "origini__nazione",
                "origini__regione",
                "origini__subregione",
            )
        return qs

    def get_serializer_class(self):
        if self.action == "list":
            return LottoListSerializer
        if self.action in (
            "create", "update", "partial_update",
        ):
            return LottoWriteSerializer
        return LottoDetailSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


# =========================================================
# SCELTA LOTTO
# =========================================================

class SceltaLottoViewSet(viewsets.ModelViewSet):
    serializer_class = SceltaLottoSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["fk_lotto"]

    def get_queryset(self):
        return SceltaLotto.objects.select_related(
            "fk_scelta",
        ).all()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


# =========================================================
# LOTTO ORIGINE
# =========================================================

class LottoOrigineViewSet(viewsets.ModelViewSet):
    serializer_class = LottoOrigineSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["lotto"]

    def get_queryset(self):
        return LottoOrigine.objects.select_related(
            "nazione", "regione", "subregione",
        ).all()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
