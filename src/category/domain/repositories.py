
from .entities import Category
from abc import ABC

from __seedwork.domain.repositories import (
    SearchableRepositoryInterface,
    SearchParams as DefaultSearchParams,
    SearchResult as DefaultSearchResult,
)


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
    sortable_fields = ["name", "is_active", "created_at"]
    SearchParams = _SearchParams
    SearchResult = _SearchResult
