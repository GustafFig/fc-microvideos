from dependency_injector import containers, providers
from core.category.application.usecase import (
    CreateCategoryUseCase,
    DeleteCategoryUseCase,
    GetCategoryUseCase,
    ListCategoriesUseCase,
    UpdateCategoryUseCase,
)
from core.category.infra.repositories import InMemoryCategoryRepository


class Container(containers.DeclarativeContainer):

    repository_category_in_memory = providers.Singleton(InMemoryCategoryRepository)

    use_case_category_create_category = providers.Singleton(
        CreateCategoryUseCase,
        repo=repository_category_in_memory,
    )

    use_case_category_list_category = providers.Singleton(
        ListCategoriesUseCase,
        repo=repository_category_in_memory,
    )

    use_case_category_get_category = providers.Singleton(
        GetCategoryUseCase,
        repo=repository_category_in_memory,
    )

    use_case_category_update_category = providers.Singleton(
        UpdateCategoryUseCase,
        repo=repository_category_in_memory,
    )

    use_case_category_delete_category = providers.Singleton(
        DeleteCategoryUseCase,
        repo=repository_category_in_memory,
    )
