from dataclasses import is_dataclass
import datetime as dt
import unittest

from category.domain.entities import Category


class TestCategory(unittest.TestCase):
    def test_if_category_is_a_dataclass(self):
        self.assertTrue(is_dataclass(Category))

    def test_category_constructor(self):
        category = Category(name="Cat1")
        self.assertEqual(category.name, "Cat1")
        self.assertEqual(category.description, None)
        self.assertEqual(category.is_active, True)
        self.assertIsInstance(category.created_at, dt.datetime)

        created_at = dt.datetime.now() - dt.timedelta(days=-2)
        category = Category(name="Cat2", description="First1", is_active=False, created_at=created_at)
        self.assertEqual(category.name, 'Cat2')
        self.assertEqual(category.is_active, False)
        self.assertEqual(category.description, "First1")
        self.assertEqual(category.created_at.timestamp(), created_at.timestamp())
