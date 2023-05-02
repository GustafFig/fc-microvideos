"""
    Test integrations classes of validations
"""


import unittest

from __seedwork.domain.validators import StrictBooleanField, StrictCharField, BooleanField
from rest_framework.exceptions import ErrorDetail
from rest_framework.serializers import Serializer


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
            self.assertEqual(serializer.validated_data["name"], valid["name"])
            self.assertEqual(serializer.errors, {})


class TestStrictBooleanField(unittest.TestCase):

    class StubDFVStrictBooleanFieldNonNull(Serializer):
        active = BooleanField()

    class StubDFVStrictBooleanFieldNonNullable(Serializer):
        active = BooleanField(allow_null=True)

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
        for invalid in invalid_data:
            serializer = self.StubDFVStrictBooleanFieldNonNull(data=invalid)
            self.assertFalse(serializer.is_valid())
            self.assertEqual({}, serializer.validated_data)
            self.assertEqual(serializer.errors["active"][0],
                             ErrorDetail("Must be a valid boolean.", "invalid"))

    def test_it_when_None_is_passed(self):
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
        self.assertEqual(serializer.validated_data["active"], None)

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
            self.assertEqual(
                serializer.validated_data["active"], valid["active"])
            self.assertEqual(serializer.errors, {})
