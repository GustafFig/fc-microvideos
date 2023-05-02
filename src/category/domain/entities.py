"""Define the entities of domain"""
from dataclasses import dataclass, field
import datetime as dt
import typing as t

from __seedwork.domain.entities import Entity, ToggleIsActive
from __seedwork.domain.validators import ValidatorRules

# O frozen evita o comportamento anêmico com as entidades


@dataclass(kw_only=True, frozen=True, slots=True)
class Category(Entity, ToggleIsActive):
    """Define the category entity at the domain"""

    name: str
    description: t.Optional[str] = None
    is_active: bool = True
    created_at: dt.datetime = field(default_factory=dt.datetime.now)

    def __new__(cls, **kwargs):
        cls.validate(
            name=kwargs.get("name"),
            description=kwargs.get("description"),
            is_active=kwargs.get("is_active"),
        )
        return super(Category, cls).__new__(cls)

    def update(self, *, name: str, description: t.Optional[str]) -> None:
        object.__setattr__(self, 'name', name)
        object.__setattr__(self, 'description', description)

    @classmethod
    def validate(
        cls,
        name: t.Optional[str],
        description: t.Optional[str],
        is_active: t.Optional[bool] = None
    ):
        """Validate the Category entity"""
        ValidatorRules.values(name, 'name').required().string().max_length(255)
        ValidatorRules.values(description, 'description').string()
        ValidatorRules.values(is_active, 'is_active').boolean()
