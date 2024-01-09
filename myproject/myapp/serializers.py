from rest_framework import serializers

from .models import Item


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = "__all__"


class ItemListCreateSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source="created_by.id")

    class Meta:
        model = Item
        fields = "__all__"
