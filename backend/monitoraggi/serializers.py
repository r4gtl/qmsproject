from rest_framework import serializers
from .models import (
    MonitoraggioAcqua,
    MonitoraggioGas,
    MonitoraggioEnergiaElettrica,
    DatoProduzione,
)


# =============================================================================
# MONITORAGGIO ACQUA
# =============================================================================

class MonitoraggioAcquaSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonitoraggioAcqua
        fields = [
            "id",
            "data_lettura",
            "mc_in",
            "mc_out",
            "note",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]


# =============================================================================
# MONITORAGGIO GAS
# =============================================================================

class MonitoraggioGasSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonitoraggioGas
        fields = [
            "id",
            "data_lettura",
            "mc_in",
            "note",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]


# =============================================================================
# MONITORAGGIO ENERGIA ELETTRICA
# =============================================================================

class MonitoraggioEnergiaElettricaSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonitoraggioEnergiaElettrica
        fields = [
            "id",
            "data_lettura",
            "kwh_in",
            "note",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]


# =============================================================================
# DATO PRODUZIONE
# =============================================================================

class DatoProduzioneSerializer(serializers.ModelSerializer):
    tipoanimale_descrizione = serializers.CharField(
        source="fk_tipoanimale.descrizione",
        read_only=True,
        allow_null=True,
    )
    industries_served_display = serializers.CharField(
        source="get_industries_served_display",
        read_only=True,
    )

    class Meta:
        model = DatoProduzione
        fields = [
            "id",
            "data_inserimento",
            "industries_served",
            "industries_served_display",
            "fk_tipoanimale",
            "tipoanimale_descrizione",
            "n_pelli",
            "mq",
            "kg",
            "note",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]
