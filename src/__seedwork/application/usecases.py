from abc import ABC, abstractmethod


class UseCase(ABC):

    @abstractmethod
    def __call__(self, input_param: 'Input') -> 'Output':
        raise NotImplementedError()

    class Input:
        pass

    class Output:
        pass
