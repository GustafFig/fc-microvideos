from inspect import isabstract
from dataclasses import dataclass, is_dataclass
from typing import Optional
import unittest
from __seedwork.domain.entities import Entity

from __seedwork.domain.repositories import Filters, RepositoryInterface, InMemoryRepository, SearchParams
from __seedwork.domain.value_objects import UniqueEntityId


class TestRepositoryInterface(unittest.TestCase):

    def test_it_is_abc_class_for_methods(self):
        with self.assertRaises(TypeError, msg="Not raised") as err:
            RepositoryInterface()  # type: ignore
        self.assertEqual(
            err.exception.args[0],
            "Can't instantiate abstract class RepositoryInterface with abstract "
            "methods delete, find_all, find_by_id, insert, update"
        )


@dataclass(slots=True, kw_only=True, frozen=True)
class StubEntity(Entity):
    name: str


class StubInMemoryRepository(InMemoryRepository[StubEntity]):
    """Defines a stub class for test InMemoryRepository"""


class TestInMemoryRepository(unittest.TestCase):

    repo: StubInMemoryRepository

    def setUp(self) -> None:
        self.repo = StubInMemoryRepository()

    def test_it_is_a_dataclass(self):
        self.assertTrue(is_dataclass(InMemoryRepository))

    def test_it_can_save_an_item(self):
        entity = StubEntity(name="Teste")
        self.repo.insert(entity)
        self.assertListEqual(self.repo.items, [entity])

    def test_it_can_save_many_items_iteratively(self):
        entities = list(map(lambda name: StubEntity(
            name=name), ["Teste1", "Teste2", "Teste3"]))
        for entity in entities:
            self.repo.insert(entity)

        self.assertListEqual(self.repo.items, entities)

    def test_it_can_retrieve_an_item(self):
        entities = list(map(lambda name: StubEntity(
            name=name), ["Teste1", "Teste2", "Teste3"]))
        for entity in entities:
            self.repo.insert(entity)

        self.assertEqual(self.repo.find_by_id(entities[0].id), entities[0])

    def test_it_can_retrieve_all_items(self):
        entities = list(map(lambda name: StubEntity(
            name=name), ["Teste1", "Teste2", "Teste3"]))
        for entity in entities:
            self.repo.insert(entity)

        self.assertListEqual(self.repo.find_all(), entities)

    def test_it_can_remove_an_item(self):
        entities = list(map(lambda name: StubEntity(
            name=name), ["Teste1", "Teste2", "Teste3"]))
        for entity in entities:
            self.repo.insert(entity)

        self.repo.delete(entities[0])
        self.assertEqual(self.repo.items, entities[1:])

    def test_it_can_update_an_item(self):
        entities = list(map(lambda name: StubEntity(
            name=name), ["Teste1", "Teste2", "Teste3"]))
        for entity in entities:
            self.repo.insert(entity)

        entity = StubEntity(unique_entity_id=UniqueEntityId(
            entities[0].id), name="UpdatedName")
        self.repo.update(entity)
        entity1 = self.repo.find_by_id(entities[0].id)
        self.assertTrue(entity1)
        self.assertEqual(entity1.name, "UpdatedName")  # type: ignore


class TestSearchParams(unittest.TestCase):

    def test_props_annotations(self):
        self.assertEqual(SearchParams.__annotations__, {
            'page': Optional[int],
            'per_page': Optional[int],
            'sort': Optional[str],
            'sort_dir': Optional[str],
            'filters': Optional[Filters]
        })

    def test_page_prop(self):
        params = SearchParams()
        self.assertEqual(params.page, 1)

        arrange = [
            {'page': None, 'expected': 1},
            {'page': "", 'expected': 1},
            {'page': "fake", 'expected': 1},
            {'page': 0, 'expected': 1},
            {'page': -1, 'expected': 1},
            {'page': "0", 'expected': 1},
            {'page': "-1", 'expected': 1},
            {'page': 5.5, 'expected': 5},
            {'page': True, 'expected': 1},
            {'page': False, 'expected': 1},
            {'page': {}, 'expected': 1},
            {'page': 1, 'expected': 1},
            {'page': 2, 'expected': 2},
        ]

        for i in arrange:
            params = SearchParams(page=i['page'])
            self.assertEqual(params.page, i['expected'])

    def test_per_page_prop(self):
        params = SearchParams()
        self.assertEqual(params.per_page, 15)

        arrange = [
            {'per_page': None, 'expected': 15},
            {'per_page': "", 'expected': 15},
            {'per_page': "fake", 'expected': 15},
            {'per_page': 0, 'expected': 15},
            {'per_page': -1, 'expected': 15},
            {'per_page': "0", 'expected': 15},
            {'per_page': "-1", 'expected': 15},
            {'per_page': 5.5, 'expected': 5},
            {'per_page': True, 'expected': 1},
            {'per_page': False, 'expected': 15},
            {'per_page': {}, 'expected': 15},
            {'per_page': 1, 'expected': 1},
            {'per_page': 2, 'expected': 2},
        ]

        for i in arrange:
            params = SearchParams(per_page=i['per_page'])
            self.assertEqual(params.per_page, i['expected'], i)

    def test_sort_prop(self):
        params = SearchParams()
        self.assertIsNone(params.sort)

        arrange = [
            {'sort': None, 'expected': None},
            {'sort': "", 'expected': None},
            {'sort': "fake", 'expected': 'fake'},
            {'sort': 0, 'expected': None},
            {'sort': -1, 'expected': '-1'},
            {'sort': "0", 'expected': '0'},
            {'sort': "-1", 'expected': '-1'},
            {'sort': 5.5, 'expected': '5.5'},
            {'sort': True, 'expected': 'True'},
            {'sort': False, 'expected': None},
            {'sort': {}, 'expected': None},
        ]

        for i in arrange:
            params = SearchParams(sort=i['sort'])
            self.assertEqual(params.sort, i['expected'], i)

    def test_sort_dir_prop(self):
        params = SearchParams()
        self.assertIsNone(params.sort_dir)

        params = SearchParams(sort=None)
        self.assertIsNone(params.sort_dir)

        params = SearchParams(sort="")
        self.assertIsNone(params.sort_dir)

        arrange = [
            {'sort_dir': None, 'expected': 'asc'},
            {'sort_dir': "", 'expected': 'asc'},
            {'sort_dir': "fake", 'expected': 'asc'},
            {'sort_dir': 0, 'expected': 'asc'},
            {'sort_dir': {}, 'expected': 'asc'},
            {'sort_dir': 'asc', 'expected': 'asc'},
            {'sort_dir': 'ASC', 'expected': 'asc'},
            {'sort_dir': 'desc', 'expected': 'desc'},
            {'sort_dir': 'DESC', 'expected': 'desc'},
        ]

        for i in arrange:
            params = SearchParams(sort='name', sort_dir=i['sort_dir'])
            self.assertEqual(params.sort_dir, i['expected'], i)

    def test_filter_prop(self):
        params = SearchParams()
        self.assertIsNone(params.filters)

        arrange = [
            {'filters': None, 'expected': None},
            {'filters': "", 'expected': None},
            {'filters': "fake", 'expected': 'fake'},
            {'filters': 0, 'expected': '0'},
            {'filters': -1, 'expected': '-1'},
            {'filters': "0", 'expected': '0'},
            {'filters': "-1", 'expected': '-1'},
            {'filters': 5.5, 'expected': '5.5'},
            {'filters': True, 'expected': 'True'},
            {'filters': False, 'expected': 'False'},
            {'filters': {}, 'expected': '{}'},
        ]

        for i in arrange:
            params = SearchParams(filters=i['filters'])
            self.assertEqual(params.filters, i['expected'], i)
