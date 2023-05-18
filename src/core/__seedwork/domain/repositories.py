"""
    Interfaces that define how others apps layers talk save and recue info to the domain
"""

import math
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Generic, List, Optional, TypeVar

from core.__seedwork.domain.value_objects import UniqueEntityId

from .entities import Entity

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
    def find_by_id(self, entity_id: str | UniqueEntityId) -> Optional[ET]:
        raise NotImplementedError()

    @abstractmethod
    def find_all(self) -> List[ET]:
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
                return None  # True
        return None  # False

    def delete(self, entity: ET) -> None:
        for index, repo_entity in enumerate(self.items):
            if repo_entity.id == entity.id:
                self.items.pop(index)
                break

    def find_all(self) -> List[ET]:
        return list(self.items)

    def find_by_id(self, entity_id: str | UniqueEntityId) -> Optional[ET]:
        for repo_entity in self.items:
            if repo_entity.id == str(entity_id):
                return repo_entity
        return None


Filters = TypeVar("Filters", str, Any)


@dataclass(frozen=True, kw_only=True, slots=True)
class SearchParams(Generic[Filters], ABC):

    page: int = 1
    per_page: int = 15
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
        default = self._get_field_default("page")
        page = self._convert_int(self.page, default)
        if page <= 0:
            page = default
        object.__setattr__(self, "page", page)

    def _adjust_page_size(self):
        default = self._get_field_default("per_page")
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
        filters = str(
            self.filters) if self.filters is not None and self.filters != "" else None
        object.__setattr__(self, "filters", filters)

    def _get_field_default(self, field_name: str) -> Any:
        return self.__dataclass_fields__[field_name].default  # pylint: disable=no-member

    @classmethod
    def get_field_default(cls, field_name: str) -> Any:
        return cls.__dataclass_fields__[field_name].default  # pylint: disable=no-member

@dataclass(frozen=True, slots=True, kw_only=True)
class SearchResult(Generic[Filters, ET], ABC):
    """
        Study Note: here I passed SearchParams as an dependency of search result.
        It is not exaclity a problem but in general it's better to have the more flexible code
        A general (flexible) rule would be make use Inherit to make the coupling, not the typing.
        So the "ABC domain" uses some kind of "Atomic design" with a high flexible behaviour
        stiffened by the domain's implementation
    """

    items: List[ET]
    total: int
    last_page: int = field(init=False)
    search_params: SearchParams[Filters]

    def __post_init__(self, ):
        object.__setattr__(self, 'last_page', math.ceil(
            self.total / self.search_params.per_page))

    def to_dict(self):
        return {
            'items': self.items,
            'total': self.total,
            'current_page': self.search_params.page,
            'per_page': self.search_params.per_page,
            'last_page': self.last_page,
            'sort': self.search_params.sort,
            'sort_dir': self.search_params.sort_dir,
            'filters': self.search_params.filters,
        }


Input = TypeVar('Input')
Output = TypeVar('Output')


class SearchableRepositoryInterface(
    Generic[Input, Output, ET],
    RepositoryInterface[ET],
    ABC,
):
    """
    Study Note: pass SearchParams[Filters] is not good, because I am going to need to passe
        SearchParams[SomeType] through all app. So it's better to receive
        some definables'n aggregate Input and Output.
        With that the class get a Bonus of having others inputs and outputs types for searching
    """

    sortable_fields: List[str] = []

    @abstractmethod
    def search(self, params: Input) -> Output:
        raise NotImplementedError()


class InMemorySearchableRepositoryInterface(
    Generic[Filters, ET],
    SearchableRepositoryInterface[SearchParams[Filters],
                                  SearchResult[Filters, ET], ET],
    InMemoryRepository[ET],
    ABC,
):
    """
    Study Note: Here the SearchParams and SearchResult are defined because search is implemented
        using type like it. So it's good to pass it in generic of more flexible base class
        and method's typing.
    """

    def search(self, params: SearchParams[Filters]) -> SearchResult[Filters, ET]:
        items_filtered = self._apply_filter(self.items, params.filters)
        items_sorted = self._apply_sort(
            items_filtered, params.sort, params.sort_dir)
        items_paginated = self._apply_paginate(
            items_sorted, params.page, params.per_page)

        return SearchResult(
            items=items_paginated,
            total=len(items_filtered),
            search_params=params,
        )

    @abstractmethod
    def _apply_filter(self, items: List[ET], filter_param: Filters | None) -> List[ET]:
        raise NotImplementedError()

    def _apply_sort(self, items: List[ET], sort: str | None, sort_dir: str | None) -> List[ET]:
        if sort and sort in self.sortable_fields:
            is_reverse = sort_dir == 'desc'
            return sorted(items, key=lambda item: getattr(item, sort), reverse=is_reverse)
        return items

    def _apply_paginate(self, items: List[ET], page: int, per_page: int) -> List[ET]:
        start = (page - 1) * per_page
        limit = start + per_page
        return items[start:limit]
