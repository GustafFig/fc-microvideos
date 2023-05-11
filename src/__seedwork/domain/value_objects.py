import json
import uuid
from abc import ABC
from dataclasses import dataclass, field, fields

from src.__seedwork.domain.exceptions import InvalidUUidException


@dataclass(frozen=True)
class ValueObject(ABC):
    def __eq__(self, other):
        if not isinstance(other, ValueObject):
            raise NotImplementedError(
                f"ValueObject cannot be compared equally with {type(other)}")

    def __str__(self) -> str:
        fields_name = [field.name for field in fields(self)]
        if len(fields_name) == 1:
            return str(getattr(self, fields_name[0]))
        return json.dumps({field_name: getattr(self, field_name) for field_name in fields_name})


@dataclass(frozen=True)
class UniqueEntityId(ValueObject):

    id: str = field(default_factory=lambda: str(uuid.uuid4()))  # pylint: disable=invalid-name

    def __post_init__(self):
        # garante que sempre seja uma string
        id_value = str(self.id) if isinstance(self.id, uuid.UUID) else self.id
        object.__setattr__(self, 'id', id_value)
        self.__validate()

    def __validate(self):
        try:
            uuid.UUID(self.id)
        except Exception as ex:
            raise InvalidUUidException() from ex

    def __str__(self):
        return f"{self.id}"

    def __repr__(self):
        return f"{self.id}"
