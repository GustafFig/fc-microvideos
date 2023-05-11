"""
    Test integrations classes of validations
"""
# pylint: disable=abstract-method

import unittest

from rest_framework.exceptions import ErrorDetail
from rest_framework.serializers import Serializer

from __seedwork.domain.validators import StrictBooleanField, StrictCharField


class TestStrictCharField(unittest.TestCase):

    class StubDFVStrictCharField(Serializer):
        name = StrictCharField()

    def test_it_invalid_for_non_string_values(self):
        invalid_data = [
            {"name": {}},
            {"name": []},
            {"name": 1},
            {"name": False},
            {"name": True},
            {"name": 1.1},
            {"name": set()},
        ]
        for invalid in invalid_data:
            serializer = self.StubDFVStrictCharField(data=invalid)
            self.assertFalse(serializer.is_valid())
            self.assertEqual({}, serializer.validated_data)
            self.assertEqual(serializer.errors["name"][0],
                             ErrorDetail("Not a valid string.", "invalid"))

    def test_it_consider_none_invalid(self):
        data = {"name": None}
        serializer = self.StubDFVStrictCharField(data=data)  # type: ignore
        self.assertFalse(serializer.is_valid())
        self.assertEqual({}, serializer.validated_data)
        self.assertEqual(serializer.errors["name"][0],
                         ErrorDetail("This field may not be null.", "null"))

    def test_valid_strings(self):
        valid_data = [
            {"name": "{}"},
            {"name": "[]"},
            {"name": "1"},
            {"name": "False"},
            {"name": "True"},
            {"name": "1.1"},
            {"name": "qwertyuiop;/@#$%*++='-®ħæßøæøþđ“«ø/¢]£set()"},
        ]
        for valid in valid_data:
            serializer = self.StubDFVStrictCharField(
                data=valid)  # type: ignore
            self.assertTrue(serializer.is_valid())
            # type: ignore
            # type: ignore
            self.assertEqual(serializer.validated_data["name"], valid["name"])  # type: ignore
            self.assertEqual(serializer.errors, {})


class TestStrictBooleanField(unittest.TestCase):

    class StubDFVStrictBooleanFieldNonNull(Serializer):
        active = StrictBooleanField()

    class StubDFVStrictBooleanFieldNonNullable(Serializer):
        active = StrictBooleanField(allow_null=True)

    def test_it_invalid_for_non_string_values(self):
        invalid_data = [
            {"active": {}},
            {"active": []},
            {"active": 1},
            {"active": "False"},
            {"active": "True"},
            {"active": 1.1},
            {"active": set()},
        ]
        for index, invalid in enumerate(invalid_data):
            serializer = self.StubDFVStrictBooleanFieldNonNull(data=invalid)

            assert_error_message = f"Row: {index}, invalida_data: {invalid}"
            self.assertFalse(serializer.is_valid(), assert_error_message)
            self.assertEqual({}, serializer.validated_data,
                             assert_error_message)
            self.assertEqual(serializer.errors["active"][0],
                             ErrorDetail(
                                 "Must be a valid boolean.", "invalid"),
                             assert_error_message)

    def test_it_when_none_is_passed(self):
        data = {"active": None}
        serializer = self.StubDFVStrictBooleanFieldNonNull(
            data=data)  # type: ignore
        self.assertFalse(serializer.is_valid())
        self.assertEqual({}, serializer.validated_data)
        self.assertEqual(serializer.errors["active"][0],
                         ErrorDetail("This field may not be null.", "null"))

        data = {"active": None}
        serializer = self.StubDFVStrictBooleanFieldNonNullable(
            data=data)  # type: ignore
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.errors, {})
        validated_data = serializer.validated_data or {}
        self.assertEqual(validated_data["active"], None)  # type: ignore

    def test_valid_booleans(self):
        valid_data = [
            {"active": False},
            {"active": True},
        ]
        for valid in valid_data:
            serializer = self.StubDFVStrictBooleanFieldNonNull(
                data=valid)  # type: ignore
            self.assertTrue(serializer.is_valid())
            # type: ignore
            validated_data = serializer.validated_data or {}
            self.assertEqual(
                validated_data["active"], valid["active"])  # type: ignore
            self.assertEqual(serializer.errors, {})
