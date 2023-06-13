# pylint: disable=protected-access
from typing import TYPE_CHECKING
from unittest.mock import PropertyMock, patch
import pytest
from core.__seedwork.infra.testing_helpers import make_request
from core.category.infra.serializer import CategorySerializer
from django_app.category.tests.helpers import init_category_resource_all_none

from core.category.domain.repositories import CategoryRepository
from django_app import container
from django_app.category.api import CategoryResource
from django_app.category.repositories import CategoryDjangoRepository
from django_app.category.tests.fixture.categories_api_fixtures import CategoryApiFixture, CreateCategoryApiFixture, HttpExpect


@pytest.mark.django_db
class TestCategoryResourcePostMethodInt:

    resource: CategoryResource
    repo: CategoryRepository

    @classmethod
    def setup_class(cls):
        cls.repo = CategoryDjangoRepository()
        cls.resource = init_category_resource_all_none(
            CategoryResource,
            create_use_case=container.Container.use_case_category_create_category
        )

    @pytest.mark.parametrize('http_expect', CreateCategoryApiFixture.arrange_for_save())
    def test_post_method(self, http_expect: HttpExpect):
        request = make_request(http_method='post', send_data=http_expect.request.body)
        response = self.resource.post(request)
        assert response.status_code == 201
        assert CategoryApiFixture.keys_in_category_response() == list(response.data.keys())

        category_created = self.repo.find_by_id(response.data["id"])
        serialized = CategoryResource.category_to_response(category_created)
        assert response.data == serialized

        expected_data = {
            **http_expect.response.body,
            'id': category_created.id,
            'created_at': serialized['created_at'],
        }
        for key, value in expected_data.items():
            assert response.data[key] == value

    @pytest.mark.parametrize('http_expect', CreateCategoryApiFixture.arrange_for_entity_validation_error())
    def test_entity_validation_error(self, http_expect: HttpExpect):
        with (
            patch.object(CategorySerializer, 'is_valid') as mock_is_valid,
            patch.object(
                CategorySerializer,
                'validated_data',
                new_callable=PropertyMock,
                return_value=http_expect.request.body
            ) as mock_validated_data
        ):
            request = make_request(
                http_method='post',
                send_data=http_expect.request.body
            )
            with pytest.raises(http_expect.exception.__class__) as assert_exception:
                self.resource.post(request)
            mock_is_valid.assert_called()
            mock_validated_data.assert_called()
            assert assert_exception.value.error == http_expect.exception.error
