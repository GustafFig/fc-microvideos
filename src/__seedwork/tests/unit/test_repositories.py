from inspect import isabstract
from dataclasses import dataclass, is_dataclass
import unittest
from __seedwork.domain.entities import Entity

from __seedwork.domain.repositories import RepositoryInterface, InMemoryRepository
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
        entities = list(map(lambda name: StubEntity(name=name), ["Teste1", "Teste2", "Teste3"]))
        for entity in entities:
            self.repo.insert(entity)

        self.assertListEqual(self.repo.items, entities)


    def test_it_can_retrieve_an_item(self):
        entities = list(map(lambda name: StubEntity(name=name), ["Teste1", "Teste2", "Teste3"]))
        for entity in entities:
            self.repo.insert(entity)

        self.assertEqual(self.repo.find_by_id(entities[0].id), entities[0])

    def test_it_can_retrieve_all_items(self):
        entities = list(map(lambda name: StubEntity(name=name), ["Teste1", "Teste2", "Teste3"]))
        for entity in entities:
            self.repo.insert(entity)

        self.assertListEqual(self.repo.find_all(), entities)

    def test_it_can_remove_an_item(self):
        entities = list(map(lambda name: StubEntity(name=name), ["Teste1", "Teste2", "Teste3"]))
        for entity in entities:
            self.repo.insert(entity)

        self.repo.delete(entities[0])
        self.assertEqual(self.repo.items, entities[1:])

    def test_it_can_update_an_item(self):
        entities = list(map(lambda name: StubEntity(name=name), ["Teste1", "Teste2", "Teste3"]))
        for entity in entities:
            self.repo.insert(entity)

        entity = StubEntity(unique_entity_id=UniqueEntityId(entities[0].id), name="UpdatedName")
        self.repo.update(entity)
        entity1 = self.repo.find_by_id(entities[0].id)
        self.assertTrue(entity1)
        self.assertEqual(entity1.name, "UpdatedName") # type: ignore
