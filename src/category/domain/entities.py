"""Define the entities of domain"""
from dataclasses import dataclass, field
import datetime as dt
import typing as t

from __seedwork.domain.entities import Entity, ToggleIsActive
from __seedwork.domain.exceptions import ValidationException
from category.domain.validators import CategoryValidatorFactory

# O frozen evita o comportamento anêmico com as entidades


@dataclass(kw_only=True, frozen=True, slots=True)
class Category(Entity, ToggleIsActive):
    """Define the category entity at the domain"""

    name: str
    description: t.Optional[str] = None
    is_active: bool = True
    created_at: dt.datetime = field(default_factory=dt.datetime.now)

    def __post_init__(self, **kwargs):
        created_at = self.created_at if self.created_at else dt.datetime.now()
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
