# pylint: disable=redefined-builtin
# pylint: disable=invalid-name
from dataclasses import dataclass
from typing import Callable, Optional

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT

from core.__seedwork.infra.serializers import UUIDSerializer
from core.category.application.dto import CategoryOutput
from core.category.application.usecase import (
    CreateCategoryUseCase,
    DeleteCategoryUseCase,
    GetCategoryUseCase,
    ListCategoriesUseCase,
    UpdateCategoryUseCase,
)
from core.category.infra.serializer import CategorySerializer, CategoryCollectionSerializer


@dataclass(slots=True)
class CategoryResource(APIView):

    create_use_case: Optional[Callable[[], CreateCategoryUseCase]] = None
    list_use_case: Optional[Callable[[], ListCategoriesUseCase]] = None
    get_use_case: Optional[Callable[[], GetCategoryUseCase]] = None
    update_use_case: Optional[Callable[[], UpdateCategoryUseCase]] = None
    delete_use_case: Optional[Callable[[], DeleteCategoryUseCase]] = None

    def post(self, req: Request):
        serializer = CategorySerializer(data=req.data)
        serializer.is_valid(raise_exception=True)

        input_param = CreateCategoryUseCase.Input(**serializer.validated_data)
        method = self.create_use_case()
        output = method(input_param)
        body = self.category_to_response(output)
        return Response(body, status=HTTP_201_CREATED)

    def get(self, req: Request, id: str = None):
        if id:
            return self.get_object(id=id)
        input_param = ListCategoriesUseCase.Input(**req.query_params.dict())
        output = self.list_use_case()(input_param)
        body = CategoryCollectionSerializer(instance=output).data
        return Response(body)

    def get_object(self, id: str):
        CategoryResource.validate_id(id)
        input_param = GetCategoryUseCase.Input(id=id)
        output = self.get_use_case()(input_param)
        body = self.category_to_response(output)
        return Response(body, HTTP_200_OK)

    def put(self, req: Request, id: str):  # pylint: disable=redefined-builtin,invalid-name
        CategoryResource.validate_id(id)

        serializer = CategorySerializer(data=req.data)
        serializer.is_valid(raise_exception=True)
        input_param = UpdateCategoryUseCase.Input(
            **{'id': id, **serializer.validated_data}
        )
        output = self.update_use_case()(input_param)
        body = self.category_to_response(output)
        return Response(body, HTTP_200_OK)

    def delete(self, _req: Request, id: str):
        self.validate_id(id)
        input_param = DeleteCategoryUseCase.Input(id=id)
        self.delete_use_case()(input_param)
        return Response(status=HTTP_204_NO_CONTENT)

    @staticmethod
    def category_to_response(output: CategoryOutput) -> CategorySerializer:
        serializer = CategorySerializer(instance=output)
        return serializer.data

    @staticmethod
    def validate_id(id: str):  # pylint: disable=redefined-builtin,invalid-name
        serializer = UUIDSerializer(data={'id': id})
        serializer.is_valid(raise_exception=True)
