import pytest

from rest_framework.exceptions import ErrorDetail, ValidationError

from core.__seedwork.domain.exceptions import EntityNotFound
from core.category.domain.entities import Category
from core.category.domain.repositories import CategoryRepository
from core.__seedwork.infra.testing_helpers import make_request
from django_app import container
from django_app.category.api import CategoryResource
from django_app.category.tests.helpers import init_category_resource_all_none


@pytest.mark.django_db
class TestCategoryResourceDeleteMethodInt:

    resource: CategoryResource
    repo: CategoryRepository

    @classmethod
    def setup_class(cls):
        cls.repo = container.Container.repository_category_django_orm()
        cls.resource = init_category_resource_all_none(
            CategoryResource,
            delete_use_case=container.Container.use_case_category_delete_category,
        )

    def test_throw_exception_when_uuid_is_invalid(self):
        request = make_request(http_method='delete')
        with pytest.raises(ValidationError) as assert_exception:
            self.resource.delete(request, 'fake api')
        assert assert_exception.value.detail == {
            'id': [ErrorDetail(string='Must be a valid UUID.', code='invalid')]
        }

    def test_throw_exception_when_category_not_found(self):
        uuid_value = 'af46842e-027d-4c91-b259-3a3642144ba4'
        request = make_request(http_method='delete')
        with pytest.raises(EntityNotFound) as assert_exception:
            self.resource.delete(request, uuid_value)
        error_message = assert_exception.value.args[0]
        assert error_message == "Category not found"

    def test_delete_method(self):
        category = Category.fake().a_category().build()
        self.repo.insert(category)
        request = make_request(http_method='delete')
        response = self.resource.delete(request, category.id)

        assert response.status_code == 204
        with pytest.raises(EntityNotFound) as assert_exception:
            self.repo.find_by_id(category.id)
        error_message = assert_exception.value.args[0]
        assert error_message == "Category not found"