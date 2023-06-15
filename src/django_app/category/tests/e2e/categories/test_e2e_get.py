from urllib.parse import urlencode
import pytest
from rest_framework.renderers import JSONRenderer
from rest_framework.test import APIClient

from core.category.domain.entities import Category
from core.category.domain.repositories import CategoryRepository
from django_app.category.tests.fixture.categories_api_fixtures import ListCategoriesApiFixture, SearchExpectation
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

    @pytest.mark.parametrize('item', ListCategoriesApiFixture.arrange_incremented_with_created_at())
    def test_execute_using_empty_search_params(self, item: SearchExpectation):
        self.repo.bulk_insert(item.entities)
        self.assert_response(item.send_data, item.expected)

    @pytest.mark.parametrize('item', ListCategoriesApiFixture.arrange_unsorted())
    def test_execute_using_pagination_and_sort_and_filter(self, item: SearchExpectation):
        self.repo.bulk_insert(item.entities)
        self.assert_response(item.send_data, item.expected)

    def assert_response(self, send_data: dict, expected: SearchExpectation.Expected):
        response = self.client_http.get(f'/categories/?{urlencode(send_data)}', format='json')

        assert response.status_code == 200
        assert response.data == {
            'data': [self.serialize_category(category) for category in expected.entities],
            'meta': expected.meta,
        }

    def serialize_category(self, category: Category):
        return CategoryResource.category_to_response(category)['data']
