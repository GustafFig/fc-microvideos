"""
Define the rules to validate category's module's entities
"""
# pylint: disable=too-few-public-methods
from typing import Dict
from rest_framework.serializers import Serializer, DateTimeField
from __seedwork.domain.validators import ValidatorRules, ValidatorRulesValidator
from __seedwork.domain.validators import DRFValidator, StrictBooleanField, StrictCharField


class CategoryRules(Serializer):
    name = StrictCharField(max_length=255)
    description = StrictCharField(
        required=False, allow_null=True, allow_blank=True
    )
    is_active = StrictBooleanField(required=False)
    created_at = DateTimeField(required=False)


class DRFCategoryValidator(DRFValidator[Dict]):

    def validate(self, data: Dict) -> bool:
        return super().validate(
            CategoryRules(data=data or {})  # type: ignore
        )


class ValidatorRulesCategoryValidator(ValidatorRulesValidator):

    def validate(self, data):
        ValidatorRules.values(
            data.get('name'), 'name').required().string().max_length(255)
        ValidatorRules.values(data.get('description'), 'description').string()
        ValidatorRules.values(data.get('is_active'), 'is_active').boolean()
        ValidatorRules.values(data.get('is_active'), 'is_active').boolean()
        return True


class CategoryValidatorFactory:

    @staticmethod
    def create():
        return DRFCategoryValidator()
