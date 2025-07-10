from rest_framework import serializers
from .models import Articolo


class ArticoloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Articolo
        fields = "__all__"
        read_only_fields = ["created_by"]
