# pylint: disable=no-member
import unittest
import pytest

from django_app.category.models import CategoryModel
from django_app.category.repositories import CategoryDjangoRepository

from core.category.domain.entities import Category
from core.__seedwork.domain.exceptions import EntityNotFound


@pytest.mark.django_db
class TestCategoryDjangoRepositoryInt(unittest.TestCase):

    repo: CategoryDjangoRepository

    def setUp(self):
        self.repo = CategoryDjangoRepository()

    def test_can_insert_a_category(self):
        category = Category(name="Movie")
        self.repo.insert(category)

        # Consultar é importante para sabermos se foi inserido no banco de dados corretamente
        model = CategoryModel.objects.get(pk=category.id)
        self.assertEqual(str(category.id), str(model.id))

        category2 = Category(name="Movie", description="Movie description", is_active=False)

        self.repo.insert(category2)
        model = CategoryModel.objects.get(pk=category2.id)
        self.assertEqual(str(category2.id), str(model.id))
        self.assertEqual(category2.name, model.name)
        self.assertEqual(category2.description, model.description)
        self.assertFalse(category2.is_active)

    def test_cannot_insert_the_same_category_by_id_multiple_times(self):
        pytest.skip()

    def test_can_find_by_id(self):
        category = Category(name="Movie")
        self.repo.insert(category)

        repo_category = self.repo.find_by_id(category.id)
        self.assertEqual(repo_category, category)

    def test_should_throw_test_if_not_found(self):
        with self.assertRaises(EntityNotFound) as err:
            self.repo.find_by_id("Not exists")
        self.assertEqual(err.exception.args[0], "Category not found")

        with self.assertRaises(EntityNotFound) as err:
            self.repo.find_by_id("c005735a-f9a6-11ed-be56-0242ac120002")
        self.assertEqual(err.exception.args[0], "Category not found")

    def test_find_all(self):
        self.assertListEqual([], self.repo.find_all())

        category = Category(name="Movie")
        category2 = Category(name="Movie2")
        self.repo.insert(category)
        self.repo.insert(category2)

        self.assertListEqual(
            [category, category2],
            self.repo.find_all(),
        )
