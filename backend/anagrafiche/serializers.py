from rest_framework import serializers
from .models import Cliente, Fornitore, LwgFornitore


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = "__all__"
        read_only_fields = ["created_by", "company"]


class FornitoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fornitore
        fields = "__all__"
        read_only_fields = ["created_by", "company"]
        latitude = serializers.FloatField(required=False, allow_null=True)
        longitude = serializers.FloatField(required=False, allow_null=True)


class LwgFornitoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = LwgFornitore
        fields = "__all__"
        read_only_fields = ["created_by", "company"]        