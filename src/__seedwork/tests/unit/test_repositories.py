from inspect import isabstract
from dataclasses import dataclass, is_dataclass
from typing import List, Optional
import unittest
from __seedwork.domain.entities import Entity

from __seedwork.domain.repositories import (
    ET, Filters, InMemorySearchableRepositoryInterface, RepositoryInterface, InMemoryRepository, SearchParams, SearchResult, SearchableRepositoryInterface)
from __seedwork.domain.value_objects import UniqueEntityId
from sqlparse import filters


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
            'page': int,
            'per_page': int,
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


class TestSearchResult(unittest.TestCase):

    def test_props_annotations(self):
        self.assertEqual(SearchResult.__annotations__, {
            "items": List[ET],
            "total": int,
            "last_page": int,
            "search_params": SearchParams[Filters],
        })

    def test_last_page(self):
        entity = StubEntity(name='Teste1')
        data_list = [
            {"params": {"per_page": 15}, "result": {"total": 100}, "last_page": 7},
            {"params": {"per_page": 10}, "result": {"total": 100}, "last_page": 10},
            {"params": {"per_page": 10}, "result": {"total": 101}, "last_page": 11},
            {"params": {"per_page": 10}, "result": {"total": 109}, "last_page": 11},
        ]

        sp_props = {"page": 1}
        items = [entity]
        for data in data_list:
            search_result = SearchResult(
                items=items,
                total=data["result"]["total"],
                search_params=SearchParams(
                    **sp_props,
                    per_page=data["params"]["per_page"]
                )
            )

            self.assertEqual(search_result.last_page, data["last_page"])

    def test_to_dict(self):
        items = [StubEntity(name='Teste1')]

        search_result = SearchResult(
            items=items,
            total=100,
            search_params=SearchParams(
                page=3,
                per_page=20,
            )
        )
        self.assertEqual(search_result.to_dict(), {
            "items": items,
            "total": 100,
            "current_page": 3,
            "per_page": 20,
            "last_page": 5,
            "sort": None,
            "sort_dir": None,
            "filters": None,
        })


class TestSearchblaeRepositoryInterface(unittest.TestCase):

    def test_it_is_an_abstract_with_a_searchable_method(self):
        with self.assertRaises(TypeError) as err:
            SearchableRepositoryInterface()  # type: ignore
        self.assertEqual(
            err.exception.args[0],
            "Can't instantiate abstract class SearchableRepositoryInterface with abstract "
            "methods delete, find_all, find_by_id, insert, search, update"
        )


class StubInMemorySearchableRepository(
    InMemorySearchableRepositoryInterface[str, StubEntity]
):

    sortable_fields = ["name"]

    def _apply_filter(
        self,
        items: List[StubEntity], filter_param: Optional[str],
    ) -> List[StubEntity]:
        if filter_param:
            filter_obj = filter(
                lambda i: filter_param.lower() in i.name.lower(),
                items,
            )
            return list(filter_obj)
        return items


class TestInMemorySearchableRepository(unittest.TestCase):

    repo: StubInMemorySearchableRepository

    def setUp(self) -> None:
        self.repo = StubInMemorySearchableRepository()

    def test__apply_filter(self):
        items = [StubEntity(name='test')]
        # pylint: disable=protected-access
        result = self.repo._apply_filter(items, None)
        self.assertEqual(items, result)

        items = [
            StubEntity(name='test'),
            StubEntity(name='TEST'),
            StubEntity(name='fake'),
        ]

        # pylint: disable=protected-access
        result = self.repo._apply_filter(items, 'TEST')
        self.assertEqual([items[0], items[1]], result)

    def test__apply_sort(self):
        items = [
            StubEntity(name='b'),
            StubEntity(name='a'),
            StubEntity(name='c'),
        ]

        result = self.repo._apply_sort(items, 'name', 'asc')
        self.assertEqual([items[1], items[0], items[2]], result)

        result = self.repo._apply_sort(items, 'name', 'desc')
        self.assertEqual([items[2], items[0], items[1]], result)

    def test_apply_invalid_sort_field_should_ignore_it(self):
        items = [
            StubEntity(name='b'),
            StubEntity(name='a'),
            StubEntity(name='c'),
        ]
        result = self.repo._apply_sort(items, 'no_price', 'asc')
        self.assertEqual(items, result)

    def test__apply_paginate(self):
        items = [
            StubEntity(name='a'),
            StubEntity(name='b'),
            StubEntity(name='c'),
            StubEntity(name='d'),
            StubEntity(name='e'),
        ]

        result = self.repo._apply_paginate(items, 1, 2)
        self.assertEqual([items[0], items[1]], result)

        result = self.repo._apply_paginate(items, 2, 2)
        self.assertEqual([items[2], items[3]], result)

        result = self.repo._apply_paginate(items, 3, 2)
        self.assertEqual([items[4]], result)

        result = self.repo._apply_paginate(items, 4, 2)
        self.assertEqual([], result)

    def test_search_when_params_is_empty(self):
        entity = StubEntity(name='a')
        items = [entity] * 16
        self.repo.items = items

        search_params = SearchParams()
        result = self.repo.search(search_params)
        self.assertEqual(result, SearchResult(
            items=[entity] * 15,
            total=16,
            search_params=search_params
        ))
        self.assertEqual(
            search_params,
            result.search_params,
            "search method should repass search params result"
        )

    def test_search_applying_filter_and_paginate(self):
        items = [
            StubEntity(name='test'),
            StubEntity(name='a'),
            StubEntity(name='TEST'),
            StubEntity(name='TeSt'),
        ]
        self.repo.items = items

        search_params = SearchParams(
            page=1, per_page=2, filters='TEST'
        )
        result = self.repo.search(search_params)
        self.assertEqual(result, SearchResult(
            items=[items[0], items[2]],
            total=3,
            search_params=search_params,
        ))

        search_params = SearchParams(
            page=2, per_page=2, filters='TEST'
        )
        result = self.repo.search(search_params)
        self.assertEqual(result, SearchResult(
            items=[items[3]],
            total=3,
            search_params=search_params,
        ))

        search_params = SearchParams(
            page=3, per_page=2, filters='TEST'
        )
        result = self.repo.search(search_params)
        self.assertEqual(result, SearchResult(
            items=[],
            total=3,
            search_params=search_params,
        ))

    def test_search_applying_sort_and_paginate(self):
        items = [
            StubEntity(name='b'),
            StubEntity(name='a'),
            StubEntity(name='d'),
            StubEntity(name='e'),
            StubEntity(name='c'),
        ]
        self.repo.items = items

        arrange_by_asc = [
            {
                'input': SearchParams(page=1, per_page=2, sort='name'),
                'output': dict(items=[items[1], items[0]], total=5),
            },
            {
                'input': SearchParams(page=2, per_page=2, sort='name'),
                'output': dict(items=[items[4], items[2]], total=5),
            },
            {
                'input': SearchParams(page=3, per_page=2, sort='name'),
                'output': dict(items=[items[3]], total=5),
            }
        ]

        for index, item in enumerate(arrange_by_asc):
            result = self.repo.search(item['input'])
            self.assertEqual(
                result,
                SearchResult(**item['output'], search_params=item["input"]),
                f"The output using sort_dir asc on index {index} is different"
            )

        arrange_by_desc = [
            {
                'input': SearchParams(page=1, per_page=2, sort='name', sort_dir='desc'),
                'output': dict(items=[items[3], items[2]], total=5)
            },
            {
                'input': SearchParams(page=2, per_page=2, sort='name', sort_dir='desc'),
                'output': dict(items=[items[4], items[0]], total=5)
            },
            {
                'input': SearchParams(page=3, per_page=2, sort='name', sort_dir='desc'),
                'output': dict(items=[items[1]], total=5)
            }
        ]

        for index, item in enumerate(arrange_by_desc):
            result = self.repo.search(item['input'])
            self.assertEqual(
                result,
                SearchResult(**item['output'], search_params=item["input"]),
                f"The output using sort_dir desc on index {index} is different"
            )

    def test_search_applying_filter_and_sort_and_paginate(self):
        items = [
            StubEntity(name='test'),
            StubEntity(name='a'),
            StubEntity(name='TEST'),
            StubEntity(name='e'),
            StubEntity(name='TeSt'),
        ]
        self.repo.items = items

        test_list = [
            {
                'input': SearchParams(
                    page=1, per_page=2, sort="name", sort_dir="asc", filters="TEST"
                ),
                'output': dict(items=[items[2], items[4]], total=3)
            },
            {
                'input': SearchParams(
                    page=2, per_page=2, sort="name", sort_dir="asc", filters="TEST"
                ),
                'output': dict(items=[items[0]], total=3)
            },
        ]

        for index, item in enumerate(test_list):
            result = self.repo.search(item['input'])
            self.assertEqual(
                result,
                SearchResult(**item['output'], search_params=item["input"]),
                f"The output using sort and filter on index {index} is different"
            )
