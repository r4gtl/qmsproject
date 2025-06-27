from rest_framework import serializers
from .models import Cliente, Fornitore


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = "__all__"


class FornitoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fornitore
        fields = "__all__"
