from typing import List, Optional

from __seedwork.domain.repositories import \
    InMemorySearchableRepositoryInterface
from category.domain.entities import Category
from category.domain.repositories import (CategoryRepository,
                                          CategoryTypeFilters)


class InMemoryCategoryRepository(
    CategoryRepository,
    InMemorySearchableRepositoryInterface[CategoryTypeFilters, Category]
):

    def _apply_filter(
        self,
        items: List[Category],
        filter_param: Optional[CategoryTypeFilters],
    ) -> List[Category]:
        if filter_param:
            filtering = filter(
                lambda item: filter_param in item.name.lower(),
                items,
            )
            return list(filtering)
        return items

    def _apply_sort(
        self,
        items: List[Category],
        sort: str | None,
        sort_dir: str | None
    ) -> List[Category]:
        return sorted(
            items,
            key=lambda item: getattr(item, sort or "created_at"),
            reverse=sort_dir == 'desc'
        )
