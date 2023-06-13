from dataclasses import dataclass
from typing import Generic, List, TypeVar

from core.__seedwork.domain.repositories import SearchResult

Item = TypeVar('Item')

@dataclass(frozen=True, slots=True)
class PaginationOutput(Generic[Item]):
    items: List[Item]
    total: int
    page: int
    per_page: int
    last_page: int


Output = TypeVar('Output', bound=PaginationOutput)


@dataclass(frozen=True, slots=True)
class PaginationOutputMapper:
    output_child: Output

    @staticmethod
    def from_child(output_child: Output):
        return PaginationOutputMapper(output_child)

    def to_output(self, items: List[Item], result: SearchResult) -> PaginationOutput[Item]:
        return self.output_child(
            items=items,
            total=result.total,
            page=result.search_params.page,
            per_page=result.search_params.per_page,
            last_page=result.last_page
        )
