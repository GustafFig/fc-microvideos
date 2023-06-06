# pylint: disable=protected-access
from typing import TYPE_CHECKING
import pytest
from django_app.category.tests.helpers import init_category_resource_all_none
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory

from core.category.domain.repositories import CategoryRepository
from django_app import container
from django_app.category.api import CategoryResource
from django_app.category.repositories import CategoryDjangoRepository
from django_app.category.tests.fixture.categories_api_fixtures import CategoryApiFixture, HttpExpect


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

    @pytest.fixture()
    def req(self):
        request_factory = APIRequestFactory()
        _request = request_factory.get('/categories')
        return Request(_request)

    @pytest.mark.parametrize('http_expect', CategoryApiFixture.arrange_for_save())
    def test_post_method(self, http_expect: HttpExpect, req):
        req._full_data = http_expect.request.body
        response = self.resource.post(req)
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
