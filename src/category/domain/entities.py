"""Define the entities of domain"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
import datetime as dt
import typing as t

from rest_framework.serializers import Serializer

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
    def validate(cls, name: str, description: str, is_active: bool = None):
        ValidatorRules.values(name, 'name').required().string().max_length(255)
        ValidatorRules.values(description, 'description').string()
        ValidatorRules.values(is_active, 'is_active').boolean()


ErrorFields = t.Dict[str, t.List[str]]
PropsValidated = t.TypeVar('PropsValidated')


class ValidatorFieldsInterface(ABC, t.Generic[PropsValidated]):
    """Define the format the type of a Validator in the domain"""
    errors: ErrorFields = t.Optional[None]
    validated_data: t.Optional[PropsValidated] = None

    @abstractmethod
    def validate(self, data: t.Any) -> bool:
        raise NotImplementedError()


class DRFValidator(ValidatorFieldsInterface[PropsValidated], ABC):
    """Define a domain validator based on Django Rest Framework"""

    def validate(self, data: Serializer):
        if data.is_valid():
            self.validated_data = data.validated_data
            return True
        else:
            self.errors = {
                key: [str(err) for err in errors]
                for key, errors in data.errors.items()
            }
            return False
