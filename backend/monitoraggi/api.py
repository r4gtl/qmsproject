"""
ViewSets per Monitoraggi API.

Endpoints:
- /api/monitoraggi/acqua/                  MonitoraggioAcqua CRUD
- /api/monitoraggi/gas/                    MonitoraggioGas CRUD
- /api/monitoraggi/energia-elettrica/      MonitoraggioEnergiaElettrica CRUD
- /api/monitoraggi/dati-produzione/        DatoProduzione CRUD
"""
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .models import (
    MonitoraggioAcqua,
    MonitoraggioGas,
    MonitoraggioEnergiaElettrica,
    DatoProduzione,
)
from .serializers import (
    MonitoraggioAcquaSerializer,
    MonitoraggioGasSerializer,
    MonitoraggioEnergiaElettricaSerializer,
    DatoProduzioneSerializer,
)


# =============================================================================
# MONITORAGGIO ACQUA
# =============================================================================

class MonitoraggioAcquaViewSet(viewsets.ModelViewSet):
    """
    ViewSet per MonitoraggioAcqua.

    Endpoints:
    - GET /acqua/                  Lista paginata, ordinata per -data_lettura
    - GET /acqua/?search=          Ricerca per note
    - GET /acqua/{id}/             Dettaglio monitoraggio
    - POST /acqua/                 Crea monitoraggio
    - PATCH /acqua/{id}/           Modifica monitoraggio
    - DELETE /acqua/{id}/          Elimina monitoraggio
    """
    queryset = MonitoraggioAcqua.objects.all()
    serializer_class = MonitoraggioAcquaSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    search_fields = ["note"]
    ordering_fields = ["data_lettura", "mc_in", "mc_out"]
    ordering = ["-data_lettura"]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


# =============================================================================
# MONITORAGGIO GAS
# =============================================================================

class MonitoraggioGasViewSet(viewsets.ModelViewSet):
    """
    ViewSet per MonitoraggioGas.

    Endpoints:
    - GET /gas/                    Lista paginata, ordinata per -data_lettura
    - GET /gas/?search=            Ricerca per note
    - GET /gas/{id}/               Dettaglio monitoraggio
    - POST /gas/                   Crea monitoraggio
    - PATCH /gas/{id}/             Modifica monitoraggio
    - DELETE /gas/{id}/            Elimina monitoraggio
    """
    queryset = MonitoraggioGas.objects.all()
    serializer_class = MonitoraggioGasSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    search_fields = ["note"]
    ordering_fields = ["data_lettura", "mc_in"]
    ordering = ["-data_lettura"]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


# =============================================================================
# MONITORAGGIO ENERGIA ELETTRICA
# =============================================================================

class MonitoraggioEnergiaElettricaViewSet(viewsets.ModelViewSet):
    """
    ViewSet per MonitoraggioEnergiaElettrica.

    Endpoints:
    - GET /energia-elettrica/      Lista paginata, ordinata per -data_lettura
    - GET /energia-elettrica/?search=  Ricerca per note
    - GET /energia-elettrica/{id}/ Dettaglio monitoraggio
    - POST /energia-elettrica/     Crea monitoraggio
    - PATCH /energia-elettrica/{id}/   Modifica monitoraggio
    - DELETE /energia-elettrica/{id}/  Elimina monitoraggio
    """
    queryset = MonitoraggioEnergiaElettrica.objects.all()
    serializer_class = MonitoraggioEnergiaElettricaSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    search_fields = ["note"]
    ordering_fields = ["data_lettura", "kwh_in"]
    ordering = ["-data_lettura"]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


# =============================================================================
# DATO PRODUZIONE
# =============================================================================

class DatoProduzioneViewSet(viewsets.ModelViewSet):
    """
    ViewSet per DatoProduzione.

    Endpoints:
    - GET /dati-produzione/        Lista paginata, ordinata per -data_inserimento
    - GET /dati-produzione/?search=    Ricerca per note
    - GET /dati-produzione/?industries_served=   Filtra per destinazione
    - GET /dati-produzione/?fk_tipoanimale=      Filtra per tipo animale
    - GET /dati-produzione/{id}/   Dettaglio dato produzione
    - POST /dati-produzione/       Crea dato produzione
    - PATCH /dati-produzione/{id}/ Modifica dato produzione
    - DELETE /dati-produzione/{id}/ Elimina dato produzione
    """
    queryset = DatoProduzione.objects.select_related("fk_tipoanimale").all()
    serializer_class = DatoProduzioneSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["industries_served", "fk_tipoanimale"]
    search_fields = ["note"]
    ordering_fields = ["data_inserimento", "n_pelli", "mq", "kg"]
    ordering = ["-data_inserimento"]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
