"""Module for define an declarator rules for Validation of the project domain
    It is an internal library
"""

from dataclasses import dataclass
from typing import Any

from .exceptions import ValidationException


@dataclass(slots=True, frozen=True)
class ValidatorRules:
    """Used to define validation for fields and vallues"""
    value: Any
    prop: str

    @staticmethod
    def values(value: Any, prop: str) ->  'ValidatorRules':
        """Create the Validator Rules"""
        return ValidatorRules(value, prop)

    def required(self):
        """Test if value is not None, neither empty string"""
        if self.value is None or self.value == "":
            raise ValidationException(f'The {self.prop} is required')
        return self

    def string(self):
        """Test if value is of type str"""
        if self.value is not None and not isinstance(self.value, str):
            raise ValidationException(f"The {self.prop} must be a string")
        return self

    def max_length(self, size: int):
        """Test max size of string"""
        if self.value is not None and len(self.value) > size:
            raise ValidationException(
                f"The {self.prop} length must be equal or lower than {size}"
            )
        return self

    def boolean(self):
        if all(self.value is not obj for obj in [None, True, False]):
            raise ValidationException(
                f"The {self.prop} must be a boolean"
            )
        return self
