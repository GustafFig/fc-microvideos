
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
    
    def _adjust_sort(self):
        sort = str(self.sort) if self.sort else 'created_at'
        object.__setattr__(self, "sort", sort)


class _SearchResult(DefaultSearchResult[CategoryTypeFilters, Category]):
    pass


class CategoryRepository(
    SearchableRepositoryInterface[_SearchParams, _SearchResult, Category],
    ABC,
):
    sortable_fields = ["name", "is_active", "created_at"]
    SearchParams = _SearchParams
    SearchResult = _SearchResult
