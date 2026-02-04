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
    RegistroOreLavoro,
    AreaFormazione,
    CorsoFormazione,
    RegistroFormazione,
    DettaglioRegistroFormazione,
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
    fk_hr_display = serializers.SerializerMethodField()

    def get_fk_hr_display(self, obj):
        return str(obj.fk_hr) if obj.fk_hr else None
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
    fk_hr_display = serializers.SerializerMethodField()

    def get_fk_hr_display(self, obj):
        return str(obj.fk_hr) if obj.fk_hr else None

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


# =============================================================================
# REGISTRO ORE LAVORO
# =============================================================================

class RegistroOreLavoroListSerializer(serializers.ModelSerializer):
    """
    Serializer per lista Registro Ore Lavoro.
    Campi minimi per la tabella lista.
    """
    month_verbose = serializers.SerializerMethodField()

    class Meta:
        model = RegistroOreLavoro
        fields = [
            "id",
            "entry_year",
            "entry_month",
            "month_verbose",
            "ore_lavorabili",
            "ore_lavorate",
        ]

    def get_month_verbose(self, obj):
        return obj.month_verbose()


class RegistroOreLavoroDetailSerializer(serializers.ModelSerializer):
    """
    Serializer per dettaglio Registro Ore Lavoro.
    Include tutti i campi.
    """
    month_verbose = serializers.SerializerMethodField()

    class Meta:
        model = RegistroOreLavoro
        fields = [
            "id",
            "entry_year",
            "entry_month",
            "month_verbose",
            "ore_lavorabili",
            "ore_lavorate",
            "straordinari",
            "ferie_permessi",
            "permessi_speciali",
            "maternità",
            "infortunio",
            "formazione",
            "formazione_neoassunti",
            "malattia",
            "n_infortuni",
            "n_infortuni_itinere",
            "n_malattie_professionali",
            "ore_malattie_professionali",
            "permessi_non_retribuiti",
            "assenze_ingiustificate",
            "note",
        ]
        read_only_fields = ["id"]

    def get_month_verbose(self, obj):
        return obj.month_verbose()


class RegistroOreLavoroWriteSerializer(serializers.ModelSerializer):
    """
    Serializer per create/update Registro Ore Lavoro.
    """

    class Meta:
        model = RegistroOreLavoro
        fields = [
            "entry_year",
            "entry_month",
            "ore_lavorabili",
            "ore_lavorate",
            "straordinari",
            "ferie_permessi",
            "permessi_speciali",
            "maternità",
            "infortunio",
            "formazione",
            "formazione_neoassunti",
            "malattia",
            "n_infortuni",
            "n_infortuni_itinere",
            "n_malattie_professionali",
            "ore_malattie_professionali",
            "permessi_non_retribuiti",
            "assenze_ingiustificate",
            "note",
        ]

    def validate_entry_year(self, value):
        if not value:
            raise serializers.ValidationError("L'anno è obbligatorio.")
        return value

    def validate_entry_month(self, value):
        if not value or value < 1 or value > 12:
            raise serializers.ValidationError(
                "Il mese deve essere compreso tra 1 e 12."
            )
        return value

    def create(self, validated_data):
        """Autopopolamento created_by dall'utente loggato."""
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['created_by'] = request.user
        return super().create(validated_data)


# =============================================================================
# AREA FORMAZIONE
# =============================================================================

class AreaFormazioneSerializer(serializers.ModelSerializer):
    """Serializer per AreaFormazione (Sicurezza, Qualità, ecc.)."""

    class Meta:
        model = AreaFormazione
        fields = ["id", "descrizione", "created_by"]
        read_only_fields = ["id", "created_by"]

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['created_by'] = request.user
        return super().create(validated_data)


# =============================================================================
# CORSO FORMAZIONE
# =============================================================================

class CorsoFormazioneSerializer(serializers.ModelSerializer):
    """Serializer per CorsoFormazione."""
    fk_areaformazione_display = serializers.CharField(
        source="fk_areaformazione.descrizione",
        read_only=True,
    )

    class Meta:
        model = CorsoFormazione
        fields = [
            "id",
            "descrizione",
            "fk_areaformazione",
            "fk_areaformazione_display",
            "validita_mesi",
            "created_by",
        ]
        read_only_fields = ["id", "created_by"]

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['created_by'] = request.user
        return super().create(validated_data)


# =============================================================================
# DETTAGLIO REGISTRO FORMAZIONE
# =============================================================================

class DettaglioRegistroFormazioneSerializer(serializers.ModelSerializer):
    """
    Serializer per DettaglioRegistroFormazione.
    Include scadenza_effettiva calcolata e URL certificato.
    """
    fk_hr_display = serializers.SerializerMethodField()
    scadenza_effettiva = serializers.DateField(read_only=True)
    certificato_url = serializers.SerializerMethodField()

    def get_fk_hr_display(self, obj):
        return str(obj.fk_hr) if obj.fk_hr else None

    class Meta:
        model = DettaglioRegistroFormazione
        fields = [
            "id",
            "fk_registro_formazione",
            "fk_hr",
            "fk_hr_display",
            "ore",
            "note",
            "certificato",
            "certificato_url",
            "presenza",
            "efficace",
            "scadenza_calcolata",
            "scadenza_override",
            "scadenza_effettiva",
            "created_by",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "scadenza_calcolata",
            "scadenza_effettiva",
            "created_by",
            "created_at",
            "updated_at",
        ]

    def get_certificato_url(self, obj):
        """Ritorna URL completa del certificato se presente."""
        if obj.certificato:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.certificato.url)
            return obj.certificato.url
        return None

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['created_by'] = request.user
        return super().create(validated_data)


class DettaglioRegistroFormazioneWriteSerializer(serializers.ModelSerializer):
    """Serializer per create/update DettaglioRegistroFormazione."""

    class Meta:
        model = DettaglioRegistroFormazione
        fields = [
            "fk_registro_formazione",
            "fk_hr",
            "ore",
            "note",
            "certificato",
            "presenza",
            "efficace",
            "scadenza_override",
        ]

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['created_by'] = request.user
        return super().create(validated_data)


# =============================================================================
# REGISTRO FORMAZIONE
# =============================================================================

class RegistroFormazioneListSerializer(serializers.ModelSerializer):
    """
    Serializer per lista dashboard RegistroFormazione.
    Campi minimi per performance.
    num_partecipanti viene popolato via annotate(Count) nel ViewSet.
    """
    corso_descrizione = serializers.CharField(
        source="fk_corso.descrizione",
        read_only=True,
    )
    fornitore_descrizione = serializers.CharField(
        source="fk_fornitore.ragionesociale",
        read_only=True,
        allow_null=True,
    )
    # Campo annotato dal ViewSet - evita N+1
    num_partecipanti = serializers.IntegerField(read_only=True)

    class Meta:
        model = RegistroFormazione
        fields = [
            "id",
            "data_formazione",
            "fk_corso",
            "corso_descrizione",
            "fk_fornitore",
            "fornitore_descrizione",
            "ore",
            "num_partecipanti",
        ]


class RegistroFormazioneDetailSerializer(serializers.ModelSerializer):
    """
    Serializer per dettaglio RegistroFormazione.
    Include la tabella operatori (DettaglioRegistroFormazione).
    """
    corso_descrizione = serializers.CharField(
        source="fk_corso.descrizione",
        read_only=True,
    )
    area_formazione = serializers.CharField(
        source="fk_corso.fk_areaformazione.descrizione",
        read_only=True,
    )
    validita_mesi = serializers.IntegerField(
        source="fk_corso.validita_mesi",
        read_only=True,
    )
    fornitore_descrizione = serializers.CharField(
        source="fk_fornitore.ragionesociale",
        read_only=True,
        allow_null=True,
    )
    dettagli = DettaglioRegistroFormazioneSerializer(many=True, read_only=True)

    class Meta:
        model = RegistroFormazione
        fields = [
            "id",
            "data_formazione",
            "fk_corso",
            "corso_descrizione",
            "area_formazione",
            "validita_mesi",
            "fk_fornitore",
            "fornitore_descrizione",
            "ore",
            "note",
            "created_by",
            "dettagli",
        ]
        read_only_fields = ["id", "created_by"]


class RegistroFormazioneWriteSerializer(serializers.ModelSerializer):
    """
    Serializer per create/update RegistroFormazione.
    Supporta creazione con dettagli annidati opzionali.
    """
    dettagli = DettaglioRegistroFormazioneWriteSerializer(
        many=True, required=False
    )

    class Meta:
        model = RegistroFormazione
        fields = [
            "data_formazione",
            "fk_corso",
            "fk_fornitore",
            "ore",
            "note",
            "dettagli",
        ]

    def create(self, validated_data):
        dettagli_data = validated_data.pop('dettagli', [])
        request = self.context.get('request')

        if request and hasattr(request, 'user'):
            validated_data['created_by'] = request.user

        registro = RegistroFormazione.objects.create(**validated_data)

        # Crea dettagli annidati
        for dettaglio_data in dettagli_data:
            if request and hasattr(request, 'user'):
                dettaglio_data['created_by'] = request.user
            DettaglioRegistroFormazione.objects.create(
                fk_registro_formazione=registro,
                **dettaglio_data
            )

        return registro

    def update(self, instance, validated_data):
        # Non aggiorniamo dettagli in update, vanno gestiti separatamente
        validated_data.pop('dettagli', None)
        return super().update(instance, validated_data)


# =============================================================================
# DETTAGLIO FORMAZIONE - RECORD CORRENTE (per query speciale)
# =============================================================================

class DettaglioFormazioneCurrentSerializer(serializers.ModelSerializer):
    """
    Serializer per la query "record corrente" per coppia (hr, corso).
    Include info complete su hr, corso e scadenza.
    """
    fk_hr_display = serializers.SerializerMethodField()
    corso_descrizione = serializers.CharField(
        source="fk_registro_formazione.fk_corso.descrizione",
        read_only=True,
    )
    corso_id = serializers.IntegerField(
        source="fk_registro_formazione.fk_corso.id",
        read_only=True,
    )
    data_formazione = serializers.DateField(
        source="fk_registro_formazione.data_formazione",
        read_only=True,
    )
    scadenza_effettiva = serializers.DateField(read_only=True)
    certificato_url = serializers.SerializerMethodField()

    class Meta:
        model = DettaglioRegistroFormazione
        fields = [
            "id",
            "fk_hr",
            "fk_hr_display",
            "corso_id",
            "corso_descrizione",
            "data_formazione",
            "scadenza_calcolata",
            "scadenza_override",
            "scadenza_effettiva",
            "efficace",
            "certificato_url",
        ]

    def get_fk_hr_display(self, obj):
        return str(obj.fk_hr) if obj.fk_hr else None

    def get_certificato_url(self, obj):
        if obj.certificato:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.certificato.url)
            return obj.certificato.url
        return None
