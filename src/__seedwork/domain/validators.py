"""
    Module for define an declarator rules for Validation of the project domain
    It is an internal library
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Generic, List, TypeVar, Dict, Optional
from rest_framework.fields import BooleanField, CharField

from rest_framework.serializers import Serializer
from .exceptions import ValidationRulesException


@dataclass(slots=True, frozen=True)
class ValidatorRules:
    """Used to define validation for fields and vallues"""
    value: Any
    prop: str

    @staticmethod
    def values(value: Any, prop: str) -> 'ValidatorRules':
        """Create the Validator Rules"""
        return ValidatorRules(value, prop)

    def required(self):
        """Test if value is not None, neither empty string"""
        if self.value is None or self.value == "":
            raise ValidationRulesException(f'The {self.prop} is required')
        return self

    def string(self):
        """Test if value is of type str"""
        if self.value is not None and not isinstance(self.value, str):
            raise ValidationRulesException(f"The {self.prop} must be a string")
        return self

    def max_length(self, size: int):
        """Test max size of string"""
        if self.value is not None and len(self.value) > size:
            raise ValidationRulesException(
                f"The {self.prop} length must be equal or lower than {size}"
            )
        return self

    def boolean(self):
        if all(self.value is not obj for obj in [None, True, False]):
            raise ValidationRulesException(
                f"The {self.prop} must be a boolean"
            )
        return self


ErrorFields = Dict[str, List[str]]
PropsValidated = TypeVar('PropsValidated', Dict, Any)


@dataclass(slots=True)
class ValidatorFieldsInterface(ABC, Generic[PropsValidated]):
    """Define the format the type of a Validator in the domain"""
    errors: Optional[ErrorFields] = None
    validated_data: Optional[PropsValidated] = None

    @abstractmethod
    def validate(self, data: Any) -> bool:
        raise NotImplementedError()


@dataclass(slots=True)
class ValidatorRulesValidator(ABC, Generic[PropsValidated]):
    """Define a domain validator based on ValidatorRules in-project class"""
    @abstractmethod
    def validate(self, data: Dict) -> bool:
        raise NotImplementedError()


@dataclass(slots=True)
class DRFValidator(ValidatorFieldsInterface[PropsValidated], ABC):
    """Define a domain validator based on Django Rest Framework"""

    def validate(self, data: Serializer) -> bool:
        if data.is_valid():
            self.validated_data = data.validated_data  # type: ignore
            return True

        self.errors = {
            key: [str(err) for err in errors]
            for key, errors in data.errors.items()
        }
        return False


class StrictBooleanField(BooleanField):
    """Accept only True, False and None.
        In case of None it needs to be explicit liberate by allow_null
    """

    def to_internal_value(self, data):
        if data is True:
            return True
        if data is False:
            return False
        if data is None and self.allow_null:
            return None
        self.fail('invalid', input=data)
        return bool(data)


class StrictCharField(CharField):

    def to_internal_value(self, data):
        if not isinstance(data, str):
            self.fail('invalid')

        return super().to_internal_value(data)
