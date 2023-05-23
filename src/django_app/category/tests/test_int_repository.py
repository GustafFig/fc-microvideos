# pylint: disable=no-member
from typing import List
import unittest
import datetime as dt

from django.utils import timezone
from model_bakery import baker
from model_bakery.utils import seq
import pytest

from core.category.domain.entities import Category
from core.category.infra.mapper import CategoryDjangoModelMapper
from core.category.domain.repositories import CategoryRepository
from core.__seedwork.domain.exceptions import EntityNotFound
from core.__seedwork.domain.value_objects import UniqueEntityId
from django_app.category.models import CategoryModel
from django_app.category.repositories import CategoryDjangoRepository


@pytest.mark.django_db
class TestCategoryDjangoRepositoryInt(unittest.TestCase):

    repo: CategoryDjangoRepository

    def setUp(self):
        self.repo = CategoryDjangoRepository()

    def test_can_insert_a_category(self):
        category = Category(name="Movie")
        self.repo.insert(category)

        # Consultar é importante para sabermos se foi inserido no banco de dados corretamente
        model = CategoryModel.objects.get(pk=category.id)
        self.assertEqual(str(category.id), str(model.id))

        category2 = Category(name="Movie", description="Movie description", is_active=False)

        self.repo.insert(category2)
        model = CategoryModel.objects.get(pk=category2.id)
        self.assertEqual(str(category2.id), str(model.id))
        self.assertEqual(category2.name, model.name)
        self.assertEqual(category2.description, model.description)
        self.assertFalse(category2.is_active)

    def test_cannot_insert_the_same_category_by_id_multiple_times(self):
        pytest.skip()

    def test_can_find_by_id(self):
        category = Category(name="Movie")
        self.repo.insert(category)

        repo_category = self.repo.find_by_id(category.id)
        self.assertEqual(repo_category, category)

    def test_should_throw_test_if_not_found(self):
        with self.assertRaises(EntityNotFound) as err:
            self.repo.find_by_id("Not exists")
        self.assertEqual(err.exception.args[0], "Category not found")

        with self.assertRaises(EntityNotFound) as err:
            self.repo.find_by_id("c005735a-f9a6-11ed-be56-0242ac120002")
        self.assertEqual(err.exception.args[0], "Category not found")

        with self.assertRaises(EntityNotFound) as err:
            self.repo.find_by_id(UniqueEntityId("c005735a-f9a6-11ed-be56-0242ac120002"))
        self.assertEqual(err.exception.args[0], "Category not found")

    def test_find_all(self):
        self.assertListEqual([], self.repo.find_all(), "Should get empty data")
        models = baker.make(CategoryModel, _quantity=2)

        self.assertListEqual(
            self.repo.find_all(),
            [CategoryDjangoModelMapper.to_entity(model) for model in models],
        )

    def test_throw_not_found_exception_in_update(self):
        entity = Category(name="Movie")
        # não valida com uma string que não é um uuid porque passamos a entidade
        # ela já deveria passar uuids validos
        with self.assertRaises(EntityNotFound) as err:
            self.repo.update(entity)
        self.assertEqual(err.exception.args[0], "Category not found")

    def test_update(self):
        category = Category(name="Movie")
        self.repo.insert(category)
        category.update(name="Movie changed", description="Description changed")

        self.repo.update(category)
        model = CategoryModel.objects.get(pk=category.id)
        # não faz sentido atualizar apenas na categoria temos que ir no banco
        self.assertEqual(str(model.id), category.id)
        self.assertEqual(str(model.name), category.name)
        self.assertEqual(str(model.description), category.description)
        self.assertEqual(model.is_active, category.is_active)
        self.assertEqual(model.created_at, category.created_at)

    def test_throw_not_found_exception_in_delete(self):
        entity = Category(name="Movie")
        with self.assertRaises(EntityNotFound) as err:
            self.repo.delete(entity)
        self.assertEqual(err.exception.args[0], "Category not found")

    def test_delete(self):
        entity = Category(name="Movie")
        self.repo.insert(entity)
        self.assertEqual(1, len(CategoryModel.objects.all()))
        self.repo.delete(entity)

        self.assertEqual(0, len(CategoryModel.objects.all()))


@pytest.mark.django_db
class TestCategoryDjangoRepositorySearch(unittest.TestCase):

    repo: CategoryRepository

    def setUp(self) -> None:
        self.repo = CategoryDjangoRepository()

    def test_default_size_of_search_params(self):
        models = baker.make(
            CategoryModel,
            _quantity=16,
            name="Movie",
            description="Movie description",
            is_active=True,
            created_at=timezone.now(),
        )

        params = CategoryRepository.SearchParams()
        entities = self.repo.search(params)
        self.assertEqual(len(models), len(CategoryModel.objects.all()))
        self.assertEqual(15, len(entities.items))

    def test_search_when_params_is_empty(self):
        models: List = baker.make(
            CategoryModel,
            _quantity=16,
            created_at=seq(dt.datetime.now(), dt.timedelta(days=1))
        )
        models.reverse()

        search_result = self.repo.search(CategoryRepository.SearchParams())
        self.assertIsInstance(search_result, CategoryRepository.SearchResult)
        self.assertEqual(search_result, CategoryRepository.SearchResult(
            items=[
                CategoryDjangoModelMapper.to_entity(model)
                for model in models[:15]
            ],
            total=16,
            search_params=CategoryRepository.SearchParams(
                page=1,
                per_page=15,
                sort=None,
                sort_dir=None,
                filters=None,
            ),
        ))

    def test_search_applying_filter_and_paginate(self):
        default_props = {
            'description': None,
            'is_active': True,
            'created_at': timezone.now()
        }
        models = CategoryModel.objects.bulk_create([
            CategoryModel(
                id=UniqueEntityId().id,
                name='test',
                **default_props
            ),
            CategoryModel(
                id=UniqueEntityId().id,
                name='a',
                **default_props
            ),
            CategoryModel(
                id=UniqueEntityId().id,
                name='TEST',
                **default_props
            ),
            CategoryModel(
                id=UniqueEntityId().id,
                name='TeSt',
                **default_props
            )
        ])

        search_params = CategoryRepository.SearchParams(
            page=1, per_page=2, filters='E',
        )
        search_result = self.repo.search(search_params)
        self.assertEqual(search_result, CategoryRepository.SearchResult(
            items=[
                CategoryDjangoModelMapper.to_entity(models[0]),
                CategoryDjangoModelMapper.to_entity(models[2]),
            ],
            total=3,
            search_params=CategoryRepository.SearchParams(
                page=1,
                per_page=2,
                sort=None,
                sort_dir=None,
                filters='E',
            ),
        ))

    def test_search_applying_paginate_and_sort(self):
        default_props = {
            'description': None,
            'is_active': True,
            'created_at': timezone.now()
        }
        models = CategoryModel.objects.bulk_create([
            CategoryModel(
                id=UniqueEntityId().id,
                name='b',
                **default_props
            ),
            CategoryModel(
                id=UniqueEntityId().id,
                name='a',
                **default_props
            ),
            CategoryModel(
                id=UniqueEntityId().id,
                name='d',
                **default_props
            ),
            CategoryModel(
                id=UniqueEntityId().id,
                name='e',
                **default_props
            ),
            CategoryModel(
                id=UniqueEntityId().id,
                name='c',
                **default_props
            )
        ])

        arrange_by_asc = [
            {
                'search_params': CategoryDjangoRepository.SearchParams(
                    per_page=2,
                    sort='name'
                ),
                'search_output': CategoryDjangoRepository.SearchResult(
                    items=[
                        CategoryDjangoModelMapper.to_entity(models[1]),
                        CategoryDjangoModelMapper.to_entity(models[0]),
                    ],
                    total=5,
                    search_params=CategoryDjangoRepository.SearchParams(
                        page=1,
                        per_page=2,
                        sort='name',
                        sort_dir='asc',
                        filters=None
                    ),
                ),
            },
            {
                'search_params': CategoryDjangoRepository.SearchParams(
                    page=2,
                    per_page=2,
                    sort='name'
                ),
                'search_output': CategoryDjangoRepository.SearchResult(
                    items=[
                        CategoryDjangoModelMapper.to_entity(models[4]),
                        CategoryDjangoModelMapper.to_entity(models[2]),
                    ],
                    total=5,
                    search_params=CategoryDjangoRepository.SearchParams(
                        page=2,
                        per_page=2,
                        sort='name',
                        sort_dir='asc',
                        filters=None
                    )
                ),
            },
        ]

        for index, item in enumerate(arrange_by_asc):
            search_output = self.repo.search(item['search_params'])
            self.assertEqual(
                search_output,
                item['search_output'],
                f"The output using sort_dir asc on index {index} is different"
            )

        arrange_by_desc = [
            {
                'search_params': CategoryDjangoRepository.SearchParams(
                    per_page=2,
                    sort='name',
                    sort_dir='desc',
                ),
                'search_output': CategoryDjangoRepository.SearchResult(
                    items=[
                        CategoryDjangoModelMapper.to_entity(models[3]),
                        CategoryDjangoModelMapper.to_entity(models[2]),
                    ],
                    total=5,
                    search_params=CategoryDjangoRepository.SearchParams(
                        page=1,
                        per_page=2,
                        sort='name',
                        sort_dir='desc',
                        filters=None
                    )
                ),
            },
            {
                'search_params': CategoryDjangoRepository.SearchParams(
                    page=2,
                    per_page=2,
                    sort='name',
                    sort_dir='desc',
                ),
                'search_output': CategoryDjangoRepository.SearchResult(
                    items=[
                        CategoryDjangoModelMapper.to_entity(models[4]),
                        CategoryDjangoModelMapper.to_entity(models[0]),
                    ],
                    total=5,
                    search_params=CategoryDjangoRepository.SearchParams(
                        page=2,
                        per_page=2,
                        sort='name',
                        sort_dir='desc',
                        filters=None
                    )
                ),
            }
        ]

        for index, item in enumerate(arrange_by_desc):
            search_output = self.repo.search(item['search_params'])
            self.assertEqual(
                search_output,
                item['search_output'],
                f"The output using sort_dir desc on index {index} is different"
            )

    def test_search_applying_filter_sort_and_paginate(self):
        default_props = {
            'description': None,
            'is_active': True,
            'created_at': timezone.now()
        }
        models = CategoryModel.objects.bulk_create([
            CategoryModel(
                id=UniqueEntityId().id,
                name='test',
                **default_props
            ),
            CategoryModel(
                id=UniqueEntityId().id,
                name='a',
                **default_props
            ),
            CategoryModel(
                id=UniqueEntityId().id,
                name='TEST',
                **default_props
            ),
            CategoryModel(
                id=UniqueEntityId().id,
                name='e',
                **default_props
            ),
            CategoryModel(
                id=UniqueEntityId().id,
                name='TeSt',
                **default_props
            )
        ])

        search_result = self.repo.search(CategoryRepository.SearchParams(
            page=1,
            per_page=2,
            sort='name',
            sort_dir='asc',
            filters='TEST'
        ))
        self.assertEqual(search_result, CategoryDjangoRepository.SearchResult(
            items=[
                CategoryDjangoModelMapper.to_entity(models[2]),
                CategoryDjangoModelMapper.to_entity(models[4]),
            ],
            total=3,
            search_params=CategoryDjangoRepository.SearchParams(
                page=1,
                per_page=2,
                sort='name',
                sort_dir='asc',
                filters='TEST'
            )
        ))

        search_result = self.repo.search(CategoryRepository.SearchParams(
            page=2,
            per_page=2,
            sort='name',
            sort_dir='asc',
            filters='TEST'
        ))
        self.assertEqual(search_result, CategoryDjangoRepository.SearchResult(
            items=[
                CategoryDjangoModelMapper.to_entity(models[0]),
            ],
            total=3,
            search_params=CategoryDjangoRepository.SearchParams(
                page=2,
                per_page=2,
                sort='name',
                sort_dir='asc',
                filters='TEST',
            )
        ))
