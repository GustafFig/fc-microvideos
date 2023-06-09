import datetime as dt
import unittest
from dataclasses import is_dataclass
from unittest.mock import patch

from core.category.domain.entities import Category


@patch.object(Category, 'validate')
class TestCategory(unittest.TestCase):

    def test_if_category_is_a_dataclass(self, _validator):
        self.assertTrue(is_dataclass(Category))

    def test_category_constructor(self, _validator):
        category = Category(name="Cat1")
        self.assertIsNotNone(category)
        self.assertEqual(category.name, "Cat1")
        self.assertEqual(category.description, None)
        self.assertEqual(category.is_active, True)
        self.assertIsInstance(category.created_at, dt.datetime)

        created_at = dt.datetime.now() - dt.timedelta(days=-2)
        category = Category(name="Cat2", description="First1",
                            is_active=False, created_at=created_at)
        self.assertEqual(category.name, 'Cat2')
        self.assertEqual(category.is_active, False)
        self.assertEqual(category.description, "First1")
        self.assertEqual(category.created_at.timestamp(),
                         created_at.timestamp())

    def test_category_update(self, _validator):
        category = Category(name="Cat1")
        category.update(name="Cat2", description="Description")

        assert category.name == "Cat2"
        assert category.description == "Description"

        category.update(name="Cat3", description="Description3")
        assert category.name == "Cat3"
        assert category.description == "Description3"

    def test_category_activate(self, _validator):
        category = Category(name="Cat1", is_active=False)

        assert category.is_active is False
        category.activate()
        assert category.is_active is True
        category.activate()
        assert category.is_active is True

    def test_category_inactivate(self, _validator):
        category = Category(name="Cat1", is_active=True)

        assert category.is_active is True
        category.inactivate()
        assert category.is_active is False
        category.inactivate()
        assert category.is_active is False
