from os import name
from typing import Optional
import unittest
from unittest.mock import patch
from __seedwork.domain.exceptions import EntityNotFound

from category.application.usecase import CreateCategoryUseCase, GetCategoryUseCase
from category.domain.entities import Category
from category.infra.repositories import InMemoryCategoryRepository


class TestCreateCategory(unittest.TestCase):

    def setUp(self) -> None:
        self.repo = InMemoryCategoryRepository()

    def test_create_category_can_create_a_category(self):
        # not using InMemoryRepository can be used here. To explain I gonna use an supposition
        # if python weren't have unittest.mock you would create a mock class with InMemoryBehaviour.
        # Maybe you would create a class with some aspect of it to every moment you have
        # some aspect of it. So it can be used for unit

        # besides we have -> no disk, no network, only memory. this is important for unit tests
        create_category = CreateCategoryUseCase(self.repo)
        input_param = CreateCategoryUseCase.Input(
            name="Test1",
            description="Test2",
            is_active=False
        )
        with patch.object(self.repo, 'insert', wraps=self.repo.insert) as spy_repo:
            output = create_category(input_param)
            # good point with inMemoryRepository
            saved_item = self.repo.items[0]
            self.assertEqual(output, CreateCategoryUseCase.Output(
                id=saved_item.id,
                name="Test1",
                description="Test2",
                is_active=False,
                created_at=saved_item.created_at,
            ))
            spy_repo.assert_called_once()

    def test_input(self):
        self.assertEqual(CreateCategoryUseCase.Input.__annotations__, {
            'name': str,
            'description': Optional[str],
            'is_active': Optional[bool],
        })

    def test_can_get_category(self):
        categories = list(map(lambda name: Category(
            name=name), ("Cat1", "Cat2", "Cat3")))
        for category in categories:
            self.repo.insert(category)

        for category in categories:
            with patch.object(self.repo, 'find_by_id', wraps=self.repo.find_by_id) as find_by_id:
                usecase = GetCategoryUseCase(self.repo)
                input_param = GetCategoryUseCase.Input(id=category.id)
                output = usecase(input_param)
                expected_output = GetCategoryUseCase.Output(
                    id=category.id,
                    name=category.name,
                    description=category.description,
                    is_active=category.is_active,
                    created_at=category.created_at,
                )
                self.assertEqual(output, expected_output,
                                 f"Output is diferent in category={category.name}")
                find_by_id.assert_called_once_with(category.id)

    def test_raise_when_category_not_found(self):
        categories = list(map(lambda name: Category(
            name=name), ("Cat1", "Cat2", "Cat3")))
        for category in categories:
            self.repo.insert(category)

        with patch.object(self.repo, 'find_by_id', wraps=self.repo.find_by_id) as find_by_id:
            usecase = GetCategoryUseCase(self.repo)
            input_param = GetCategoryUseCase.Input(id="not_an_valid_id")
            with self.assertRaises(EntityNotFound) as err:
                usecase(input_param)
            self.assertEqual(err.exception.args[0], 'Category not found')
            find_by_id.assert_called_once_with("not_an_valid_id")
