import pytest
from rest_framework.renderers import JSONRenderer
from rest_framework.test import APIClient

from core.__seedwork.domain.value_objects import UniqueEntityId
from core.category.domain.entities import Category
from core.category.domain.repositories import CategoryRepository
from django_app import container
from django_app.category.api import CategoryResource
from django_app.category.tests.api.helpers import \
    mock_category_serializer_validators
from django_app.category.tests.fixture.categories_api_fixtures import (
    HttpExpect, UpdateCategoryApiFixture)


@pytest.mark.group('e2e')
@pytest.mark.django_db
class TestCategoryResourcePutMethodE2E:

    client_http: APIClient
    repo: CategoryRepository

    @classmethod
    def setup_class(cls):
        cls.repo = container.repository_category_django_orm()
        cls.client_http = APIClient()

    @pytest.mark.parametrize('http_expect', UpdateCategoryApiFixture.arrange_for_invalid_requests())
    def test_invalid_request(self, http_expect: HttpExpect):
        uuid_value = 'af46842e-027d-4c91-b259-3a3642144ba4'
        response = self.client_http.put(
            f'/categories/{uuid_value}/', data=http_expect.request.body, format="json",
        )
        assert response.status_code == 422
        assert response.content == JSONRenderer().render(http_expect.exception.detail)

    @pytest.mark.parametrize(
        'http_expect', UpdateCategoryApiFixture.arrange_for_entity_validation_error()
    )
    def test_entity_validation_error(self, http_expect: HttpExpect):
        category = Category.fake().a_category().build()
        self.repo.insert(category)
        with mock_category_serializer_validators(http_expect) as mockSerializer:
            response = self.client_http.put(
                f'/categories/{category.id}/', data=http_expect.request.body, format="json",
            )
        mockSerializer.mock_is_valid.assert_called()
        mockSerializer.mock_validated_data.assert_called()
        assert response.status_code == 422
        assert response.content == JSONRenderer().render(http_expect.exception.error)

    def test_throw_exception_when_category_not_found(self):
        uuid = UniqueEntityId().id
        category = Category.fake().a_category().build()
        data = {
            "name": category.name,
            "description": category.description,
        }
        response = self.client_http.put(
            f'/categories/{uuid}/', data=data, format="json",
        )
        # assert response.status_code == 404
        assert response.content == JSONRenderer().render({"message": "Category not found"})

    @pytest.mark.parametrize('http_expect', UpdateCategoryApiFixture.arrange_for_save())
    def test_put_method(self, http_expect: HttpExpect):
        category = Category.fake().a_category().build()
        self.repo.insert(category)
        response = self.client_http.put(
            f'/categories/{category.id}/', data=http_expect.request.body, format="json",
        )

        assert response.status_code == 200
        expected_keys = UpdateCategoryApiFixture.keys_in_category_response()
        assert expected_keys == list(response.data['data'].keys())

        response_data = response.data["data"]
        category_updated = self.repo.find_by_id(response_data['id'])
        serialized = CategoryResource.category_to_response(category_updated)

        assert response.data == serialized
        assert response.content == JSONRenderer().render(serialized)
        assert response.data == {
            "data": {
                **http_expect.response.body,
                'id': category_updated.id,
                'created_at': serialized["data"]['created_at'],
            }
        }
