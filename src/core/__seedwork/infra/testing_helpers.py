from typing import Any, Dict, Literal
from rest_framework.request import Request as DrfRequest
from rest_framework.test import APIRequestFactory
from django.http.request import HttpRequest

HTTP_VERB = Literal['get', 'post', 'put', 'delete']

def make_request(http_method: HTTP_VERB, url: str = '/', send_data: Any = None) -> DrfRequest:
    request_factory = APIRequestFactory()
    http_method_func = getattr(request_factory, http_method)
    http_request: HttpRequest = http_method_func(url)
    request = DrfRequest(http_request)
    request._full_data = send_data  # pylint: disable=protected-access
    return request


def assert_response_data(response_data: Dict, expected_data: Dict):
    for key, value in expected_data.items():
        assert response_data[key] == value
