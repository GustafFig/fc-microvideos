# pylint: disable=abstract-method
from rest_framework import serializers

from core.__seedwork.infra.serializers import (ISO_8601, CollectionSerializer,
                                               ResourceSerializer)


class CategorySerializer(ResourceSerializer):
    id = serializers.UUIDField(read_only=True)
    name = serializers.CharField()
    description = serializers.CharField(required=False, allow_null=True)
    is_active = serializers.BooleanField(required=False)
    created_at = serializers.DateTimeField(read_only=True, format=ISO_8601)


class CategoryCollectionSerializer(CollectionSerializer):
    child = CategorySerializer()
