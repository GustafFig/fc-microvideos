"""Module for declare the Exception of the project"""

class InvalidUUidException(Exception):
    """The Exception for invalid UUID value"""
    def __init__(self, error: str="ID must be a valid UUID") -> None:
        super().__init__(error)


class ValidationException(Exception):
    """The Exception for domain validations"""

    def __init__(self, error) -> None:
        self.error = error
        super().__init__('Validation Error')

class ValidationRulesException(Exception):
    """The Exception for ValidationRulesException"""
