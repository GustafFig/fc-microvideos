from abc import ABC
from dataclasses import is_dataclass, FrozenInstanceError, dataclass
from unittest import TestCase
from unittest.mock import patch
import uuid

from src.__seedwork.domain.value_objects import UniqueEntityId, InvalidUUidException, ValueObject


@dataclass(frozen=True)
class StubProp(ValueObject):
    prop: str


@dataclass(frozen=True)
class StubTwoProps(ValueObject):
    prop1: str
    prop2: str


class TestValueObjectUnit(TestCase):
    def test_if_value_object_is_a_dataclass(self):
        self.assertTrue(is_dataclass(ValueObject))

    def test_if_value_object_is_a_abc(self):
        self.assertIsInstance(ValueObject(), ABC)

    def test_init_prop(self):
        vo1 = StubProp(prop="value")
        vo2 = StubTwoProps(prop1="value1", prop2="value2")
        self.assertEqual(vo1.prop, "value")
        self.assertEqual(vo2.prop1, "value1")

    def test_convert_to_string(self):
        vo1 = StubProp(prop="value")
        vo2 = StubTwoProps(prop1="value1", prop2="value2")

        self.assertEqual(vo1.prop, str(vo1))
        self.assertEqual('{"prop1": "value1", "prop2": "value2"}', str(vo2))

    def test_is_immutaboe(self):
        with self.assertRaises(FrozenInstanceError) as assert_error:
            vo1 = StubProp(prop="value")
            vo1.prop = "new value"  # type: ignore


class TestUniqueEntityIdUnit(TestCase):
    def test_if_is_a_dataclass(self):
        self.assertTrue(is_dataclass(UniqueEntityId))

    def test_throw_exception_when_uuid_is_invalid(self):
        with patch.object(
            UniqueEntityId,
            '_UniqueEntityId__validate',
            autospec=True,
            side_effect=UniqueEntityId._UniqueEntityId__validate,  # type: ignore
        ) as mock_validate:
            with self.assertRaises(InvalidUUidException) as assert_error:
                UniqueEntityId('fake id')
            mock_validate.assert_called_once()
            self.assertEqual(
                assert_error.exception.args[0], "ID must be a valid UUID")

    def test_accept_uuid_passed_in_constructor(self):
        with patch.object(
            UniqueEntityId,
            '_UniqueEntityId__validate',
            autospec=True,
            wraps=UniqueEntityId._UniqueEntityId__validate,  # type: ignore
        ) as mock_validate:
            value_object = UniqueEntityId(
                "0a189b24-f2fe-46d9-905a-9f0878cef77a")
            mock_validate.assert_called_once()
            self.assertEqual(
                value_object.id, "0a189b24-f2fe-46d9-905a-9f0878cef77a")

        uuid_value = uuid.uuid4()
        value_object = UniqueEntityId(uuid_value)  # type: ignore
        self.assertEqual(value_object.id, str(uuid_value))

    def test_generate_id_when_no_passed_id_in_constructor(self):
        with patch.object(
            UniqueEntityId,
            '_UniqueEntityId__validate',
            autospec=True,
            wraps=UniqueEntityId._UniqueEntityId__validate,  # type: ignore
        ) as mock_validate:
            value_object = UniqueEntityId()
            uuid.UUID(value_object.id)
            mock_validate.assert_called_once()

    def test_is_immutable(self):
        with self.assertRaises(FrozenInstanceError) as assert_error:
            value_object = UniqueEntityId()
            value_object.id = 'asdfasdf'  # type: ignore

    def test_convert_to_str(self):
        value_object = UniqueEntityId()
        self.assertEqual(value_object.id, str(value_object))
        self.assertEqual(value_object.id, repr(value_object))
