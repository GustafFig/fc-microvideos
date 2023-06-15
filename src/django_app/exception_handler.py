from rest_framework.exceptions import ValidationError

from rest_framework.views import exception_handler as rest_framework_exception_handler


def handler_serializer_validation_error(exception: ValidationError, context):
    response = rest_framework_exception_handler(exception, context)
    response.status_code = 422
    return response

def custom_exception_handler(exc, context):
    if isinstance(exc, ValidationError):
        return handler_serializer_validation_error(exc, context)
    return rest_framework_exception_handler(exc, context)
