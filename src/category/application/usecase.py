from dataclasses import asdict, dataclass
from typing import List, Optional

from __seedwork.application.usecases import UseCase
from __seedwork.domain.exceptions import EntityNotFound
from category.application.dto import CategoryOutput, CategoryOutputMapper
from category.domain.entities import Category
from category.domain.repositories import CategoryRepository


@dataclass(frozen=True, slots=True)
class CreateCategoryUseCase(UseCase):
    # usar uma class por caso de uso é ruim porque fere o solid
    # Claro que se você garantir que os métodos tão segregados o efeito é o quse o mesmo.
    # Mas as dependencias de um pode interferir em outro, ex: instanciação na factory

    # E se usar metodos compartilhados ai acaba com o S de Solid
    # Abstracao de repeticao casos de uso, usa um helper mixim

    # um caso de uso não pode extender do outro? Não, porque eles podem mudar diferente

    # init without dataclass
    # def __init__(self, repo) -> None:
    #    self.repo: CategoryRepository = repo
    repo: CategoryRepository

    def execute(self, input_param: 'Input') -> 'Output':
        raise NotImplementedError()

    # with the __call__ is an python specific way
    def __call__(self, input_param: 'Input') -> 'Output':
        category = Category(
            name=input_param.name,
            description=input_param.description,
            is_active=bool(input_param.is_active),
        )
        self.repo.insert(category)
        return self.Output(
            id=category.id,
            name=category.name,
            description=category.description,
            is_active=category.is_active,
            created_at=category.created_at,
        )

    # Bonderies
    # input e output
    # using inner class because:
    #   when use Input it alwayt with CreateCategory, and CreateCategoty always uses Input
    #   same with Category
    @dataclass(slots=True, frozen=True)
    class Input:
        name: str
        description: Optional[str]
        is_active: Optional[bool]

    @dataclass(slots=True, frozen=True)
    class Output(CategoryOutput):
        pass


@dataclass(slots=True, frozen=True)
class GetCategoryUseCase(UseCase):

    repo: CategoryRepository

    def __call__(self, input_param: 'Input') -> 'Output':
        if category := self.repo.find_by_id(input_param.id):
            return self.Output(
                id=category.id,
                name=category.name,
                description=category.description,
                is_active=category.is_active,
                created_at=category.created_at,
            )

        raise EntityNotFound(Category)

    @dataclass(slots=True, frozen=True)
    class Input:
        id: str  # pylint: disable=invalid-name

    @dataclass(slots=True, frozen=True)
    class Output(CategoryOutput):
        pass


@dataclass(slots=True, frozen=True)
class ListCategoriesUseCase(UseCase):

    repo: CategoryRepository

    def __call__(self, input_param: 'Input') -> 'Output':
        search_params = self.repo.SearchParams(**asdict(input_param))
        result = self.repo.search(search_params)
        items = map(CategoryOutputMapper.to_output, result.items)
        return self.Output(
            items=list(items),
            total=result.total,
            last_page=result.last_page,
            page=result.search_params.page,
            per_page=result.search_params.per_page,
            sort=result.search_params.sort,
            sort_dir=result.search_params.sort_dir,
        )

    @dataclass(slots=True, frozen=True)
    class Input:
        page: int
        per_page: int
        sort: str
        sort_dir: str

    @dataclass(slots=True, frozen=True)
    class Output:
        items: List[CategoryOutput]
        total: int
        last_page: int
        page: int
        per_page: int
        sort: Optional[str]
        sort_dir: Optional[str]
