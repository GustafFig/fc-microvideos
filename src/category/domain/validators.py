"""
Define the rules to validate category's module's entities
"""
# pylint: disable=too-few-public-methods
from typing import Dict
from rest_framework.serializers import Serializer, DateTimeField
from __seedwork.domain.validators import DRFValidator, StrictBooleanField, StrictCharField


class CategoryRules(Serializer):
    name = StrictCharField(max_length=255)
    description = StrictCharField(
        required=False, allow_null=True, allow_black=True
    )
    is_active = StrictBooleanField(required=False)
    created_at = DateTimeField(required=True)


class CategoryValidator(DRFValidator[Dict]):

    def validate(self, data: Dict) -> bool:
        return super().validate(
            CategoryRules(data=data) # type: ignore
        )


class CategoryValidatorFactory:

    @staticmethod
    def create():
        return CategoryValidator()
