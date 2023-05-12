import unittest
from typing import Optional
from unittest.mock import patch
from __seedwork.application.usecases import UseCase

from __seedwork.domain.exceptions import EntityNotFound, MissingParameter, ValidationException
from category.application.dto import CategoryOutputMapper
from category.application.usecase import (CreateCategoryUseCase, DeleteCategoryUseCase,
                                          GetCategoryUseCase, UpdateCategoryUseCase)
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


class TestGetCategoryUseCase(unittest.TestCase):

    def setUp(self) -> None:
        self.repo = InMemoryCategoryRepository()

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
                expected_output = CategoryOutputMapper\
                    .with_child(GetCategoryUseCase.Output)\
                    .to_output(category)
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


class TestUpdateCategoryUseCase(unittest.TestCase):

    def setUp(self) -> None:
        self.repo = InMemoryCategoryRepository()

    def test_it_fail_with_name_is_to_long(self):
        category = Category(name="Test", description="Description")
        self.repo.insert(category)

        usecase = UpdateCategoryUseCase(self.repo)
        input_param = UpdateCategoryUseCase.Input(
            id=category.id,
            name="u" * 256,
            description="updated description",
        )
        with (
            patch.object(self.repo, 'update', wraps=self.repo.update) as repo_update,
            self.assertRaises(ValidationException) as err,
        ):
            usecase(input_param)
        self.assertEqual(err.exception.args[0], "Validation Error")
        self.assertTrue(err.exception.error.get('name'))
        self.assertEqual(
            err.exception.error['name'][0],
            'Ensure this field has no more than 255 characters.',
        )

        repo_update.assert_not_called()

    def test_name_cannot_be_none(self):
        category = Category(name="Test", description="Description")
        self.repo.insert(category)

        usecase = UpdateCategoryUseCase(self.repo)
        input_param = UpdateCategoryUseCase.Input(
            id=category.id,
            name=None,
            description="updated description",
        )
        with (
            patch.object(self.repo, 'update', wraps=self.repo.update) as repo_update,
            self.assertRaises(ValidationException) as err,
        ):
            usecase(input_param)
        self.assertEqual(err.exception.args[0], "Validation Error")
        self.assertTrue(err.exception.error.get('name'))
        self.assertEqual(
            err.exception.error['name'][0],
            'This field may not be null.',
        )

        repo_update.assert_not_called()

    def test_not_update_a_non_exists_category(self):
        usecase = UpdateCategoryUseCase(self.repo)
        input_param = UpdateCategoryUseCase.Input(
            id="NonExists", name="updated name", description="updated description",
        )
        with (
            patch.object(self.repo, 'find_by_id', wraps=self.repo.find_by_id) as repo_find_by_id,
            patch.object(self.repo, 'update', wraps=self.repo.update) as repo_update,
            self.assertRaises(EntityNotFound) as err,
        ):
            usecase(input_param)
        repo_find_by_id.assert_called_with(entity_id="NonExists")
        repo_update.assert_not_called()
        self.assertEqual(err.exception.args[0], "Category not found")

    def test_cannot_pass_invalid_types_to_input_name(self):
        category = Category(name="Test", description="Description")
        self.repo.insert(category)
        usecase = UpdateCategoryUseCase(self.repo)

        for name in [{}, 5, 5.5, [], set()]:
            input_param = UpdateCategoryUseCase.Input(
                id=category.id,
                name=name,
                description=category.description,
            )

            with (
                patch.object(self.repo, 'update', wraps=self.repo.update) as repo_update,
                self.assertRaises(ValidationException) as err,
            ):
                usecase(input_param)
            repo_update.assert_not_called()
            self.assertTrue(err.exception.error.get('name'))
            self.assertEqual(
                err.exception.error['name'][0],
                'Not a valid string.',
            )

    def test_cannot_pass_invalid_types_to_input_description(self):
        category = Category(name="Test", description="Description")
        self.repo.insert(category)
        usecase = UpdateCategoryUseCase(self.repo)

        for description in [{}, 5, 5.5, [], set()]:
            input_param = UpdateCategoryUseCase.Input(
                id=category.id,
                name=category.name,
                description=description,
            )

            with (
                patch.object(self.repo, 'update', wraps=self.repo.update) as repo_update,
                self.assertRaises(ValidationException) as err,
            ):
                usecase(input_param)
            repo_update.assert_not_called()
            self.assertTrue(err.exception.error.get('description'))
            self.assertEqual(
                err.exception.error['description'][0],
                'Not a valid string.',
            )

    def test_update_category(self):
        category = Category(name="Test", description="Description")
        self.repo.insert(category)

        usecase = UpdateCategoryUseCase(self.repo)
        input_param = UpdateCategoryUseCase.Input(
            id=category.id,
            name="updated name",
            is_active=True,
            description="updated description",
        )
        with patch.object(self.repo, 'update', wraps=self.repo.update) as repo_update:
            output = usecase(input_param)
        repo_update.assert_called()
        repo_category = self.repo.find_by_id(category.id)
        self.assertEqual(repo_category, category)
        self.assertEqual(output.name, category.name)
        self.assertEqual(output.description, category.description)
        self.assertTrue(output.is_active)

    def test_description_can_be_none(self):
        category = Category(name="Test", description="Description")
        self.repo.insert(category)

        usecase = UpdateCategoryUseCase(self.repo)
        input_param = UpdateCategoryUseCase.Input(
            id=category.id,
            name="Updated Name",
            description=None,
        )
        with patch.object(self.repo, 'update', wraps=self.repo.update) as repo_update:
            output = usecase(input_param)

        repo_update.assert_called_once()
        repo_category = self.repo.find_by_id(category.id)
        self.assertIsNone(repo_category.description)
        self.assertIsNone(output.description)

    def test_should_be_possible_toggle_category_active(self):
        category = Category(name="Test", description="Description")
        self.repo.insert(category)
        usecase = UpdateCategoryUseCase(self.repo)

        for is_active in [not category.is_active, category.is_active]:
            input_param = UpdateCategoryUseCase.Input(
                id=category.id,
                name="category name",
                description="description",
                is_active=is_active,
            )

            with patch.object(self.repo, 'update', wraps=self.repo.update) as repo_update:
                output = usecase(input_param)

            repo_update.assert_called_once()
            repo_category = self.repo.find_by_id(category.id)
            self.assertEqual(repo_category.is_active, is_active)
            self.assertEqual(output.is_active, is_active)

    def test_its_not_possible_to_pass_created_at(self):
        with self.assertRaises(TypeError) as err:
            UpdateCategoryUseCase.Input(  # pylint: disable=unexpected-keyword-arg
                id="123",
                name="Test",
                description="132",
                is_active=True,
                created_at="value",  # type: ignore
            )
        self.assertEqual(
            err.exception.args[0],
            "UpdateCategoryUseCase.Input.__init__() got an unexpected keyword argument 'created_at'"
        )


class TestDeleteCategoryUseCase(unittest.TestCase):

    repo: InMemoryCategoryRepository

    def setUp(self) -> None:
        self.repo = InMemoryCategoryRepository()

    def test_it_inherit_from_use_case(self):
        self.assertTrue(issubclass(DeleteCategoryUseCase, UseCase))

    def test_it_raises_if_id_is_none(self):
        usecase = DeleteCategoryUseCase(repo=self.repo)
        input_param = DeleteCategoryUseCase.Input(id=None)
        with (
            self.assertRaises(MissingParameter) as err,
            patch.object(self.repo, 'delete') as repo_delete
        ):
            usecase(input_param)
        self.assertEqual(err.exception.args[0], "Missing parameter id")
        repo_delete.assert_not_called()

    def test_it_delete_if_find_the_target_category(self):
        category = Category(name="cat1")
        self.repo.insert(category)

        usecase = DeleteCategoryUseCase(repo=self.repo)
        input_param = DeleteCategoryUseCase.Input(id="fake id")
        with patch.object(self.repo, 'delete') as repo_delete:
            usecase(input_param)
        repo_delete.assert_not_called()

    def test_it_can_delete_a_category(self):
        category = Category(name="cat1")
        self.repo.insert(category)

        usecase = DeleteCategoryUseCase(repo=self.repo)
        input_param = DeleteCategoryUseCase.Input(id=category.id)
        with patch.object(self.repo, 'delete') as repo_delete:
            usecase(input_param)
        repo_delete.assert_called_once_with(category)
