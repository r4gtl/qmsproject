from rest_framework import serializers
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
from anagrafiche.models import Fornitore


class ArticoloSerializer(serializers.ModelSerializer):
    fk_tipoanimale_descrizione = serializers.CharField(
        source="fk_tipoanimale.descrizione", read_only=True
    )
    fk_tipogrezzo_descrizione = serializers.CharField(
        source="fk_tipogrezzo.descrizione", read_only=True
    )

    class Meta:
        model = Articolo
        fields = "__all__"
        read_only_fields = ["created_by"]


class ElencoTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElencoTest
        fields = "__all__"
        read_only_fields = ["created_by", "created_at"]


class FaseLavoroSerializer(serializers.ModelSerializer):
    class Meta:
        model = FaseLavoro
        fields = "__all__"
        read_only_fields = ["created_by", "created_at"]


class DettaglioFaseLavoroSerializer(serializers.ModelSerializer):
    class Meta:
        model = DettaglioFaseLavoro
        fields = "__all__"
        read_only_fields = ["id", "created_by", "created_at"]


class LavorazioneEsternaSerializer(serializers.ModelSerializer):
    class Meta:
        model = LavorazioneEsterna
        fields = "__all__"
        read_only_fields = ["created_by", "created_at"]


# =============================================================================
# PROCEDURE SERIALIZERS
# =============================================================================

class CaratteristicaProceduraSerializer(serializers.ModelSerializer):
    """
    Serializer per CaratteristicaProcedura con validazione interno/esterno.

    Regole:
    - Se DettaglioProcedura.is_interna == True:
        * fk_dettaglio_fase_lavoro OBBLIGATORIO
        * fk_fornitore e fk_lavorazione_esterna DEVONO essere NULL

    - Se DettaglioProcedura.is_interna == False:
        * fk_fornitore e fk_lavorazione_esterna OBBLIGATORI
        * fk_dettaglio_fase_lavoro DEVE essere NULL
    """
    # Campi read-only per display
    fk_fornitore_nome = serializers.CharField(
        source="fk_fornitore.ragionesociale", read_only=True
    )
    fk_lavorazione_esterna_descrizione = serializers.CharField(
        source="fk_lavorazione_esterna.descrizione", read_only=True
    )
    fk_dettaglio_fase_lavoro_attributo = serializers.CharField(
        source="fk_dettaglio_fase_lavoro.attributo", read_only=True
    )

    class Meta:
        model = CaratteristicaProcedura
        fields = [
            "id",
            "fk_dettaglio_procedura",
            "fk_fornitore",
            "fk_fornitore_nome",
            "fk_lavorazione_esterna",
            "fk_lavorazione_esterna_descrizione",
            "fk_dettaglio_fase_lavoro",
            "fk_dettaglio_fase_lavoro_attributo",
            "valore",
            "note",
            "numero_riga",
            "created_by",
            "created_at",
        ]
        read_only_fields = ["id", "created_by", "created_at"]

    def validate(self, data):
        """
        Valida coerenza tra is_interna del dettaglio e i campi della caratteristica.

        Per PATCH parziali, usa i valori esistenti dell'istanza se non presenti nei data.
        """
        dettaglio = data.get("fk_dettaglio_procedura")

        # In update, potremmo non avere dettaglio nei data
        if not dettaglio and self.instance:
            dettaglio = self.instance.fk_dettaglio_procedura

        if not dettaglio:
            return data

        is_interna = dettaglio.is_interna

        # Per PATCH: usa valori esistenti se non nei data
        def get_value(field_name):
            if field_name in data:
                return data[field_name]
            if self.instance:
                return getattr(self.instance, field_name, None)
            return None

        fk_fornitore = get_value("fk_fornitore")
        fk_lavorazione_esterna = get_value("fk_lavorazione_esterna")
        fk_dettaglio_fase_lavoro = get_value("fk_dettaglio_fase_lavoro")

        if is_interna:
            # Lavorazione INTERNA
            if fk_fornitore or fk_lavorazione_esterna:
                raise serializers.ValidationError(
                    "Per lavorazione interna, fk_fornitore e fk_lavorazione_esterna devono essere vuoti."
                )
            if not fk_dettaglio_fase_lavoro:
                raise serializers.ValidationError(
                    "Per lavorazione interna, fk_dettaglio_fase_lavoro è obbligatorio."
                )
        else:
            # Lavorazione ESTERNA
            if fk_dettaglio_fase_lavoro:
                raise serializers.ValidationError(
                    "Per lavorazione esterna, fk_dettaglio_fase_lavoro deve essere vuoto."
                )
            if not fk_fornitore:
                raise serializers.ValidationError(
                    "Per lavorazione esterna, fk_fornitore è obbligatorio."
                )
            if not fk_lavorazione_esterna:
                raise serializers.ValidationError(
                    "Per lavorazione esterna, fk_lavorazione_esterna è obbligatorio."
                )

        return data


class DettaglioProceduraSerializer(serializers.ModelSerializer):
    """
    Serializer per DettaglioProcedura.
    Include le caratteristiche annidate in read.
    """
    # Campi read-only per display
    fk_faselavoro_descrizione = serializers.CharField(
        source="fk_faselavoro.descrizione", read_only=True
    )
    fk_fornitore_nome = serializers.CharField(
        source="fk_fornitore.ragionesociale", read_only=True
    )

    # Caratteristiche annidate (solo in lettura)
    caratteristiche = CaratteristicaProceduraSerializer(many=True, read_only=True)

    # Conteggio caratteristiche per lista
    caratteristiche_count = serializers.SerializerMethodField()

    class Meta:
        model = DettaglioProcedura
        fields = [
            "id",
            "fk_procedura",
            "fk_faselavoro",
            "fk_faselavoro_descrizione",
            "fk_fornitore",
            "fk_fornitore_nome",
            "is_interna",
            "numero_riga",
            "note",
            "caratteristiche",
            "caratteristiche_count",
            "created_by",
            "created_at",
        ]
        read_only_fields = ["id", "created_by", "created_at", "caratteristiche"]

    def get_caratteristiche_count(self, obj):
        return obj.caratteristiche.count()


class DettaglioProceduraWriteSerializer(serializers.ModelSerializer):
    """
    Serializer per scrittura DettaglioProcedura (senza caratteristiche annidate).

    NOTA: fk_fornitore è DEPRECATO. Il fornitore va specificato in CaratteristicaProcedura.
    """
    class Meta:
        model = DettaglioProcedura
        fields = [
            "id",
            "fk_procedura",
            "fk_faselavoro",
            "fk_fornitore",
            "is_interna",
            "numero_riga",
            "note",
        ]
        read_only_fields = ["id"]

    def validate(self, data):
        """
        Valida coerenza is_interna e avvisa su fk_fornitore deprecato.
        """
        import logging
        logger = logging.getLogger(__name__)

        fk_fornitore = data.get("fk_fornitore")
        is_interna = data.get("is_interna", True)

        # Avviso deprecazione fk_fornitore
        if fk_fornitore:
            logger.warning(
                "DettaglioProcedura.fk_fornitore è DEPRECATO. "
                "Usa CaratteristicaProcedura.fk_fornitore invece."
            )

        # Coerenza: se is_interna=True, fk_fornitore non ha senso
        if is_interna and fk_fornitore:
            raise serializers.ValidationError(
                "fk_fornitore non può essere impostato per lavorazione interna."
            )

        return data


class ProceduraListSerializer(serializers.ModelSerializer):
    """
    Serializer leggero per lista procedure (senza dettagli annidati).
    """
    fk_articolo_descrizione = serializers.CharField(
        source="fk_articolo.descrizione", read_only=True
    )
    dettagli_count = serializers.SerializerMethodField()

    class Meta:
        model = Procedura
        fields = [
            "id",
            "fk_articolo",
            "fk_articolo_descrizione",
            "nr_procedura",
            "data_procedura",
            "nr_revisione",
            "data_revisione",
            "note",
            "dettagli_count",
            "created_by",
            "created_at",
        ]
        read_only_fields = ["id", "nr_procedura", "nr_revisione", "created_by", "created_at"]

    def get_dettagli_count(self, obj):
        return obj.dettagli.count()


class ProceduraDetailSerializer(serializers.ModelSerializer):
    """
    Serializer completo per dettaglio procedura (con dettagli annidati).
    """
    fk_articolo_descrizione = serializers.CharField(
        source="fk_articolo.descrizione", read_only=True
    )
    dettagli = DettaglioProceduraSerializer(many=True, read_only=True)

    class Meta:
        model = Procedura
        fields = [
            "id",
            "fk_articolo",
            "fk_articolo_descrizione",
            "nr_procedura",
            "data_procedura",
            "nr_revisione",
            "data_revisione",
            "note",
            "dettagli",
            "created_by",
            "created_at",
        ]
        read_only_fields = ["id", "nr_procedura", "nr_revisione", "created_by", "created_at"]


class ProceduraCreateSerializer(serializers.Serializer):
    """
    Serializer per creazione procedura (usa il service).
    """
    fk_articolo = serializers.PrimaryKeyRelatedField(queryset=Articolo.objects.all())
    note = serializers.CharField(required=False, allow_blank=True)
    data_revisione = serializers.DateField(required=False)

    def create(self, validated_data):
        from .services.procedure import create_procedura_revision

        user = self.context["request"].user
        return create_procedura_revision(
            articolo_id=validated_data["fk_articolo"].id,
            user=user,
            note=validated_data.get("note", ""),
            data_revisione=validated_data.get("data_revisione"),
        )


class ProceduraCloneSerializer(serializers.Serializer):
    """
    Serializer per clonazione procedura come nuova revisione.
    """
    note = serializers.CharField(required=False, allow_blank=True)

    def create(self, validated_data):
        from .services.procedure import clone_procedura_as_revision

        procedura_id = self.context["procedura_id"]
        user = self.context["request"].user

        return clone_procedura_as_revision(
            procedura_id=procedura_id,
            user=user,
            note=validated_data.get("note"),
        )


class ReorderDettagliSerializer(serializers.Serializer):
    """
    Serializer per riordinare i dettagli di una procedura.
    """
    ordered_ids = serializers.ListField(
        child=serializers.IntegerField(),
        min_length=1,
    )

    def validate_ordered_ids(self, value):
        # Verifica che non ci siano duplicati
        if len(value) != len(set(value)):
            raise serializers.ValidationError("ID duplicati non ammessi.")
        return value


class ReorderCaratteristicheSerializer(serializers.Serializer):
    """
    Serializer per riordinare le caratteristiche di un dettaglio.
    """
    ordered_ids = serializers.ListField(
        child=serializers.IntegerField(),
        min_length=1,
    )

    def validate_ordered_ids(self, value):
        if len(value) != len(set(value)):
            raise serializers.ValidationError("ID duplicati non ammessi.")
        return value
