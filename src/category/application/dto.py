from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Type, TypeVar

from category.domain.entities import Category


@dataclass(frozen=True, slots=True)
class CategoryOutput:
    id: str  # pylint: disable=invalid-name
    name: str
    description: Optional[str]
    is_active: bool
    created_at: datetime


Output = TypeVar('Output', bound=CategoryOutput)


@dataclass()
class CategoryOutputMapper:

    child_output: Type[Output] = CategoryOutput

    @staticmethod
    def with_child(child: Output):
        return CategoryOutputMapper(child_output=child)

    @staticmethod
    def without_child():
        return CategoryOutputMapper()

    def to_output(self, category: Category) -> Output:
        return self.child_output(
            id=category.id,
            name=category.name,
            description=category.description,
            is_active=category.is_active,
            created_at=category.created_at
        )
