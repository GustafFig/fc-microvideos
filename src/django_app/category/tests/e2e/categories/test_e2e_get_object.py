import pytest
from rest_framework.renderers import JSONRenderer
from rest_framework.test import APIClient

from core.__seedwork.domain.value_objects import UniqueEntityId
from core.category.domain.entities import Category
from core.category.domain.repositories import CategoryRepository
from django_app.category.api import CategoryResource
from django_app import container


@pytest.mark.group('e2e')
@pytest.mark.django_db
class TestCategoryResourceGetE2E:

    client_http: APIClient
    repo: CategoryRepository

    @classmethod
    def setup_class(cls):
        cls.repo = container.repository_category_django_orm()
        cls.client_http = APIClient()

    def test_invalid_request(self):
        arrange = [
            {
                'id': UniqueEntityId().id,
                'expected': {
                    'status_code': 404,
                    'response': {
                        'message': "Category not found"
                    }
                }
            },
            {
                'id': 'fake id',
                'expected': {
                    'status_code': 422,
                    'response': {
                        'id': ['Must be a valid UUID.']
                    }
                }
            }
        ]

        for item in arrange:
            response = self.client_http.get(
                f'/categories/{item["id"]}/', data={}, format="json"
            )
            assert response.status_code == item["expected"]["status_code"]
            assert response.content == JSONRenderer().render(item["expected"]["response"])

    def test_get_method(self):
        category = Category.fake().a_category().build()
        self.repo.insert(category)
        response = self.client_http.get(
            f'/categories/{category.id}/', format="json",
        )
        assert response.status_code == 200
        json_serialized = CategoryResource.category_to_response(category)
        assert response.content == JSONRenderer().render(json_serialized)
