from abc import ABC
from dataclasses import Field, asdict, dataclass, field

from core.__seedwork.domain.value_objects import UniqueEntityId


@dataclass(frozen=True, slots=True)
class Entity(ABC):

    unique_entity_id: UniqueEntityId = field(
        default_factory=lambda: UniqueEntityId()  # pylint: disable=unnecessary-lambda
    )

    @property
    def id(self):  # pylint: disable=invalid-name
        return str(self.unique_entity_id)

    def to_dict(self):
        entity_dict = asdict(self)
        entity_dict.pop('unique_entity_id')
        entity_dict['id'] = self.id
        return entity_dict

    @classmethod
    def get_field(cls, entity_field: str) -> Field:
        return cls.__dataclass_fields__[entity_field]  # pylint: disable=no-member


class ToggleIsActive():

    def activate(self) -> None:
        object.__setattr__(self, 'is_active', True)

    def inactivate(self) -> None:
        object.__setattr__(self, 'is_active', False)
