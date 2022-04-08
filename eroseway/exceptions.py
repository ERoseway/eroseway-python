import copy
import inspect

__all__ = [
    'APIException',
    'Forbidden',
    'InvalidRequest',
    'NotFound',
    'RateLimitExceeded',
    'Unauthorized'
]


class APIException(Exception):
    """
    An error occurred while processing an API the request.
    """

    def __init__(self, status_code, hint=None, arg_errors=None):
        super().__init__()

        # The status code associated with the error
        self.status_code = status_code

        # A hint providing additional information as to why this error
        # occurred.
        self._hint = hint

        # A dictionary of errors relating to the arguments (parameters) sent
        # to the API endpoint (e.g `{'arg_name': ['error1', ...]}`).
        self._arg_errors = arg_errors

    def __str__(self):

        doc_str = inspect.cleandoc(self.__class__.__doc__)
        parts = [f'[{self.status_code}] {doc_str}']

        if self._hint:
            parts.append(f'Hint: {self._hint}')

        if self._arg_errors:
            parts.append(
                'Argument errors:\n- ' + '\n- '.join([
                    f'{arg_name}: {" ".join(errors)}'
                    for arg_name, errors in self._arg_errors.items()
                ])
            )

        return '\n---\n'.join(parts)

    @property
    def arg_errors(self):
        if self._arg_errors:
            return copy.deepcopy(self._arg_errors)

    @property
    def hint(self):
        return self._hint

    @classmethod
    def get_class_by_status_code(cls, error_type, default=None):
        """
        Return the exception class associated with the status code, if no
        class matches the given status code then the base `APIException` class
        is returned.
        """

        class_map = {
            400: InvalidRequest,
            401: Unauthorized,
            403: Forbidden,
            405: Forbidden,
            404: NotFound,
            429: RateLimitExceeded
        }

        return class_map.get(error_type, default or APIException)


class Forbidden(APIException):
    """
    The request is not not allowed, most likely the HTTP method used to call
    the API endpoint is incorrect or the API key (via its associated clinic)
    does not have permission to call the endpoint and/or perform the action.
    """


class InvalidRequest(APIException):
    """
    Not a valid request, most likely a missing or invalid parameter.
    """


class NotFound(APIException):
    """
    The endpoint you are calling or the document you referenced doesn't exist.
    """


class RateLimitExceeded(APIException):
    """
    You have exceeded the number of API requests allowed per second.
    """


class Unauthorized(APIException):
    """
    The API credentials provided are not valid.
    """
