class fullstoryError(Exception):
    """class representing Generic Http error."""

    def __init__(self, message=None, response=None):
        super().__init__(message)
        self.message = message
        self.response = response


class fullstoryBackoffError(fullstoryError):
    """class representing backoff error handling."""
    pass

class fullstoryBadRequestError(fullstoryError):
    """class representing 400 status code."""
    pass

class fullstoryUnauthorizedError(fullstoryError):
    """class representing 401 status code."""
    pass


class fullstoryForbiddenError(fullstoryError):
    """class representing 403 status code."""
    pass

class fullstoryNotFoundError(fullstoryError):
    """class representing 404 status code."""
    pass

class fullstoryConflictError(fullstoryError):
    """class representing 409 status code."""
    pass

class fullstoryUnprocessableEntityError(fullstoryBackoffError):
    """class representing 422 status code."""
    pass

class fullstoryRateLimitError(fullstoryBackoffError):
    """class representing 429 status code."""
    pass

class fullstoryInternalServerError(fullstoryBackoffError):
    """class representing 500 status code."""
    pass

class fullstoryNotImplementedError(fullstoryBackoffError):
    """class representing 501 status code."""
    pass

class fullstoryBadGatewayError(fullstoryBackoffError):
    """class representing 502 status code."""
    pass

class fullstoryServiceUnavailableError(fullstoryBackoffError):
    """class representing 503 status code."""
    pass

ERROR_CODE_EXCEPTION_MAPPING = {
    400: {
        "raise_exception": fullstoryBadRequestError,
        "message": "A validation exception has occurred."
    },
    401: {
        "raise_exception": fullstoryUnauthorizedError,
        "message": "The access token provided is expired, revoked, malformed or invalid for other reasons."
    },
    403: {
        "raise_exception": fullstoryForbiddenError,
        "message": "You are missing the following required scopes: read"
    },
    404: {
        "raise_exception": fullstoryNotFoundError,
        "message": "The resource you have specified cannot be found."
    },
    409: {
        "raise_exception": fullstoryConflictError,
        "message": "The API request cannot be completed because the requested operation would conflict with an existing item."
    },
    422: {
        "raise_exception": fullstoryUnprocessableEntityError,
        "message": "The request content itself is not processable by the server."
    },
    429: {
        "raise_exception": fullstoryRateLimitError,
        "message": "The API rate limit for your organisation/application pairing has been exceeded."
    },
    500: {
        "raise_exception": fullstoryInternalServerError,
        "message": "The server encountered an unexpected condition which prevented" \
            " it from fulfilling the request."
    },
    501: {
        "raise_exception": fullstoryNotImplementedError,
        "message": "The server does not support the functionality required to fulfill the request."
    },
    502: {
        "raise_exception": fullstoryBadGatewayError,
        "message": "Server received an invalid response."
    },
    503: {
        "raise_exception": fullstoryServiceUnavailableError,
        "message": "API service is currently unavailable."
    }
}
