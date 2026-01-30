from rest_framework import serializers
from .models import Articolo, ElencoTest, FaseLavoro, DettaglioFaseLavoro, LavorazioneEsterna


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
