"""Module for declare the Exception of the project"""

from typing import TYPE_CHECKING, Type

if TYPE_CHECKING:
    from core.__seedwork.domain.entities import Entity


class InvalidUUidException(Exception):
    """The Exception for invalid UUID value"""

    def __init__(self, error: str = "ID must be a valid UUID") -> None:
        super().__init__(error)


class ValidationException(Exception):
    """The Exception for domain validations"""

    def __init__(self, error) -> None:
        self.error = error
        super().__init__('Validation Error')

class LoadValidationException(Exception):
    """The Exception for domain validations"""

    def __init__(self, error) -> None:
        self.error = error
        super().__init__('Load Entity Error')


class ValidationRulesException(Exception):
    """The Exception for ValidationRulesException"""


class EntityNotFound(Exception):
    def __init__(self, entity_type: Type['Entity']) -> None:
        super().__init__(f"{entity_type.__name__} not found")


class MissingParameter(Exception):

    def __init__(self, parameter_name) -> None:
        super().__init__(f"Missing parameter {parameter_name}")
