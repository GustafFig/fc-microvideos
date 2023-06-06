# pylint: disable=abstract-method
from rest_framework import ISO_8601, serializers
from core.__seedwork.infra.serializers import ISO_8601, CollectionSerializer


class CategorySerializer(serializers.Serializer):

    id = serializers.UUIDField(read_only=True)
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(required=False, allow_null=True)
    is_active = serializers.BooleanField(required=False)
    created_at = serializers.DateTimeField(read_only=True, format=ISO_8601)


class CategoryCollectionSerializer(CollectionSerializer):  # pylint: disable=abstract-method
    child = CategorySerializer()
