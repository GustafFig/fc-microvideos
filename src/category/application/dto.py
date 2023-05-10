from dataclasses import dataclass
from datetime import datetime
from typing import Optional, TypeVar
from category.domain.entities import Category


@dataclass(frozen=True, slots=True)
class CategoryOutput:
    id: str  # pylint: disable=invalid-name
    name: str
    description: Optional[str]
    is_active: bool
    created_at: datetime


Output = TypeVar('Output', bound=CategoryOutput)


class CategoryOutputMapper:

    @staticmethod
    def to_output(category: Category) -> CategoryOutput:
        return CategoryOutput(
            id=category.id,
            name=category.name,
            description=category.description,
            is_active=category.is_active,
            created_at=category.created_at
        )