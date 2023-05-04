import unittest
from collections import namedtuple

from category.domain.validators import DRFCategoryValidator, CategoryValidatorFactory


class TestCategoryValidatorUnit(unittest.TestCase):

    validator: DRFCategoryValidator

    def setUp(self) -> None:
        self.validator = CategoryValidatorFactory.create()

    def test_no_field_is_passed(self):
        InvalidaData = namedtuple("InvalidData", ["data", "expected"])
        invalid_data = [
            InvalidaData(None, "This field is required."),
            InvalidaData({}, "This field is required."),
        ]
        for data in invalid_data:
            is_valid = self.validator.validate(data.data)
            self.assertFalse(is_valid)
            errors = self.validator.errors or {}
            self.assertIn("name", errors)
            self.assertEqual(data.expected, errors["name"][0])

    def test_invalid_name(self):

        InvalidaData = namedtuple("InvalidData", ["data", "expected"])
        invalid_data = [
            InvalidaData(None, "This field is required."),
            InvalidaData({}, "This field is required."),
            InvalidaData({'name': None}, 'This field may not be null.'),
            InvalidaData({'name': ''}, 'This field may not be blank.'),
            InvalidaData({'name': 5}, 'Not a valid string.'),
            InvalidaData({'name': {}}, 'Not a valid string.'),
            InvalidaData({'name': 5.5}, 'Not a valid string.'),
            InvalidaData({'name': []}, 'Not a valid string.'),
            InvalidaData({'name': 'a'*256},
                         'Ensure this field has no more than 255 characters.'),
        ]

        for data in invalid_data:
            is_valid = self.validator.validate(data.data)
            self.assertFalse(is_valid)
            errors = self.validator.errors or {}
            self.assertIn("name", errors)
            self.assertEqual(data.expected, errors["name"][0])

    def test_invalid_description(self):
        InvalidaData = namedtuple("InvalidData", ["data", "expected"])
        predata = {"name": "valid"}
        invalid_data = [
            InvalidaData({**predata, 'description': 5}, 'Not a valid string.'),
            InvalidaData({**predata, 'description': {}},
                         'Not a valid string.'),
            InvalidaData({**predata, 'description': 5.5},
                         'Not a valid string.'),
            InvalidaData({**predata, 'description': []},
                         'Not a valid string.'),
        ]

        for data in invalid_data:
            is_valid = self.validator.validate(data.data)
            self.assertFalse(is_valid, f"Should be invalid, {data.data}")
            errors = self.validator.errors or {}
            self.assertIn("description", errors)
            self.assertEqual(
                data.expected,
                errors["description"][0],
                f"Expected: {data.expected}, Actual {errors['description'][0]}"
            )

    def test_invalid_active_values(self):
        InvalidaData = namedtuple("InvalidData", ["data", "expected"])
        predata = {"name": "valid", "description": "Valid"}
        invalid_data = [
            InvalidaData({**predata, "is_active": 5},
                         'Must be a valid boolean.'),
            InvalidaData({**predata, "is_active": {}},
                         'Must be a valid boolean.'),
            InvalidaData({**predata, "is_active": 5.5},
                         'Must be a valid boolean.'),
            InvalidaData({**predata, "is_active": []},
                         'Must be a valid boolean.'),
        ]

        for data in invalid_data:
            is_valid = self.validator.validate(data.data)
            self.assertFalse(is_valid, f"Should be invalid, {data.data}")
            errors = self.validator.errors or {}
            self.assertIn("is_active", errors)
            self.assertEqual(
                data.expected,
                errors["is_active"][0],
                f"Expected: {data.expected}, Actual {errors['is_active'][0]}"
            )

    def test_invalid_created_at(self):
        InvalidaData = namedtuple("InvalidData", ["data", "expected"])
        predata = {"name": "valid", "description": "Valid"}
        invalid_message = "Datetime has wrong format. Use one of these formats instead: YYYY-MM-DDThh:mm[:ss[.uuuuuu]][+HH:MM|-HH:MM|Z]."
        invalid_data = [
            InvalidaData({**predata, "created_at": 5}, invalid_message),
            InvalidaData({**predata, "created_at": {}}, invalid_message),
            InvalidaData({**predata, "created_at": 5.5}, invalid_message),
            InvalidaData({**predata, "created_at": []}, invalid_message),
        ]

        for index, data in enumerate(invalid_data):
            is_valid = self.validator.validate(data.data)
            self.assertFalse(is_valid, f"Should be invalid, {data.data}")
            errors = self.validator.errors or {}
            self.assertIn("created_at", errors)
            self.assertEqual(
                data.expected,
                errors["created_at"][0],
                f"Row: {index}, Expected: '{data.expected}', Actual: '{errors['created_at'][0]}'"
            )

    def test_validate_cases(self):

        valid_data = [
            {'name': 'Movie'},
            {'name': 'Movie', 'description': None},
            {'name': 'Movie', 'description': ''},
            {'name': 'Movie', 'description': 'some description'},
            {'name': 'Movie', 'is_active': True},
            {'name': 'Movie', 'is_active': False},
            {'name': 'Movie', 'description': 'some description', 'is_active': True},
        ]

        for index, data in enumerate(valid_data):
            is_valid = self.validator.validate(data)
            self.assertTrue(is_valid, f"Row: {index}, valid_data: {data}, {self.validator.errors}")
