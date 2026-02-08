"""
DRF Serializers for Manuale Procedure API.
"""
from rest_framework import serializers
from .models import SezioneLWG, Procedura, RevisioneProcedura, Modulo, RevisioneModulo


class SezioneLWGSerializer(serializers.ModelSerializer):
    """Serializer for SezioneLWG (read-only, populated by fixture)."""
    class Meta:
        model = SezioneLWG
        fields = ['id', 'lwgsection', 'note', 'created_by', 'created_at']
        read_only_fields = ['id', 'created_by', 'created_at']


class ProceduraListSerializer(serializers.ModelSerializer):
    """Serializer for Procedura list (optimized, includes FK display)."""
    fk_lwgsection_display = serializers.CharField(
        source='fk_lwgsection.lwgsection',
        read_only=True,
        allow_null=True
    )

    class Meta:
        model = Procedura
        fields = [
            'id',
            'identificativo',
            'data_procedura',
            'descrizione',
            'fk_lwgsection',
            'fk_lwgsection_display',
            'is_eliminata',
            'created_at'
        ]
        read_only_fields = ['id', 'created_by', 'created_at']


class ProceduraDetailSerializer(serializers.ModelSerializer):
    """Serializer for Procedura detail."""
    fk_lwgsection_display = serializers.CharField(
        source='fk_lwgsection.lwgsection',
        read_only=True,
        allow_null=True
    )

    class Meta:
        model = Procedura
        fields = [
            'id',
            'identificativo',
            'data_procedura',
            'descrizione',
            'is_eliminata',
            'fk_lwgsection',
            'fk_lwgsection_display',
            'note',
            'created_by',
            'created_at'
        ]
        read_only_fields = ['id', 'created_by', 'created_at']


class ProceduraWriteSerializer(serializers.ModelSerializer):
    """Serializer for Procedura create/update."""
    class Meta:
        model = Procedura
        fields = [
            'identificativo',
            'data_procedura',
            'descrizione',
            'is_eliminata',
            'fk_lwgsection',
            'note'
        ]

    def create(self, validated_data):
        # Auto-set created_by
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['created_by'] = request.user
        return super().create(validated_data)


class RevisioneProceduraSerializer(serializers.ModelSerializer):
    """Serializer for RevisioneProcedura (supports file upload)."""
    fk_procedura_display = serializers.CharField(
        source='fk_procedura.identificativo',
        read_only=True
    )

    class Meta:
        model = RevisioneProcedura
        fields = [
            'id',
            'fk_procedura',
            'fk_procedura_display',
            'n_revisione',
            'data_revisione',
            'documento',
            'note',
            'created_by',
            'created_at'
        ]
        read_only_fields = ['id', 'created_by', 'created_at']

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['created_by'] = request.user
        return super().create(validated_data)


class ModuloSerializer(serializers.ModelSerializer):
    """Serializer for Modulo."""
    fk_procedura_display = serializers.CharField(
        source='fk_procedura.identificativo',
        read_only=True
    )

    class Meta:
        model = Modulo
        fields = [
            'id',
            'fk_procedura',
            'fk_procedura_display',
            'identificativo',
            'data_modulo',
            'descrizione',
            'note',
            'created_by',
            'created_at'
        ]
        read_only_fields = ['id', 'created_by', 'created_at']

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['created_by'] = request.user
        return super().create(validated_data)


class RevisioneModuloSerializer(serializers.ModelSerializer):
    """Serializer for RevisioneModulo (supports file upload)."""
    fk_modulo_display = serializers.CharField(
        source='fk_modulo.identificativo',
        read_only=True
    )

    class Meta:
        model = RevisioneModulo
        fields = [
            'id',
            'fk_modulo',
            'fk_modulo_display',
            'n_revisione',
            'data_revisione',
            'documento',
            'note',
            'created_by',
            'created_at'
        ]
        read_only_fields = ['id', 'created_by', 'created_at']

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['created_by'] = request.user
        return super().create(validated_data)
