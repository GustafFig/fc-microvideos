# pylint: disable=protected-access
import datetime
import unittest
from collections import namedtuple
from unittest.mock import MagicMock, Mock, patch

from core.__seedwork.infra.serializers import ISO_8601
from core.__seedwork.infra.testing_helpers import make_request
from core.category.application.dto import CategoryOutput
from core.category.application.usecase import (CreateCategoryUseCase,
                                               DeleteCategoryUseCase,
                                               GetCategoryUseCase,
                                               ListCategoriesUseCase,
                                               UpdateCategoryUseCase)
from core.category.infra.serializer import CategorySerializer
from django_app.category.api import CategoryResource
from django_app.category.tests.helpers import init_category_resource_all_none


class StubCategorySerializer:

    validated_data = None

    def is_valid(self, raise_exception: bool):
        pass


class TestCategoryResourceUnit(unittest.TestCase):

    @patch.object(CategorySerializer, '__new__')
    def test_category_to_response_method(self, mock_serializer):
        mock_serializer.return_value = namedtuple('Faker', ['data'])(data='test')
        data = CategoryResource.category_to_response('output')
        mock_serializer.assert_called_with(
            CategorySerializer,
            instance='output'
        )
        self.assertEqual(data, 'test')

    @patch.object(CategoryResource, 'category_to_response')
    def test_post_method(self, mock_category_to_response):
        expected_response = {
            'id': 'af46842e-027d-4c91-b259-3a3642144ba4',
            'name': 'Movie',
            'description': None,
            'is_active': True,
            'created_at': datetime.datetime.now()
        }
        return_value = CreateCategoryUseCase.Output(
            **expected_response,
        )
        mock_create_use_case = Mock(CreateCategoryUseCase, return_value=return_value)
        resource = init_category_resource_all_none(
            CategoryResource,
            create_use_case=lambda: mock_create_use_case,
        )

        send_data = {'name': 'Movie'}
        request = make_request('post', '/categories', send_data)

        stub_serializer = StubCategorySerializer()
        mock_category_to_response.return_value = expected_response
        with patch.object(
            CategorySerializer, '__new__', return_value=stub_serializer
        ) as mock_serializer:
            stub_serializer.validated_data = send_data
            stub_serializer.is_valid = MagicMock()
            response = resource.post(request)

        mock_serializer.assert_called_once_with(CategorySerializer, data=send_data)
        stub_serializer.is_valid.assert_called_with(raise_exception=True)
        mock_category_to_response.assert_called_with(
            mock_create_use_case.return_value
        )
        mock_create_use_case.assert_called_once_with(
            CreateCategoryUseCase.Input(name="Movie")
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, {**expected_response})

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
        resource = init_category_resource_all_none(
            CategoryResource,
            list_use_case=lambda: mock_list_use_case,
        )

        send_data = {'name': 'Movie'}
        request = make_request(
            'get',
            '/?page=1&per_page=1&sort=name&sort_dir=asc&filters=test',
            send_data
        )
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

    @patch.object(CategoryResource, 'validate_id')
    def test_get_method(self, mock_validate_id):
        return_value = GetCategoryUseCase.Output(
            id="fakeid",
            name="Movie",
            description=None,
            is_active=None,
            created_at=datetime.datetime.now().strftime(ISO_8601),
        )
        mock_get_use_case = Mock(GetCategoryUseCase, return_value=return_value)
        resource = init_category_resource_all_none(
            CategoryResource,
            get_use_case=lambda: mock_get_use_case
        )

        request = make_request('get', '/categories/fakeid')
        response = resource.get(request, id="fakeid")
        mock_get_use_case.assert_called_once_with(
            GetCategoryUseCase.Input(id="fakeid")
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {
            "data": {
                "id": "fakeid",
                "name": "Movie",
                "description": None,
                "is_active": None,
                "created_at": mock_get_use_case.return_value.created_at,
            }
        })

        mock_list_use_case = Mock()

        request = make_request("get", '/categories/fakeid')
        resource = init_category_resource_all_none(
            CategoryResource,
            list_use_case=mock_list_use_case,
        )
        resource.get_object = Mock()

        resource.get(request, id="fakeid")

        self.assertEqual(mock_list_use_case.call_count, 0)
        resource.get_object.assert_called_once_with(id="fakeid")
        mock_validate_id.assert_called_once_with('fakeid')

    @patch.object(CategoryResource, 'validate_id')
    def test_update_method(self, mock_validate_id):
        send_data = {
            "name": "Movie",
            "description": "description",
            "is_active": True,
        }
        return_value = UpdateCategoryUseCase.Output(
            id="fakeid",
            name="Movie",
            description=send_data["description"],
            is_active=send_data["is_active"],
            created_at=datetime.datetime.now().strftime(ISO_8601),
        )
        mock_update_use_case = Mock(UpdateCategoryUseCase, return_value=return_value)
        resource = init_category_resource_all_none(
            CategoryResource,
            update_use_case=lambda: mock_update_use_case
        )

        request = make_request('put', '/categories/fakeid', send_data)
        response = resource.put(request, id="fakeid")
        mock_validate_id.assert_called_once_with('fakeid')
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
            "data": {
                "id": "fakeid",
                "name": send_data["name"],
                "description": send_data["description"],
                "is_active": send_data["is_active"],
                "created_at": mock_update_use_case.return_value.created_at,
            }
        })

    @patch.object(CategoryResource, 'validate_id')
    def test_delete_method(self, mock_validate_id):
        return_value = DeleteCategoryUseCase.Output()
        mock_delete_use_case = Mock(DeleteCategoryUseCase, return_value=return_value)
        resource = init_category_resource_all_none(
            CategoryResource,
            delete_use_case=lambda: mock_delete_use_case
        )

        request = make_request('delete', '/categories/fakeid')
        response = resource.delete(request, id="fakeid")
        mock_validate_id.assert_called_once_with('fakeid')
        mock_delete_use_case.assert_called_once_with(
            DeleteCategoryUseCase.Input(id="fakeid")
        )
        self.assertEqual(response.status_code, 204)
