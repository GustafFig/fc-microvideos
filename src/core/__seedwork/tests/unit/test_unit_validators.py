"""Test the validation classes at __seedwork
"""

import typing as t
import unittest
# pylint: disable=abstract-class-instantiated
from dataclasses import fields, is_dataclass
from unittest.mock import MagicMock, PropertyMock, patch

from rest_framework.serializers import Serializer

from core.__seedwork.domain.validators import (DRFValidator,
                                               ValidationRulesException,
                                               ValidatorFieldsInterface,
                                               ValidatorRules)


class TestValidatorRulesUnit(unittest.TestCase):

    def test_values_method(self):
        validator = ValidatorRules.values('value1', 'field')
        self.assertIsInstance(validator, ValidatorRules)
        self.assertEqual(validator.value, "value1")
        self.assertEqual(validator.prop, "field")

    def test_required_raise_on_invalid_rule(self):
        invalid_data = [
            {"value": None, "prop": "field1"},
            {"value": "", "prop": "field2"},
        ]
        for i in invalid_data:
            msg = f"value = {i['value']}, prop = {i['prop']}"
            with self.assertRaises(ValidationRulesException, msg=msg) as error:
                ValidatorRules.values(i["value"], str(i["prop"])).required()
            self.assertEqual(
                f"The {i['prop']} is required", error.exception.args[0])

    def test_required_return_the_a_validator_when_value_pass(self):
        valid_data: t.List[t.Dict[str, t.Any]] = [
            {"value": 0, "prop": "field1"},
            {"value": False, "prop": "field1"},
            {"value": "string1", "prop": "field1"},
            {"value": {}, "prop": "field1"},
            {"value": [], "prop": "field1"},
        ]
        for i in valid_data:
            try:
                ValidatorRules.values(i["value"], i["prop"]).required()
            except ValidationRulesException as err:
                self.fail(err.args[0])

    def test_string_raise_on_invalid_rule(self):
        invalid_data: t.List[t.Dict[str, t.Any]] = [
            {"value": 0, "prop": "field1"},
            {"value": {}, "prop": "field2"},
            {"value": [], "prop": "field2"},
            {"value": True, "prop": "field2"},
        ]
        for i in invalid_data:
            msg = f"value = {i['value']}, prop = {i['prop']}"
            with self.assertRaises(ValidationRulesException, msg=msg) as error:
                ValidatorRules.values(i["value"], i["prop"]).string()
            self.assertEqual(
                f"The {i['prop']} must be a string", error.exception.args[0])

    def test_string_return_the_a_validator_when_value_pass(self):
        valid_data: t.List[t.Dict[str, t.Any]] = [
            {"value": None, "prop": "field1"},
            {"value": "", "prop": "field1"},
            {"value": "string112348$%$#%", "prop": "field1"},
        ]
        for i in valid_data:
            try:
                ValidatorRules.values(i["value"], i["prop"]).string()
            except ValidationRulesException as err:
                self.fail(err.args[0])

    def test_max_len_raise_on_invalid_rule(self):
        i = {"value": "t" * 6, "prop": "field"}
        msg = f"value = {i['value']}, prop = {i['prop']}"
        with self.assertRaises(ValidationRulesException, msg=msg) as error:
            ValidatorRules.values(i["value"], i["prop"]).max_length(5)
        self.assertEqual(
            f"The {i['prop']} length must be equal or lower than 5",
            error.exception.args[0]
        )

    def test_max_len_return_the_a_validator_when_value_pass(self):
        size = 5
        i = {"value": "t" * size, "prop": "field1"}
        try:
            ValidatorRules.values(i["value"], i["prop"]).max_length(size)
        except ValidationRulesException as err:
            self.fail(err.args[0])

    def test_boolean_raise_on_invalid_rule(self):
        invalid_data: t.List[t.Dict[str, t.Any]] = [
            {"value": 0, "prop": "field1"},
            {"value": 1, "prop": "field1"},
            {"value": {}, "prop": "field2"},
            {"value": [], "prop": "field2"},
            {"value": "True", "prop": "field2"},
        ]
        for i in invalid_data:
            msg = f"value = {i['value']}, prop = {i['prop']}"
            with self.assertRaises(ValidationRulesException, msg=msg) as error:
                ValidatorRules.values(i["value"], i["prop"]).boolean()
            self.assertEqual(
                f"The {i['prop']} must be a boolean", error.exception.args[0])

    def test_boolean_return_the_a_validator_when_value_pass(self):
        valid_data: t.List[t.Dict[str, t.Any]] = [
            {"value": None, "prop": "field1"},
            {"value": False, "prop": "field1"},
            {"value": True, "prop": "field1"},
        ]
        for i in valid_data:
            try:
                ValidatorRules.values(i["value"], i["prop"]).boolean()
            except ValidationRulesException as err:
                self.fail(err.args[0])

    def test_throw_a_validation_exception_when_combine_two_or_more_rules(self):
        with self.assertRaises(ValidationRulesException) as assert_error:
            ValidatorRules.values(
                None,
                'prop'
            ).required().string().max_length(5)
        self.assertEqual(
            'The prop is required',
            assert_error.exception.args[0],
        )

        with self.assertRaises(ValidationRulesException) as assert_error:
            ValidatorRules.values(
                5,
                'prop'
            ).required().string().max_length(5)
        self.assertEqual(
            'The prop must be a string',
            assert_error.exception.args[0],
        )

        with self.assertRaises(ValidationRulesException) as assert_error:
            ValidatorRules.values(
                "t" * 6,
                'prop'
            ).required().string().max_length(5)
        self.assertEqual(
            'The prop length must be equal or lower than 5',
            assert_error.exception.args[0],
        )

        with self.assertRaises(ValidationRulesException) as assert_error:
            ValidatorRules.values(
                None,
                'prop'
            ).required().boolean()
        self.assertEqual(
            'The prop is required',
            assert_error.exception.args[0],
        )

        with self.assertRaises(ValidationRulesException) as assert_error:
            ValidatorRules.values(
                5,
                'prop'
            ).required().boolean()
        self.assertEqual(
            'The prop must be a boolean',
            assert_error.exception.args[0],
        )

    def test_valid_cases_for_combination_between_rules(self):
        ValidatorRules('test', 'prop').required().string()
        ValidatorRules("t" * 5, 'prop').required().string().max_length(5)

        ValidatorRules(True, 'prop').required().boolean()
        ValidatorRules(False, 'prop').required().boolean()
        self.assertTrue(True)  # pylint: disable=redundant-unittest-assert


class TestValidatorFieldsInterface(unittest.TestCase):

    def test_it_is_abstract(self):
        with self.assertRaises(TypeError, msg="Error") as error:
            ValidatorFieldsInterface()  # type: ignore
        self.assertEqual(
            error.exception.args[0],
            "Can't instantiate abstract class ValidatorFieldsInterface "
            "with abstract method validate"
        )

    def test_it_is_a_dataclass(self):
        self.assertTrue(is_dataclass(ValidatorFieldsInterface))

    def test_attrs(self):
        errors_field, validated_data_field = fields(ValidatorFieldsInterface)
        self.assertEqual(errors_field.name, 'errors')
        self.assertIsNone(errors_field.default)

        self.assertEqual(validated_data_field.name, 'validated_data')
        self.assertIsNone(validated_data_field.default)


class TestDRFValidatorUnit(unittest.TestCase):

    @patch.object(Serializer, 'is_valid', return_value=True)
    @patch.object(
        Serializer,
        'validated_data',
        return_value={'field': 'value'},
        new_callable=PropertyMock,
    )
    def test_if_validated_data_is_set_when_is_valid(
        self, mock_validated_data: PropertyMock, mock_is_valid: MagicMock
    ):
        validator = DRFValidator()
        is_valid = validator.validate(Serializer())
        self.assertTrue(is_valid)
        self.assertEqual(validator.validated_data, {'field': 'value'})
        mock_validated_data.assert_called_once()
        mock_is_valid.assert_called_once()

    @patch.object(Serializer, 'is_valid', return_value=True)
    @patch.object(
        Serializer,
        'validated_data',
        return_value={'field': 'value'},
        new_callable=PropertyMock,
    )
    def test_if_validated_data_is_set_when_is_not_valid(
        self, mock_validated_data: PropertyMock, mock_is_valid: MagicMock
    ):
        validator = DRFValidator()
        is_valid = validator.validate(Serializer())
        self.assertTrue(is_valid)
        self.assertEqual(validator.validated_data, {'field': 'value'})
        mock_validated_data.assert_called_once()
        mock_is_valid.assert_called_once()
