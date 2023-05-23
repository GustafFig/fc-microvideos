# pylint: disable=no-member,protected-access
import unittest

import pytest
from django.utils import timezone
from django.db import models

from django_app.category.models import CategoryModel


@pytest.mark.django_db()
class TestCategoryModelInt(unittest.TestCase):

    def test_table_name(self):
        table_name = CategoryModel._meta.db_table
        self.assertEqual(table_name, 'categories')

        fields_name = [field.name for field in CategoryModel._meta.fields]
        self.assertListEqual(
            fields_name,
            ["id", "name", "description", "is_active", "created_at"]
        )
        id_field: models.UUIDField = CategoryModel.id.field
        self.assertIsInstance(id_field, models.UUIDField)
        self.assertTrue(id_field.primary_key)
        self.assertIsNone(id_field.db_column)
        self.assertTrue(id_field.editable)

    def test_create_category(self, ):
        arrange = {
            "id": 'bee01e76-f8fc-11ed-be56-0242ac120002',
            "name": 'Movie',
            "description": None,
            "is_active": True,
            "created_at": timezone.now(),
        }
        category = CategoryModel.objects.create(**arrange)
        self.assertEqual(category.id, arrange["id"])
        self.assertEqual(category.name, arrange["name"])
        self.assertEqual(category.description, arrange["description"])
        self.assertEqual(category.is_active, arrange["is_active"])
        self.assertEqual(category.created_at, arrange["created_at"])
