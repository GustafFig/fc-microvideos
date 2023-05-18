from dataclasses import asdict, dataclass
from typing import Callable

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.status import HTTP_201_CREATED

from core.category.application.usecase import (
    CreateCategoryUseCase,
    GetCategoryUseCase,
    ListCategoriesUseCase
)


@dataclass(slots=True)
class CategoryResource(APIView):

    create_use_case: Callable[[], CreateCategoryUseCase]
    get_use_case: Callable[[], GetCategoryUseCase]
    list_use_case: Callable[[], ListCategoriesUseCase]

    def post(self, req: Request):
        input_param = CreateCategoryUseCase.Input(**req.data)
        output = self.create_use_case()(input_param)
        return Response(asdict(output), status=HTTP_201_CREATED)

    def get(self, req: Request):
        input_param = ListCategoriesUseCase.Input(**req.query_params.dict())
        output = self.list_use_case()(input_param)
        return Response(asdict(output))
