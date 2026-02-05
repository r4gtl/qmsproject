from rest_framework import serializers
from .models import (
    TipoAnimale, TipoGrezzo, Scelta,
    LwgRegione, LwgSubregione, Nazione,
    Lotto, SceltaLotto, LottoOrigine,
)


# =============================================================================
# TABELLE GENERICHE
# =============================================================================

class TipoAnimaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoAnimale
        fields = ["id", "descrizione"]


class TipoGrezzoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoGrezzo
        fields = ["id", "descrizione"]


class SceltaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scelta
        fields = ["id", "descrizione"]


# =============================================================================
# LWG REGIONI / SUBREGIONI / NAZIONI
# =============================================================================

class LwgRegioneSerializer(serializers.ModelSerializer):
    class Meta:
        model = LwgRegione
        fields = ["id", "codice_m49", "nome_regione"]


class LwgSubregioneSerializer(serializers.ModelSerializer):
    regione_nome = serializers.CharField(
        source="regione.nome_regione", read_only=True,
    )

    class Meta:
        model = LwgSubregione
        fields = [
            "id", "regione", "regione_nome",
            "codice_m49", "nome_subregione",
        ]


class NazioneSerializer(serializers.ModelSerializer):
    regione_nome = serializers.CharField(
        source="regione.nome_regione", read_only=True, allow_null=True,
    )
    subregione_nome = serializers.CharField(
        source="subregione.nome_subregione", read_only=True, allow_null=True,
    )

    class Meta:
        model = Nazione
        fields = [
            "id", "sigla_estesa", "descrizione", "sigla", "codice_m49",
            "regione", "regione_nome", "subregione", "subregione_nome",
        ]


# =============================================================================
# SCELTA LOTTO
# =============================================================================

class SceltaLottoSerializer(serializers.ModelSerializer):
    scelta_descrizione = serializers.CharField(
        source="fk_scelta.descrizione", read_only=True,
    )

    class Meta:
        model = SceltaLotto
        fields = [
            "id", "fk_lotto", "fk_scelta", "scelta_descrizione",
            "pezzi", "scelta_terminata", "data_termine", "note",
        ]
        read_only_fields = ["id"]


# =============================================================================
# LOTTO ORIGINE
# =============================================================================

class LottoOrigineSerializer(serializers.ModelSerializer):
    nazione_display = serializers.SerializerMethodField()
    regione_display = serializers.CharField(
        source="regione.nome_regione", read_only=True, allow_null=True,
    )
    subregione_display = serializers.CharField(
        source="subregione.nome_subregione", read_only=True, allow_null=True,
    )

    class Meta:
        model = LottoOrigine
        fields = [
            "id", "lotto", "nazione", "nazione_display",
            "regione", "regione_display", "subregione", "subregione_display",
            "quota_percentuale", "qta_stimata", "livello_rischio",
            "fonte_dato", "note", "livello_precisione",
        ]
        read_only_fields = ["id"]

    def get_nazione_display(self, obj):
        if obj.nazione:
            return (
                obj.nazione.descrizione
                or obj.nazione.sigla
                or str(obj.nazione.pk)
            )
        return None


# =============================================================================
# LOTTO
# =============================================================================

class LottoListSerializer(serializers.ModelSerializer):
    """Serializer per lista lotti (dashboard). Campi minimi + display."""
    fornitore_ragionesociale = serializers.CharField(
        source="fk_fornitore.ragionesociale", read_only=True,
    )
    tipoanimale_descrizione = serializers.CharField(
        source="fk_tipoanimale.descrizione", read_only=True, allow_null=True,
    )
    tipogrezzo_descrizione = serializers.CharField(
        source="fk_tipogrezzo.descrizione", read_only=True, allow_null=True,
    )

    class Meta:
        model = Lotto
        fields = [
            "id", "data_acquisto", "identificativo",
            "fk_fornitore", "fornitore_ragionesociale",
            "fk_tipoanimale", "tipoanimale_descrizione",
            "fk_tipogrezzo", "tipogrezzo_descrizione",
            "origine", "pezzi", "peso_totale", "is_lwg",
        ]


class LottoDetailSerializer(serializers.ModelSerializer):
    """Serializer per dettaglio lotto con nested scelte e origini."""
    fornitore_ragionesociale = serializers.CharField(
        source="fk_fornitore.ragionesociale", read_only=True,
    )
    tipoanimale_descrizione = serializers.CharField(
        source="fk_tipoanimale.descrizione", read_only=True, allow_null=True,
    )
    tipogrezzo_descrizione = serializers.CharField(
        source="fk_tipogrezzo.descrizione", read_only=True, allow_null=True,
    )
    macello_ragionesociale = serializers.CharField(
        source="fk_macello.ragionesociale", read_only=True, allow_null=True,
    )
    scelte = SceltaLottoSerializer(
        source="sceltalotto_set", many=True, read_only=True,
    )
    origini = LottoOrigineSerializer(many=True, read_only=True)

    class Meta:
        model = Lotto
        fields = [
            "id", "data_acquisto", "identificativo",
            "fk_fornitore", "fornitore_ragionesociale",
            "fk_tipoanimale", "tipoanimale_descrizione",
            "fk_tipogrezzo", "tipogrezzo_descrizione",
            "fk_macello", "macello_ragionesociale",
            "origine", "documento", "is_lwg",
            "peso_totale", "pezzi", "prezzo_unitario",
            "spese_accessorie", "kg_km", "note",
            "created_by", "created_at",
            "scelte", "origini",
        ]
        read_only_fields = ["id", "created_by", "created_at"]


class LottoWriteSerializer(serializers.ModelSerializer):
    """Serializer per create/update lotto."""

    class Meta:
        model = Lotto
        fields = [
            "data_acquisto", "identificativo",
            "fk_fornitore", "fk_tipoanimale", "fk_tipogrezzo",
            "fk_macello", "origine", "documento", "is_lwg",
            "peso_totale", "pezzi", "prezzo_unitario",
            "spese_accessorie", "kg_km", "note",
        ]

    def create(self, validated_data):
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            validated_data["created_by"] = request.user
        return super().create(validated_data)
