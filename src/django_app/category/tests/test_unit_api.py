import datetime
import unittest
from unittest.mock import Mock
from core.category.application.usecase import CreateCategoryUseCase

from django_app.category.api import CategoryResource

from rest_framework.test import APIRequestFactory
from rest_framework.request import Request


class TestCategoryResourceUnit(unittest.TestCase):

    def test_post_method(self):
        return_value = CreateCategoryUseCase.Output(
            id="fake id",
            name="Movie",
            description=None,
            is_active=None,
            created_at=datetime.datetime.now(),
        )
        create_category_use_case = Mock(CreateCategoryUseCase, return_value=return_value)
        resource = CategoryResource(
            create_use_case=lambda: create_category_use_case,
            list_use_case=Mock(),
            get_use_case=Mock(),
        )

        send_data = {'name': 'Movie'}
        _req = APIRequestFactory().post('/categories')
        request = Request(_req)
        request._full_data = send_data
        response = resource.post(request)
        create_category_use_case.assert_called_once_with(
            CreateCategoryUseCase.Input(name="Movie")
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, {
            "id": "fake id",
            "name": "Movie",
            "description": None,
            "is_active": None,
            "created_at": create_category_use_case.return_value.created_at,
        })
