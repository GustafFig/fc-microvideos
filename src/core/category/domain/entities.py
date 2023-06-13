"""Define the entities of domain"""
import datetime as dt
import typing as t
from dataclasses import dataclass, field

from core.__seedwork.domain.entities import Entity, ToggleIsActive
from core.__seedwork.domain.exceptions import ValidationException
from core.category.domain.validators import CategoryValidatorFactory

# O frozen evita o comportamento anêmico com as entidades


@dataclass(kw_only=True, frozen=True, slots=True)
class Category(Entity, ToggleIsActive):
    """Define the category entity at the domain"""

    name: str
    description: t.Optional[str] = None
    is_active: bool = True
    created_at: dt.datetime = field(
        default_factory=lambda: dt.datetime.now(dt.timezone.utc)
    )

    def __post_init__(self):
        created_at = self.created_at if self.created_at else dt.datetime.now(dt.timezone.utc)
        object.__setattr__(self, 'created_at', created_at)
        self.validate()

    def update(self, *, name: str, description: t.Optional[str]) -> None:
        object.__setattr__(self, 'name', name)
        object.__setattr__(self, 'description', description)
        self.validate()

    def validate(self):
        """Validate the Category entity"""
        validator = CategoryValidatorFactory().create()
        is_category_valid = validator.validate(self.to_dict())
        if not is_category_valid:
            raise ValidationException(validator.errors)

    @staticmethod
    def fake():
        from .entities_faker_builder import CategoryFakerBuilder # pylint: disable=import-outside-toplevel
        return CategoryFakerBuilder
