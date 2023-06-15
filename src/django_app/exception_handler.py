from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import \
    exception_handler as rest_framework_exception_handler

from core.__seedwork.domain.exceptions import (EntityNotFound,
                                               ValidationException)


def handler_serializer_validation_error(exception: ValidationError, context):
    response = rest_framework_exception_handler(exception, context)
    response.status_code = 422
    return response


def handler_serializer_validation_exception(
    exception: ValidationException, context,   # pylint: disable=unused-argument
):
    response = Response(exception.error, status=422)
    return response

def handler_serializer_entity_not_found(
    exception: EntityNotFound, context,   # pylint: disable=unused-argument
):
    response = Response({"message": str(exception)}, status=404)
    return response

handlers = {
    ValidationError: handler_serializer_validation_error,
    ValidationException: handler_serializer_validation_exception,
    EntityNotFound: handler_serializer_entity_not_found,
}


def custom_exception_handler(exc, context):
    handler = handlers.get(exc.__class__, rest_framework_exception_handler)
    return handler(exc, context)
