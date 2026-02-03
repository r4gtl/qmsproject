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
    Safety_Role,
    HR_Safety,
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
            "created_by",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_by", "created_at", "updated_at"]

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

    def create(self, validated_data):
        """Autopopolamento created_by dall'utente loggato."""
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['created_by'] = request.user
        return super().create(validated_data)


# =============================================================================
# SAFETY ROLE (INCARICHI SICUREZZA)
# =============================================================================

class SafetyRoleSerializer(serializers.ModelSerializer):
    """Serializer per Safety_Role (Incarichi Sicurezza)."""

    class Meta:
        model = Safety_Role
        fields = ["id", "descrizione", "note", "created_at"]
        read_only_fields = ["id", "created_at", "created_by"]

    def create(self, validated_data):
        """Autopopolamento created_by dall'utente loggato."""
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['created_by'] = request.user
        return super().create(validated_data)


# =============================================================================
# HR SAFETY (INCARICHI SICUREZZA PER DIPENDENTE)
# =============================================================================

class HRSafetySerializer(serializers.ModelSerializer):
    """
    Serializer per HR_Safety (Incarichi Sicurezza per dipendente).
    Include validazione overlap date per stesso fk_hr + fk_safety_role.

    SEMANTICA INTERVALLI:
    Gli intervalli sono trattati come [data_inizio, data_fine) (semi-aperti):
    - data_inizio: inclusa
    - data_fine: esclusa (se NULL = +infinito)
    Questo permette incarichi consecutivi dove fine(A) = inizio(B).
    Esempio: [2024-01-01, 2024-01-10) seguito da [2024-01-10, 2024-02-01) è valido.

    INTERVALLI VUOTI:
    Non sono permessi incarichi con data_fine == data_inizio (0 giorni).
    Se data_fine è valorizzata, deve essere STRICT > data_inizio.
    """
    fk_safety_role_display = serializers.CharField(
        source="fk_safety_role.descrizione",
        read_only=True,
    )
    fk_hr_display = serializers.CharField(
        source="fk_hr.__str__",
        read_only=True,
    )

    class Meta:
        model = HR_Safety
        fields = [
            "id",
            "fk_hr",
            "fk_hr_display",
            "fk_safety_role",
            "fk_safety_role_display",
            "data_inizio_incarico",
            "data_fine_incarico",
            "note",
            "created_at",
        ]
        read_only_fields = ["id", "created_at", "created_by"]

    def validate(self, data):
        """
        Validazioni:
        1) Se data_fine_incarico presente: >= data_inizio_incarico
        2) Nessun overlap con incarichi esistenti per stesso hr+role

        PATCH Robustness:
        In caso di update parziale, combina data con instance esistente
        per validazione completa.

        Overlap Rule:
        start_new < end_old AND start_old < end_new
        Questo permette incarichi consecutivi con fine=inizio (NO overlap).
        """
        # PATCH robustness: recupera valori da instance se non in data
        if self.instance:
            data_inizio = data.get("data_inizio_incarico", self.instance.data_inizio_incarico)
            data_fine = data.get("data_fine_incarico", self.instance.data_fine_incarico)
            fk_hr = data.get("fk_hr", self.instance.fk_hr_id)
            fk_safety_role = data.get("fk_safety_role", self.instance.fk_safety_role_id)
        else:
            data_inizio = data.get("data_inizio_incarico")
            data_fine = data.get("data_fine_incarico")
            fk_hr = data.get("fk_hr")
            fk_safety_role = data.get("fk_safety_role")

        # Validazione 1: data_fine > data_inizio (STRICT, blocca intervalli vuoti)
        if data_fine is not None and data_inizio is not None:
            if data_fine <= data_inizio:
                raise serializers.ValidationError({
                    "data_fine_incarico": "La data fine deve essere maggiore (>) della data inizio. Intervalli vuoti (fine = inizio) non sono permessi."
                })

        # Validazione 2: overlap
        # Serve almeno fk_hr, fk_safety_role, data_inizio per validare
        if fk_hr and fk_safety_role and data_inizio:
            from datetime import date as date_type

            # Recupera incarichi esistenti per stesso hr + role
            qs = HR_Safety.objects.filter(
                fk_hr=fk_hr,
                fk_safety_role=fk_safety_role,
            )

            # Escludi istanza corrente in caso di update
            if self.instance:
                qs = qs.exclude(pk=self.instance.pk)

            # Controlla overlap con ciascun incarico esistente
            for existing in qs:
                # Intervallo esistente: [start_old, end_old)
                start_old = existing.data_inizio_incarico
                end_old = existing.data_fine_incarico

                # Intervallo nuovo: [start_new, end_new)
                start_new = data_inizio
                end_new = data_fine

                # Tratta None come date.max per evitare confronti diretti con None
                # None rappresenta +infinito (incarico aperto)
                end_old_cmp = end_old if end_old is not None else date_type.max
                end_new_cmp = end_new if end_new is not None else date_type.max

                # Overlap rule: start_new < end_old AND start_old < end_new
                # Semantica [start, end): end escluso, quindi fine(A)=inizio(B) è OK
                if start_new < end_old_cmp and start_old < end_new_cmp:
                    raise serializers.ValidationError({
                        "non_field_errors": [
                            "Esiste già un incarico sovrapposto per questo dipendente e ruolo."
                        ]
                    })

        return data

    def create(self, validated_data):
        """Autopopolamento created_by dall'utente loggato."""
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['created_by'] = request.user
        return super().create(validated_data)
