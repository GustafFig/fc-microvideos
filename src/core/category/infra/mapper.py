# Evita de mexer no repositório se tiver um dado novo e ou mais simples
# Dado novo
# pylint: disable=import-outside-toplevel
from typing import TYPE_CHECKING

from core.__seedwork.domain.exceptions import (LoadValidationException,
                                               ValidationException)
from core.__seedwork.domain.value_objects import UniqueEntityId
from core.category.domain.entities import Category

if TYPE_CHECKING:
    from django_app.category.models import CategoryModel


class CategoryDjangoModelMapper:

    @staticmethod
    def to_entity(model: 'CategoryModel') -> Category:
        try:
            return Category(
                unique_entity_id=UniqueEntityId(model.id),
                name=model.name,
                description=model.description,
                is_active=model.is_active,
                created_at=model.created_at,
            )
        except ValidationException as err:
            raise LoadValidationException(err.args[0]) from err

    @staticmethod
    def to_model(entity: Category) -> 'CategoryModel':
        from django_app.category.models import CategoryModel
        return CategoryModel(**entity.to_dict())
