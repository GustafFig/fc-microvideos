import unittest
from __seedwork.domain.validators import ValidatorRules, ValidationException
import typing as t

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
            with self.assertRaises(ValidationException, msg=msg) as error:
                ValidatorRules.values(i["value"], str(i["prop"])).required()
            self.assertEqual(f"The {i['prop']} is required", error.exception.args[0])


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
            except ValidationException as err:
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
            with self.assertRaises(ValidationException, msg=msg) as error:
                ValidatorRules.values(i["value"], i["prop"]).string()
            self.assertEqual(f"The {i['prop']} must be a string", error.exception.args[0])

    def test_string_return_the_a_validator_when_value_pass(self):
        valid_data: t.List[t.Dict[str, t.Any]] = [
            {"value": None, "prop": "field1"},
            {"value": "", "prop": "field1"},
            {"value": "string112348$%$#%", "prop": "field1"},
        ]
        for i in valid_data:
            try:
                ValidatorRules.values(i["value"], i["prop"]).string()
            except ValidationException as err:
                self.fail(err.args[0])

    def test_max_len_raise_on_invalid_rule(self):
        i = {"value": "t" * 6, "prop": "field"}
        msg = f"value = {i['value']}, prop = {i['prop']}"
        with self.assertRaises(ValidationException, msg=msg) as error:
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
        except ValidationException as err:
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
            with self.assertRaises(ValidationException, msg=msg) as error:
                ValidatorRules.values(i["value"], i["prop"]).boolean()
            self.assertEqual(f"The {i['prop']} must be a boolean", error.exception.args[0])

    def test_boolean_return_the_a_validator_when_value_pass(self):
        valid_data: t.List[t.Dict[str, t.Any]] = [
            {"value": None, "prop": "field1"},
            {"value": False, "prop": "field1"},
            {"value": True, "prop": "field1"},
        ]
        for i in valid_data:
            try:
                ValidatorRules.values(i["value"], i["prop"]).boolean()
            except ValidationException as err:
                self.fail(err.args[0])

    def test_throw_a_validation_exception_when_combine_two_or_more_rules(self):
        with self.assertRaises(ValidationException) as assert_error:
            ValidatorRules.values(
                None,
                'prop'
            ).required().string().max_length(5)
        self.assertEqual(
            'The prop is required',
            assert_error.exception.args[0],
        )

        with self.assertRaises(ValidationException) as assert_error:
            ValidatorRules.values(
                5,
                'prop'
            ).required().string().max_length(5)
        self.assertEqual(
            'The prop must be a string',
            assert_error.exception.args[0],
        )

        with self.assertRaises(ValidationException) as assert_error:
            ValidatorRules.values(
                "t" * 6,
                'prop'
            ).required().string().max_length(5)
        self.assertEqual(
            'The prop length must be equal or lower than 5',
            assert_error.exception.args[0],
        )

        with self.assertRaises(ValidationException) as assert_error:
            ValidatorRules.values(
                None,
                'prop'
            ).required().boolean()
        self.assertEqual(
            'The prop is required',
            assert_error.exception.args[0],
        )

        with self.assertRaises(ValidationException) as assert_error:
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
