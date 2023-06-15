import pytest
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

    @pytest.mark.parametrize('http_expect', CreateCategoryApiFixture.arrange_for_save())
    def test_post(self, http_expect: HttpExpect):
        client_http = APIClient()
        response: Response = client_http.post(
            '/categories/', data=http_expect.request.body, format="json"
        )
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
