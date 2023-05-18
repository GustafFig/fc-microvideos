# pylint: disable=protected-access)
import datetime
import unittest
from unittest.mock import Mock

from rest_framework.test import APIRequestFactory
from rest_framework.request import Request

from core.category.application.usecase import (
    CreateCategoryUseCase,
    DeleteCategoryUseCase,
    GetCategoryUseCase,
    ListCategoriesUseCase,
    UpdateCategoryUseCase,
)
from core.category.application.dto import CategoryOutput
from django_app.category.api import CategoryResource


class TestCategoryResourceUnit(unittest.TestCase):

    def test_post_method(self):
        return_value = CreateCategoryUseCase.Output(
            id="fake id",
            name="Movie",
            description=None,
            is_active=None,
            created_at=datetime.datetime.now(),
        )
        mock_create_use_case = Mock(CreateCategoryUseCase, return_value=return_value)
        resource = self.__resource_tests(
            create_use_case=lambda: mock_create_use_case,
            list_use_case=Mock(),
            get_use_case=Mock(),
        )

        send_data = {'name': 'Movie'}
        _req = APIRequestFactory().post('/categories')
        request = Request(_req)
        request._full_data = send_data
        response = resource.post(request)
        mock_create_use_case.assert_called_once_with(
            CreateCategoryUseCase.Input(name="Movie")
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, {
            "id": "fake id",
            "name": "Movie",
            "description": None,
            "is_active": None,
            "created_at": mock_create_use_case.return_value.created_at,
        })

    def test_list_method(self):
        return_value = ListCategoriesUseCase.Output(
            items=[
                CategoryOutput(
                    id='af46842e-027d-4c91-b259-3a3642144ba4',
                    name='Movie',
                    description=None,
                    is_active=True,
                    created_at=datetime.datetime.now()
                )
            ],
            total=1,
            page=1,
            per_page=2,
            last_page=1
        )
        mock_list_use_case = Mock(ListCategoriesUseCase, return_value=return_value)
        resource = self.__resource_tests(
            list_use_case=lambda: mock_list_use_case,
        )

        send_data = {'name': 'Movie'}
        _req = APIRequestFactory().get('/?page=1&per_page=1&sort=name&sort_dir=asc&filters=test')
        request = Request(_req)
        request._full_data = send_data
        response = resource.get(request)
        mock_list_use_case.assert_called_once_with(
            ListCategoriesUseCase.Input(
                page="1",
                per_page="1",
                sort="name",
                sort_dir="asc",
                filters="test",
            )
        )
        self.assertEqual(response.status_code, 200)

    def test_get_method(self):
        return_value = GetCategoryUseCase.Output(
            id="fakeid",
            name="Movie",
            description=None,
            is_active=None,
            created_at=datetime.datetime.now(),
        )
        mock_get_use_case = Mock(GetCategoryUseCase, return_value=return_value)
        resource = self.__resource_tests(get_use_case=lambda: mock_get_use_case)

        _req = APIRequestFactory().get('/categories/fakeid')
        request = Request(_req)
        response = resource.get(request, id="fakeid")
        mock_get_use_case.assert_called_once_with(
            GetCategoryUseCase.Input(id="fakeid")
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {
            "id": "fakeid",
            "name": "Movie",
            "description": None,
            "is_active": None,
            "created_at": mock_get_use_case.return_value.created_at,
        })

        mock_list_use_case = Mock()

        _req = APIRequestFactory().get('/categories/fakeid')
        request = Request(_req)
        resource = self.__resource_tests(
            list_use_case=mock_list_use_case,
        )
        resource.get_object = Mock()

        resource.get(request, id="fakeid")

        self.assertEqual(mock_list_use_case.call_count, 0)
        resource.get_object.assert_called_once_with(id="fakeid")

    def test_update_method(self):
        send_data = {
            "name": "Movie",
            "description": "description",
            "is_active": "is_active",
        }
        return_value = UpdateCategoryUseCase.Output(
            id="fakeid",
            name="Movie",
            description=send_data["description"],
            is_active=send_data["is_active"],
            created_at=datetime.datetime.now(),
        )
        mock_update_use_case = Mock(UpdateCategoryUseCase, return_value=return_value)
        resource = self.__resource_tests(update_use_case=lambda: mock_update_use_case)

        _req = APIRequestFactory().put('/categories/fakeid', send_data)
        request = Request(_req)
        request._full_data = send_data
        response = resource.put(request, id="fakeid")
        mock_update_use_case.assert_called_once_with(
            UpdateCategoryUseCase.Input(
                id="fakeid",
                name=send_data["name"],
                description=send_data["description"],
                is_active=send_data["is_active"],
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {
            "id": "fakeid",
            "name": send_data["name"],
            "description": send_data["description"],
            "is_active": send_data["is_active"],
            "created_at": mock_update_use_case.return_value.created_at,
        })

    def test_delete_method(self):
        return_value = DeleteCategoryUseCase.Output()
        mock_delete_use_case = Mock(DeleteCategoryUseCase, return_value=return_value)
        resource = self.__resource_tests(delete_use_case=lambda: mock_delete_use_case)

        _req = APIRequestFactory().delete('/categories/fakeid')
        request = Request(_req)
        response = resource.delete(request, id="fakeid")
        mock_delete_use_case.assert_called_once_with(
            DeleteCategoryUseCase.Input(id="fakeid")
        )
        self.assertEqual(response.status_code, 204)

    def __resource_tests(self, **kwargs):
        default = {
            "create_use_case": None,
            "list_use_case": None,
            "get_use_case": None,
            "update_use_case": None,
            "delete_use_case": None,
        } | kwargs
        return CategoryResource(**default)
