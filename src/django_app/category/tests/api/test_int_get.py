#pylint: disable=unexpected-keyword-arg
import pytest

from core.__seedwork.infra.testing_helpers import make_request

from urllib.parse import urlencode

from core.category.domain.entities import Category
from core.category.domain.repositories import CategoryRepository
from django_app import container
from django_app.category.api import CategoryResource
from django_app.category.tests.helpers import init_category_resource_all_none
from django_app.category.tests.fixture.categories_api_fixtures import (
    ListCategoriesApiFixture, SearchExpectation
)


@pytest.mark.django_db
class TestCategoryResourceGetMethodInt:

    resource: CategoryResource
    repo: CategoryRepository

    @classmethod
    def setup_class(cls):
        cls.repo = container.Container.repository_category_django_orm()
        cls.resource = init_category_resource_all_none(
            CategoryResource,
            list_use_case=container.Container.use_case_category_list_category,
        )

    @pytest.mark.parametrize('item', ListCategoriesApiFixture.arrange_incremented_with_created_at())
    def test_execute_using_empty_search_params(self, item: SearchExpectation):
        self.repo.bulk_insert(item.entities)
        self.assert_response(item.send_data, item.expected)

    @pytest.mark.parametrize('item', ListCategoriesApiFixture.arrange_unsorted())
    def test_execute_using_pagination_and_sort_and_filter(self, item: SearchExpectation):
        self.repo.bulk_insert(item.entities)
        self.assert_response(item.send_data, item.expected)

    def assert_response(self, send_data: dict, expected: SearchExpectation.Expected):
        request = make_request(
            http_method='get',
            url=f'/?{urlencode(send_data)}'
        )
        response = self.resource.get(request)

        assert response.status_code == 200
        assert response.data == {
            'data': [self.serialize_category(category)['data'] for category in expected.entities],
            'meta': expected.meta,
        }

    def serialize_category(self, category: Category):
        return CategoryResource.category_to_response(category)
