from dataclasses import dataclass, field
from src.__seedwork.domain.exceptions import InvalidUUidException
import uuid

@dataclass(frozen=True)
class UniqueEntityId:

    id: str = field(default_factory=lambda : str(uuid.uuid4()))

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


