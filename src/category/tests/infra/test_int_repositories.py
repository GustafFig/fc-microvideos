import datetime
import unittest

from category.domain.entities import Category
from category.infra.repositories import InMemoryCategoryRepository


class TestInMemoryCategoryRepository(unittest.TestCase):

    def setUp(self) -> None:
        self.repo = InMemoryCategoryRepository()

    def test_it_can_save_an_entity(self):
        self.repo.insert(Category(name="Test1"))
        self.assertEqual(len(self.repo.items), 1)

    def test_it_can_save_an_entity_even_already_populated(self):
        self.repo.insert(Category(name="Test1"))
        self.assertEqual(len(self.repo.items), 1)

        self.repo.insert(Category(name="Test2"))
        self.assertEqual(len(self.repo.items), 2)

        self.repo.insert(Category(name="Test3"))
        self.assertEqual(len(self.repo.items), 3)

    def test_it_can_find_by_id(self):
        categories = [
            Category(name="Test1"),
            Category(name="Test2"),
            Category(name="Test3"),
        ]
        for category in categories:
            self.repo.insert(category)

        category = self.repo.find_by_id(categories[0].id)
        self.assertEqual(category, categories[0])

        category = self.repo.find_by_id(categories[1].id)
        self.assertEqual(category, categories[1])

    def test_it_can_find_all(self):
        categories = [
            Category(name="Test1"),
            Category(name="Test2"),
            Category(name="Test3"),
        ]
        for category in categories:
            self.repo.insert(category)

        all_categories = self.repo.find_all()
        self.assertEqual(all_categories, self.repo.items)

    def test_it_can_delete_a_category(self):
        categories = [
            Category(name="Test1"),
            Category(name="Test2"),
            Category(name="Test3"),
        ]
        for category in categories:
            self.repo.insert(category)

        self.repo.delete(categories[0])
        self.assertEqual(self.repo.items, categories[1:])

        self.repo.delete(categories[1])
        self.assertEqual(self.repo.items, categories[2:])

    def test_it_can_delete_a_non_exists_category(self):
        categories = [
            Category(name="Test1"),
            Category(name="Test2"),
            Category(name="Test3"),
        ]
        for category in categories:
            self.repo.insert(category)

        self.repo.delete(Category(name="Test4"))
        self.assertEqual(self.repo.items, categories)

    def test_it_can_update_a_category(self):
        categories = [
            Category(name="Test1"),
            Category(name="Test2"),
            Category(name="Test3"),
        ]
        for category in categories:
            self.repo.insert(category)

        category = categories[0]
        category.update(name="Updated Name", description="Updated Description")

        self.repo.update(categories[0])
        repo_category = self.repo.find_by_id(category.id)

        self.assertEqual(category, repo_category)

    def test_it_can_search_categories_by_filtering_name(self):
        now = datetime.datetime.now()
        categories = list(map(
            lambda i: Category(
                name=f"Test{i}",
                description=f"Description{i}",
                created_at=now + datetime.timedelta(seconds=i),
            ),
            range(4),
        ))

        for category in categories:
            self.repo.insert(category)

        input_params = self.repo.SearchParams(
            page=1, per_page=2, filters="1"
        )
        output = self.repo.search(input_params)
        self.assertEqual(output.items, [categories[1]])
        self.assertEqual(output.last_page, 1)
        self.assertEqual(output.total, 1)

    def test_its_search_default_sort_by_created_at_in_desc_direction(self):
        now = datetime.datetime.now()
        categories = list(map(
            lambda i: Category(
                name=f"Test{i}",
                description=f"Description{i}",
                created_at=now + datetime.timedelta(seconds=-(i * 10)),
            ),
            range(4),
        ))

        for category in categories:
            self.repo.insert(category)

        input_params = self.repo.SearchParams(page=1, per_page=2)
        output = self.repo.search(input_params)
        self.assertEqual(output.items, categories[4:1:-1])
        self.assertEqual(output.last_page, 2)
        self.assertEqual(output.total, 4)
