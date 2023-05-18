  # pylint: disable=redefined-builtin
  # pylint: disable=invalid-name
from dataclasses import asdict, dataclass
from typing import Callable, Optional

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT

from core.category.application.usecase import (
    CreateCategoryUseCase,
    DeleteCategoryUseCase,
    GetCategoryUseCase,
    ListCategoriesUseCase,
    UpdateCategoryUseCase
)


@dataclass(slots=True)
class CategoryResource(APIView):

    create_use_case: Optional[Callable[[], CreateCategoryUseCase]] = None
    list_use_case: Optional[Callable[[], ListCategoriesUseCase]] = None
    get_use_case: Optional[Callable[[], GetCategoryUseCase]] = None
    update_use_case: Optional[Callable[[], UpdateCategoryUseCase]] = None
    delete_use_case: Optional[Callable[[], DeleteCategoryUseCase]] = None

    def post(self, req: Request):
        input_param = CreateCategoryUseCase.Input(**req.data)
        output = self.create_use_case()(input_param)
        return Response(asdict(output), status=HTTP_201_CREATED)

    def get(self, req: Request, id: str=None):
        if id:
            return self.get_object(id=id)
        input_param = ListCategoriesUseCase.Input(**req.query_params.dict())
        output = self.list_use_case()(input_param)
        return Response(asdict(output))

    def get_object(self, id: str):
        input_param = GetCategoryUseCase.Input(id=id)
        output = self.get_use_case()(input_param)
        return Response(asdict(output), HTTP_200_OK)

    def put(self, req: Request, id: str):
        input_param = UpdateCategoryUseCase.Input(**req.data, id=id)
        output = self.update_use_case()(input_param)
        return Response(asdict(output), HTTP_200_OK)

    def delete(self, _req: Request, id: str):
        input_param = DeleteCategoryUseCase.Input(id=id)
        self.delete_use_case()(input_param)
        return Response(status=HTTP_204_NO_CONTENT)
