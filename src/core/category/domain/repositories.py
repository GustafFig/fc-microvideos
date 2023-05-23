
from abc import ABC

from core.__seedwork.domain.repositories import SearchableRepositoryInterface
from core.__seedwork.domain.repositories import SearchParams as DefaultSearchParams
from core.__seedwork.domain.repositories import SearchResult as DefaultSearchResult

from .entities import Category


class CategoryTypeFilters(str):
    pass


class _SearchParams(DefaultSearchParams[CategoryTypeFilters]):
    pass


class _SearchResult(DefaultSearchResult[CategoryTypeFilters, Category]):
    pass


class CategoryRepository(
    SearchableRepositoryInterface[_SearchParams, _SearchResult, Category],
    ABC,
):
    """
        Not InMemory because it is in the domain.
    """
    sortable_fields = ["name", "created_at"]
    SearchParams = _SearchParams
    SearchResult = _SearchResult
