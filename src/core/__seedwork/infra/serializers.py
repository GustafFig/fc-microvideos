from core.__seedwork.application.dto import PaginationOutput
from rest_framework import serializers


ISO_8601 = '%Y-%m-%dT%H:%M:%S'


class UUIDSerializer(serializers.Serializer): # pylint: disable=abstract-method
    id = serializers.UUIDField()


class PaginationSerializer(serializers.Serializer): # pylint: disable=abstract-method
    total = serializers.IntegerField()
    page = serializers.IntegerField()
    per_page = serializers.IntegerField()
    last_page = serializers.IntegerField()


class CollectionSerializer(serializers.ListSerializer):  # pylint: disable=abstract-method
    pagination: PaginationOutput
    many = False

    def __init__(self, instance: PaginationOutput = None, **kwargs):
        if isinstance(instance, PaginationOutput):
            kwargs['instance'] = instance.items
            self.pagination = instance
        else:
            raise TypeError('instance must be a PaginationOutput')
        super().__init__(**kwargs)

    def to_representation(self, data):
        return {
            'data': [
                # todo - verificar se tem data ou não
                self.child.to_representation(item) for item in data
            ],
            'meta': PaginationSerializer(self.pagination).data
        }
