from collections import namedtuple
from contextlib import contextmanager
from unittest.mock import PropertyMock, patch

from core.category.infra.serializer import CategorySerializer
from django_app.category.tests.fixture.categories_api_fixtures import HttpExpect


@contextmanager
def mock_category_serializer_validators(http_expect: HttpExpect):
    MockSerializer = namedtuple("MockSerializer", ["mock_is_valid", "mock_validated_data"])
    with (
        patch.object(CategorySerializer, 'is_valid') as mock_is_valid,
        patch.object(
            CategorySerializer,
            'validated_data',
            new_callable=PropertyMock,
            return_value=http_expect.request.body
        ) as mock_validated_data
    ):
        yield MockSerializer(mock_is_valid, mock_validated_data)
