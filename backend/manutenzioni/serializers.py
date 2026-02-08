"""
Serializers per Manutenzioni API.

Moduli:
- Attrezzatura
- ManutenzioneStraordinaria
- ManutenzioneOrdinaria
- Taratura
- ControlloPeriodico
"""
from rest_framework import serializers
from .models import (
    Attrezzatura,
    ManutenzioneStraordinaria,
    ManutenzioneOrdinaria,
    Taratura,
    ControlloPeriodico,
)


# =============================================================================
# ATTREZZATURA
# =============================================================================

class AttrezzaturaListSerializer(serializers.ModelSerializer):
    """
    Serializer per lista attrezzature.
    Campi minimi per performance nella tabella lista.
    """
    fk_ward_display = serializers.CharField(
        source="fk_ward.description",
        read_only=True,
        allow_null=True,
    )
    fk_human_resource_display = serializers.SerializerMethodField()

    class Meta:
        model = Attrezzatura
        fields = [
            "id",
            "codice_attrezzatura",
            "descrizione",
            "modello",
            "fk_ward",
            "fk_ward_display",
            "fk_human_resource",
            "fk_human_resource_display",
            "is_dismesso",
            "is_taratura",
        ]

    def get_fk_human_resource_display(self, obj):
        return str(obj.fk_human_resource) if obj.fk_human_resource else None


class AttrezzaturaDetailSerializer(serializers.ModelSerializer):
    """
    Serializer per dettaglio attrezzatura.
    Include tutti i campi + FK con display name.
    """
    fk_ward_display = serializers.CharField(
        source="fk_ward.description",
        read_only=True,
        allow_null=True,
    )
    fk_human_resource_display = serializers.SerializerMethodField()

    class Meta:
        model = Attrezzatura
        fields = [
            "id",
            "codice_attrezzatura",
            "descrizione",
            "modello",
            "serie_matricola",
            "fk_ward",
            "fk_ward_display",
            "is_dismesso",
            "data_dismissione",
            "is_taratura",
            "periodo_taratura",
            "procedura_controlli_periodici",
            "periodo_controlli_periodici",
            "riferimento_normativo_controlli_periodici",
            "fk_human_resource",
            "fk_human_resource_display",
            "image",
            "note",
            "created_by",
            "created_at",
        ]
        read_only_fields = ["id", "created_by", "created_at"]

    def get_fk_human_resource_display(self, obj):
        return str(obj.fk_human_resource) if obj.fk_human_resource else None


class AttrezzaturaWriteSerializer(serializers.ModelSerializer):
    """
    Serializer per create/update attrezzatura.
    Validazioni:
    - codice_attrezzatura e descrizione obbligatori
    - data_dismissione richiede is_dismesso=True
    """

    class Meta:
        model = Attrezzatura
        fields = [
            "codice_attrezzatura",
            "descrizione",
            "modello",
            "serie_matricola",
            "fk_ward",
            "is_dismesso",
            "data_dismissione",
            "is_taratura",
            "periodo_taratura",
            "procedura_controlli_periodici",
            "periodo_controlli_periodici",
            "riferimento_normativo_controlli_periodici",
            "fk_human_resource",
            "image",
            "note",
        ]

    def validate_codice_attrezzatura(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Il codice attrezzatura è obbligatorio.")
        return value.strip()

    def validate_descrizione(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("La descrizione è obbligatoria.")
        return value.strip()

    def validate(self, data):
        """Validazione cross-field: data_dismissione richiede is_dismesso=True."""
        is_dismesso = data.get("is_dismesso", False)
        data_dismissione = data.get("data_dismissione")

        if data_dismissione and not is_dismesso:
            raise serializers.ValidationError({
                "data_dismissione": "La data dismissione può essere inserita solo se l'attrezzatura è dismessa."
            })

        return data

    def create(self, validated_data):
        """Autopopolamento created_by dall'utente loggato."""
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['created_by'] = request.user
        return super().create(validated_data)


# =============================================================================
# MANUTENZIONE STRAORDINARIA
# =============================================================================

class ManutenzioneStraordinariaSerializer(serializers.ModelSerializer):
    """
    Serializer per ManutenzioneStraordinaria.
    Include display names per FK.
    """
    fk_attrezzatura_display = serializers.CharField(
        source="fk_attrezzatura.descrizione",
        read_only=True,
    )
    fk_fornitore_display = serializers.CharField(
        source="fk_fornitore.ragionesociale",
        read_only=True,
        allow_null=True,
    )

    class Meta:
        model = ManutenzioneStraordinaria
        fields = [
            "id",
            "fk_attrezzatura",
            "fk_attrezzatura_display",
            "data_manutenzione",
            "descrizione",
            "importo",
            "ore_fermo",
            "fk_fornitore",
            "fk_fornitore_display",
            "ft_prot",
            "data_fattura",
            "note",
            "created_by",
            "created_at",
        ]
        read_only_fields = ["id", "created_by", "created_at"]

    def validate_data_manutenzione(self, value):
        if not value:
            raise serializers.ValidationError("La data manutenzione è obbligatoria.")
        return value

    def create(self, validated_data):
        """Autopopolamento created_by dall'utente loggato."""
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['created_by'] = request.user
        return super().create(validated_data)


# =============================================================================
# MANUTENZIONE ORDINARIA
# =============================================================================

class ManutenzioneOrdinariaSerializer(serializers.ModelSerializer):
    """
    Serializer per ManutenzioneOrdinaria.
    Include display names per FK.
    """
    fk_attrezzatura_display = serializers.CharField(
        source="fk_attrezzatura.descrizione",
        read_only=True,
    )
    fk_fornitore_display = serializers.CharField(
        source="fk_fornitore.ragionesociale",
        read_only=True,
        allow_null=True,
    )

    class Meta:
        model = ManutenzioneOrdinaria
        fields = [
            "id",
            "fk_attrezzatura",
            "fk_attrezzatura_display",
            "data_manutenzione",
            "descrizione",
            "fk_fornitore",
            "fk_fornitore_display",
            "is_eseguita",
            "prossima_scadenza",
            "note",
            "created_by",
            "created_at",
        ]
        read_only_fields = ["id", "created_by", "created_at"]

    def validate_data_manutenzione(self, value):
        if not value:
            raise serializers.ValidationError("La data manutenzione è obbligatoria.")
        return value

    def create(self, validated_data):
        """Autopopolamento created_by dall'utente loggato."""
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['created_by'] = request.user
        return super().create(validated_data)


# =============================================================================
# TARATURA
# =============================================================================

class TaraturaSerializer(serializers.ModelSerializer):
    """
    Serializer per Taratura.
    Include display names per FK e URL documento.
    """
    fk_attrezzatura_display = serializers.CharField(
        source="fk_attrezzatura.descrizione",
        read_only=True,
    )
    fk_fornitore_display = serializers.CharField(
        source="fk_fornitore.ragionesociale",
        read_only=True,
        allow_null=True,
    )
    documento_url = serializers.SerializerMethodField()

    class Meta:
        model = Taratura
        fields = [
            "id",
            "fk_attrezzatura",
            "fk_attrezzatura_display",
            "data_taratura",
            "fk_fornitore",
            "fk_fornitore_display",
            "documento",
            "documento_url",
            "is_conforme",
            "prossima_scadenza",
            "note",
            "created_by",
            "created_at",
        ]
        read_only_fields = ["id", "created_by", "created_at"]

    def get_documento_url(self, obj):
        """Ritorna URL completa del documento se presente."""
        if obj.documento:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.documento.url)
            return obj.documento.url
        return None

    def validate_data_taratura(self, value):
        if not value:
            raise serializers.ValidationError("La data taratura è obbligatoria.")
        return value

    def create(self, validated_data):
        """Autopopolamento created_by dall'utente loggato."""
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['created_by'] = request.user
        return super().create(validated_data)


# =============================================================================
# CONTROLLO PERIODICO
# =============================================================================

class ControlloPeriodicoSerializer(serializers.ModelSerializer):
    """
    Serializer per ControlloPeriodico.
    Include display names per FK.
    """
    fk_attrezzatura_display = serializers.CharField(
        source="fk_attrezzatura.descrizione",
        read_only=True,
    )
    fk_human_resource_display = serializers.SerializerMethodField()

    class Meta:
        model = ControlloPeriodico
        fields = [
            "id",
            "fk_attrezzatura",
            "fk_attrezzatura_display",
            "data_controllo",
            "descrizione",
            "fk_human_resource",
            "fk_human_resource_display",
            "is_eseguita",
            "prossima_scadenza",
            "note",
            "created_by",
            "created_at",
        ]
        read_only_fields = ["id", "created_by", "created_at"]

    def get_fk_human_resource_display(self, obj):
        return str(obj.fk_human_resource) if obj.fk_human_resource else None

    def validate_data_controllo(self, value):
        if not value:
            raise serializers.ValidationError("La data controllo è obbligatoria.")
        return value

    def create(self, validated_data):
        """Autopopolamento created_by dall'utente loggato."""
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['created_by'] = request.user
        return super().create(validated_data)
