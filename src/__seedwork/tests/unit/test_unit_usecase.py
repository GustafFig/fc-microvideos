# pylint: disable=abstract-class-instantiated
import unittest

from __seedwork.application.usecases import UseCase


class TestUseCase(unittest.TestCase):

    def test_usecase_is_an_abstract_class(self):
        with self.assertRaises(TypeError) as err:
            UseCase()  # type: ignore
        self.assertEqual(
            err.exception.args[0],
            "Can't instantiate abstract class UseCase with abstract method __call__"
        )
