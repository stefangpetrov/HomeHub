from rest_framework import serializers

from .models import Property


class PropertySerializer(serializers.ModelSerializer):

    class Meta:
        model = Property
        fields = [
            "id",
            "title",
            "description",
            "price",
            "area",
            "bedrooms",
            "bathrooms",
            "floor",
            "total_floors",
            "city",
            "address",
            "property_type",
            "status",
            "owner",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "owner",
            "created_at",
            "updated_at",
        ]