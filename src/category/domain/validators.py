"""
Define the rules to validate category's module's entities
"""
# pylint: disable=too-few-public-methods
from typing import Dict

from rest_framework.serializers import DateTimeField, Serializer

from __seedwork.domain.validators import (DRFValidator, StrictBooleanField,
                                          StrictCharField, ValidatorRules,
                                          ValidatorRulesValidator)


class CategoryRules(Serializer):
    name = StrictCharField(max_length=255)
    description = StrictCharField(
        required=False, allow_null=True, allow_blank=True
    )
    is_active = StrictBooleanField(required=False)
    created_at = DateTimeField(required=False)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


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
