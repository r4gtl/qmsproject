from rest_framework import serializers
from .models import TipoAnimale, TipoGrezzo


class TipoAnimaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoAnimale
        fields = ["id", "descrizione"]


class TipoGrezzoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoGrezzo
        fields = ["id", "descrizione"]
