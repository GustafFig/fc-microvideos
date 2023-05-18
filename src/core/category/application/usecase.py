from dataclasses import asdict, dataclass
from typing import List, Optional

from core.__seedwork.application.usecases import UseCase
from core.__seedwork.domain.exceptions import EntityNotFound, MissingParameter
from core.category.application.dto import CategoryOutput, CategoryOutputMapper
from core.category.domain.entities import Category
from core.category.domain.repositories import CategoryRepository


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
        description: Optional[str] = Category.get_field('description').default
        is_active: Optional[bool] = Category.get_field('is_active').default

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
        items = map(CategoryOutputMapper.without_child().to_output, result.items)
        return self.Output(
            items=list(items),
            total=result.total,
            last_page=result.last_page,
            page=result.search_params.page,
            per_page=result.search_params.per_page,
        )

    @dataclass(slots=True, frozen=True)
    class Input:
        page: int = CategoryRepository.SearchParams.get_field_default('page')
        per_page: int = CategoryRepository.SearchParams.get_field_default('per_page')
        sort: str = CategoryRepository.SearchParams.get_field_default('sort')
        sort_dir: str = CategoryRepository.SearchParams.get_field_default('sort_dir')
        filters: str = CategoryRepository.SearchParams.get_field_default('filters')

    @dataclass(slots=True, frozen=True)
    class Output:
        items: List[CategoryOutput]
        total: int
        last_page: int
        page: int
        per_page: int


@dataclass(frozen=True, slots=True)
class UpdateCategoryUseCase(UseCase):

    repo: CategoryRepository

    def __call__(self, input_param: 'Input') -> 'Output':
        category = self.repo.find_by_id(entity_id=input_param.id)

        if not category:
            raise EntityNotFound(Category)

        if category.is_active and not input_param.is_active:
            category.inactivate()
        elif not category.is_active and input_param.is_active:
            category.activate()

        category.update(name=input_param.name, description=input_param.description)

        self.repo.update(category)

        return CategoryOutputMapper().to_output(category)

    @dataclass(frozen=True, slots=True)
    class Input:
        id: str  # pylint: disable=invalid-name
        name: str
        description: str
        is_active: Optional[bool] = Category.get_field('is_active').default

    class Output(CategoryOutput):
        pass


@dataclass(frozen=True, slots=True)
class DeleteCategoryUseCase(UseCase):

    repo: CategoryRepository

    def __call__(self, input_param: 'Input') -> 'Output':
        if not input_param.id:
            raise MissingParameter("id")

        category = self.repo.find_by_id(input_param.id)
        if not category:
            return self.Output()

        self.repo.delete(category)
        return self.Output()

    @dataclass(frozen=True, slots=True)
    class Input:
        id: str  # pylint: disable=invalid-name

    @dataclass(frozen=True, slots=True)
    class Output:
        pass
