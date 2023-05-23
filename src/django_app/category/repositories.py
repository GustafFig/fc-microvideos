# pylint: disable=no-member
from typing import Optional, List

from django.core.exceptions import ValidationError

from core.__seedwork.domain.exceptions import EntityNotFound
from core.__seedwork.domain.value_objects import UniqueEntityId
from core.category.domain.entities import Category
from core.category.domain.repositories import CategoryRepository
from core.category.infra.mapper import CategoryDjangoModelMapper
from django_app.category.models import CategoryModel


class CategoryDjangoRepository(CategoryRepository):

    def insert(self, entity: Category) -> None:
        model = CategoryDjangoModelMapper.to_model(entity)
        model.save()

    def update(self, entity: Category) -> None:
        raise NotImplementedError()

    def delete(self, entity: Category) -> None:
        raise NotImplementedError()

    def find_by_id(self, entity_id: str | UniqueEntityId) -> Optional[Category]:
        model = self._get(str(entity_id))
        return CategoryDjangoModelMapper.to_entity(model)

    def find_all(self) -> List[Category]:
        return [
            CategoryDjangoModelMapper.to_entity(model)
            for model in CategoryModel.objects.all()
        ]

    def search(self, params: CategoryRepository.SearchParams) -> CategoryRepository.SearchResult:
        raise NotImplementedError()

    def _get(self, entity_id: str) -> CategoryModel:
        try:
            return CategoryModel.objects.get(pk=entity_id)
        except (CategoryModel.DoesNotExist, ValidationError) as err:
            raise EntityNotFound(Category) from err
