
import datetime as dt
import unittest

import pytest
from django.utils import timezone

from core.category.domain.entities import Category
from core.category.infra.mapper import CategoryDjangoModelMapper
from django_app.category.models import CategoryModel


@pytest.mark.django_db
class TestCategoryDjangoModelMapper(unittest.TestCase):

    def test_to_entity(self):
        created_at = timezone.now()
        model = CategoryModel(
            id='4e450808-bdd6-4fd0-9442-86bdc5b8bc5c',
            name="Movie",
            description="Movie Description",
            is_active=True,
            created_at=created_at,
        )

        entity = CategoryDjangoModelMapper.to_entity(model)
        self.assertEqual(entity.id, '4e450808-bdd6-4fd0-9442-86bdc5b8bc5c')
        self.assertEqual(entity.name, "Movie")
        self.assertEqual(entity.description, "Movie Description")
        self.assertEqual(entity.is_active, True)
        self.assertEqual(entity.created_at, created_at)

    def test_to_model(self):
        created_at = dt.datetime.now(dt.timezone.utc)
        entity = Category(
            unique_entity_id='4e450808-bdd6-4fd0-9442-86bdc5b8bc5c',
            name="Movie",
            description="Movie Description",
            is_active=True,
            created_at=created_at,
        )

        model = CategoryDjangoModelMapper.to_entity(entity)
        self.assertEqual(model.id, '4e450808-bdd6-4fd0-9442-86bdc5b8bc5c')
        self.assertEqual(model.name, "Movie")
        self.assertEqual(model.description, "Movie Description")
        self.assertEqual(model.is_active, True)
        self.assertEqual(model.created_at, created_at)
