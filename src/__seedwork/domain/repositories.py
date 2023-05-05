"""
    Interfaces that define how others apps layers talk save and recue info to the domain
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from __seedwork.domain.value_objects import UniqueEntityId
from .entities import Entity
from typing import Generic, Optional, TypeVar, List

ET = TypeVar("ET", bound=Entity)


class RepositoryInterface(Generic[ET], ABC):

    @abstractmethod
    def insert(self, entity: ET) -> None:
        raise NotImplementedError()
    
    @abstractmethod
    def update(self, entity: ET) -> None:
        raise NotImplementedError()
    
    @abstractmethod
    def delete(self, entity: ET) -> None:
        raise NotImplementedError()
    
    @abstractmethod
    def find_by_id(self, id: str | UniqueEntityId) -> Optional[ET]:
        raise NotImplementedError()

    @abstractmethod
    def find_all(self, id) -> List[ET]:
        raise NotImplementedError()


@dataclass
class InMemoryRepository(RepositoryInterface[ET], ABC):

    items: List[ET] = field(default_factory=lambda: [])

    def insert(self, entity: ET) -> None:
        self.items.append(entity)

    def update(self, entity: ET) -> None:
        """Returns True if updated the entity or False, if it have not been found"""
        for index, repo_entity in enumerate(self.items):
            if repo_entity.id == entity.id:
                self.items[index] = entity
                return None #True
        return None #False

    def delete(self, entity: ET) -> None:
        for index, repo_entity in enumerate(self.items):
            if repo_entity.id == entity.id:
                self.items.pop(index)
                break

    def find_all(self) -> List[ET]:
        return list(self.items)

    def find_by_id(self, id: str | UniqueEntityId) -> Optional[ET]:
        for repo_entity in self.items:
            if repo_entity.id == str(id):
                return repo_entity
