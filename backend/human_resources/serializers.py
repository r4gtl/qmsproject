"""
Serializers per Human Resources API.

Moduli:
- HumanResource (Dipendenti)
- CentrodiLavoro
- Ward (Reparti)
- Role (Mansioni)
- ValutazioneOperatore
"""
from rest_framework import serializers
from .models import (
    HumanResource,
    CentrodiLavoro,
    Ward,
    Role,
    ValutazioneOperatore,
)


# =============================================================================
# CENTRO DI LAVORO
# =============================================================================

class CentrodiLavoroSerializer(serializers.ModelSerializer):
    """Serializer per CentrodiLavoro (tabella generica)."""

    class Meta:
        model = CentrodiLavoro
        fields = ["id", "description", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]


# =============================================================================
# WARD (REPARTI)
# =============================================================================

class WardSerializer(serializers.ModelSerializer):
    """Serializer per Ward/Reparti (tabella generica)."""

    class Meta:
        model = Ward
        fields = ["id", "description", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]


# =============================================================================
# ROLE (MANSIONI)
# =============================================================================

class RoleSerializer(serializers.ModelSerializer):
    """
    Serializer per Role/Mansioni.
    Include fk_reparto come ID + campo display per leggibilità.
    """
    fk_reparto_display = serializers.CharField(
        source="fk_reparto.description",
        read_only=True,
        allow_null=True,
    )

    class Meta:
        model = Role
        fields = [
            "id",
            "description",
            "fk_reparto",
            "fk_reparto_display",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


# =============================================================================
# HUMAN RESOURCE (DIPENDENTI)
# =============================================================================

class HumanResourceListSerializer(serializers.ModelSerializer):
    """
    Serializer per lista dipendenti.
    Campi minimi per performance.
    """
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = HumanResource
        fields = [
            "id",
            "cognomedipendente",
            "nomedipendente",
            "full_name",
            "dataassunzione",
            "datadimissioni",
        ]

    def get_full_name(self, obj):
        return f"{obj.cognomedipendente} {obj.nomedipendente}"


class HumanResourceDetailSerializer(serializers.ModelSerializer):
    """
    Serializer per dettaglio dipendente.
    Include tutti i campi + FK con display name.
    """
    full_name = serializers.SerializerMethodField()
    fk_mansione_display = serializers.CharField(
        source="fk_mansione.description",
        read_only=True,
        allow_null=True,
    )
    fk_reparto_display = serializers.CharField(
        source="fk_reparto.description",
        read_only=True,
        allow_null=True,
    )
    # Country come codice ISO
    country_code = serializers.CharField(source="country.code", read_only=True, allow_null=True)
    country_name = serializers.CharField(source="country.name", read_only=True, allow_null=True)

    class Meta:
        model = HumanResource
        fields = [
            "id",
            "cognomedipendente",
            "nomedipendente",
            "full_name",
            "data_nascita",
            "country",
            "country_code",
            "country_name",
            "immagine",
            "gender",
            "contratto",
            "orario",
            "dataassunzione",
            "datadimissioni",
            "fk_mansione",
            "fk_mansione_display",
            "fk_reparto",
            "fk_reparto_display",
            "qualifica",
            "commenti",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def get_full_name(self, obj):
        return f"{obj.cognomedipendente} {obj.nomedipendente}"


class HumanResourceWriteSerializer(serializers.ModelSerializer):
    """
    Serializer per create/update dipendente.
    Validazioni:
    - dataassunzione obbligatorio
    - nome/cognome obbligatori
    """

    class Meta:
        model = HumanResource
        fields = [
            "cognomedipendente",
            "nomedipendente",
            "data_nascita",
            "country",
            "immagine",
            "gender",
            "contratto",
            "orario",
            "dataassunzione",
            "datadimissioni",
            "fk_mansione",
            "fk_reparto",
            "qualifica",
            "commenti",
        ]

    def validate_cognomedipendente(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Il cognome è obbligatorio.")
        return value.strip()

    def validate_nomedipendente(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Il nome è obbligatorio.")
        return value.strip()

    def validate_dataassunzione(self, value):
        if not value:
            raise serializers.ValidationError("La data di assunzione è obbligatoria.")
        return value

    def validate(self, data):
        """Validazione cross-field: datadimissioni >= dataassunzione."""
        dataassunzione = data.get("dataassunzione")
        datadimissioni = data.get("datadimissioni")

        if dataassunzione and datadimissioni and datadimissioni < dataassunzione:
            raise serializers.ValidationError({
                "datadimissioni": "La data di dimissioni non può essere precedente alla data di assunzione."
            })
        return data


# =============================================================================
# VALUTAZIONE OPERATORE
# =============================================================================

class ValutazioneOperatoreSerializer(serializers.ModelSerializer):
    """
    Serializer per ValutazioneOperatore.
    Include display names per FK.
    """
    fk_hr_display = serializers.CharField(
        source="fk_hr.__str__",
        read_only=True,
    )
    fk_centro_di_lavoro_display = serializers.CharField(
        source="fk_centro_di_lavoro.description",
        read_only=True,
    )
    valutazione_display = serializers.CharField(
        source="get_valutazione_display",
        read_only=True,
    )

    class Meta:
        model = ValutazioneOperatore
        fields = [
            "id",
            "fk_hr",
            "fk_hr_display",
            "fk_centro_di_lavoro",
            "fk_centro_di_lavoro_display",
            "valutazione",
            "valutazione_display",
            "note",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_fk_hr(self, value):
        if not value:
            raise serializers.ValidationError("Il dipendente è obbligatorio.")
        return value

    def validate_fk_centro_di_lavoro(self, value):
        if not value:
            raise serializers.ValidationError("Il centro di lavoro è obbligatorio.")
        return value

    def validate_valutazione(self, value):
        if not value:
            raise serializers.ValidationError("La valutazione è obbligatoria.")
        return value

    def validate(self, data):
        """
        Validazione unicità (fk_hr, fk_centro_di_lavoro).
        Evita duplicati per stesso dipendente/centro.
        """
        fk_hr = data.get("fk_hr")
        fk_centro = data.get("fk_centro_di_lavoro")

        if fk_hr and fk_centro:
            qs = ValutazioneOperatore.objects.filter(
                fk_hr=fk_hr,
                fk_centro_di_lavoro=fk_centro,
            )
            # Escludi l'istanza corrente in caso di update
            if self.instance:
                qs = qs.exclude(pk=self.instance.pk)

            if qs.exists():
                raise serializers.ValidationError({
                    "non_field_errors": [
                        f"Esiste già una valutazione per questo dipendente nel centro '{fk_centro.description}'."
                    ]
                })
        return data
