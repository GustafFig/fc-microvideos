# pylint: disable=no-member
from typing import Optional, List

from django.core.exceptions import ValidationError

from core.__seedwork.domain.exceptions import EntityNotFound
from core.__seedwork.domain.value_objects import UniqueEntityId
from core.category.domain.entities import Category
from core.category.domain.repositories import CategoryRepository
from django_app.category.models import CategoryModel


class CategoryDjangoRepository(CategoryRepository):

    def insert(self, entity: Category) -> None:
        CategoryModel.objects.create(**entity.to_dict())

    def update(self, entity: Category) -> None:
        raise NotImplementedError()

    def delete(self, entity: Category) -> None:
        raise NotImplementedError()

    def find_by_id(self, entity_id: str | UniqueEntityId) -> Optional[Category]:
        model = self._get(str(entity_id))
        return Category(
            unique_entity_id=UniqueEntityId(entity_id),
            name=model.name,
            description=model.description,
            is_active=model.is_active,
            created_at=model.created_at,
        )

    def find_all(self) -> List[Category]:
        raise NotImplementedError()

    def search(self, params: CategoryRepository.SearchParams) -> CategoryRepository.SearchResult:
        raise NotImplementedError()

    def _get(self, entity_id: str) -> CategoryModel:
        try:
            return CategoryModel.objects.get(pk=entity_id)
        except (CategoryModel.DoesNotExist, ValidationError) as err:
            raise EntityNotFound(Category) from err
