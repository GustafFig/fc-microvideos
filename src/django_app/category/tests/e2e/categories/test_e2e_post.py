import pytest
from core.__seedwork.infra.testing_helpers import make_request
from django_app.category.tests.api.helpers import mock_category_serializer_validators
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.test import APIClient

from core.category.domain.repositories import CategoryRepository
from django_app import container
from django_app.category.api import CategoryResource
from django_app.category.tests.fixture.categories_api_fixtures import CreateCategoryApiFixture, HttpExpect


@pytest.mark.group('e2e')
@pytest.mark.django_db
class TestCategoriesPostE2E:

    client_http: APIClient
    category_repository: CategoryRepository

    @classmethod
    def setup_class(cls):
        cls.client_http = APIClient()
        cls.category_repository = container.repository_category_django_orm()

    def make_requisition(self, data) -> Response:
        return self.client_http.post('/categories/', data=data, format="json")

    @pytest.mark.parametrize('http_expect', CreateCategoryApiFixture.arrange_for_invalid_requests())
    def test_invalid_request(self, http_expect: HttpExpect):
        response = self.make_requisition(http_expect.request.body)
        assert response.status_code == 422
        assert response.content == JSONRenderer().render(http_expect.exception.detail)

    @pytest.mark.parametrize(
        'http_expect', CreateCategoryApiFixture.arrange_for_entity_validation_error()
    )
    def test_entity_validation_error(self, http_expect: HttpExpect):
        """
        Remove the http validation, that is previous domain validation
        """
        with mock_category_serializer_validators(http_expect) as mockSerializer:
            response = self.make_requisition(http_expect.request.body)
        mockSerializer.mock_is_valid.assert_called()
        mockSerializer.mock_validated_data.assert_called()
        assert response.status_code == 422
        assert response.content == JSONRenderer().render(http_expect.exception.error)

    @pytest.mark.parametrize('http_expect', CreateCategoryApiFixture.arrange_for_save())
    def test_post(self, http_expect: HttpExpect):
        response = self.make_requisition(http_expect.request.body)

        assert response.status_code == 201
        assert "data" in response.data
        data = response.data["data"]
        expected_keys = CreateCategoryApiFixture.keys_in_category_response()
        assert expected_keys == list(data.keys())
        category_created = self.category_repository.find_by_id(data["id"])
        serialized = CategoryResource.category_to_response(category_created)
        assert response.content == JSONRenderer().render(serialized)
        assert data == {
            **http_expect.response.body,
            "id": category_created.id,
            "created_at": serialized["data"]["created_at"],
        }
