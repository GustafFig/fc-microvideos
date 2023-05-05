"""
    Interfaces that define how others apps layers talk save and recue info to the domain
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field, fields

from __seedwork.domain.value_objects import UniqueEntityId
from .entities import Entity
from typing import Any, Generic, Optional, TypeVar, List

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

Filters = TypeVar("Filters", str, Any)
@dataclass(frozen=True, kw_only=True, slots=True)
class SearchParams(Generic[Filters], ABC):

    page: Optional[int] = 1
    per_page: Optional[int] = 15
    sort: Optional[str] = None
    sort_dir: Optional[str] = None
    filters: Optional[Filters] = None

    def __post_init__(self):
        self._adjust_page()
        self._adjust_page_size()
        self._adjust_sort()
        self._adjust_sort_dir()
        self._normalize_filter()

    def _adjust_page(self):
        default = self.__dataclass_fields__["page"].default
        page = self._convert_int(self.page, default)
        if page <= 0:
            page = default
        object.__setattr__(self, "page", page)

    def _adjust_page_size(self):
        default = self.__dataclass_fields__["per_page"].default
        per_page = self._convert_int(self.per_page, default)
        if per_page <= 0:
            per_page = default
        object.__setattr__(self, "per_page", per_page)

    def _adjust_sort(self):
        sort = str(self.sort) if self.sort else None
        object.__setattr__(self, "sort", sort)
    
    def _adjust_sort_dir(self):
        if self.sort:
            sort_dir = str(self.sort_dir).lower()
            sort_dir = sort_dir if sort_dir in {"asc", "desc"} else "asc"
        else:
            sort_dir = None
        object.__setattr__(self, "sort_dir", sort_dir)

    def _convert_int(self, value, default):
        try:
            return int(value)
        except (TypeError, ValueError):
            return default

    def _normalize_filter(self):
        filters = str(self.filters) if self.filters is not None and self.filters != "" else None
        object.__setattr__ (self, "filters", filters)
