from abc import ABC, abstractmethod


class UseCase(ABC):

    @abstractmethod
    def __call__(self, input_param: 'Input') -> 'Output':
        raise NotImplementedError()
    
    def execute(self, input_param: 'Input') -> 'Output':
        return self(input_param)

    class Input:
        pass

    class Output:
        pass
