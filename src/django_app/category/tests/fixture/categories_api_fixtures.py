from dataclasses import dataclass
from typing import Any

import pytest


@dataclass
class Request:
    body: Any


@dataclass
class Response:
    body: Any


@dataclass
class HttpExpect:
    request: Request
    response: Response


class CategoryApiFixture:

    @staticmethod
    def keys_in_category_response():
        return ["id", "name", "description", "is_active", "created_at"]

    @staticmethod
    def arrange_for_save():
        data = [
            HttpExpect(
                request=Request(body={'name': "Movie1"}),
                response=Response(body={
                    'description': None,
                    'is_active': True,
                })
            ),
            HttpExpect(
                request=Request(body={
                    'name': "Movie1",
                    'description': "some description",
                }),
                response=Response(body={
                    'is_active': True,
                })
            )
        ]
        return [pytest.param(item, id=str(item.request.body)) for item in data]
