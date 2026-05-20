class APIError(Exception):
    code = 500
    message = 'Error del servidor'

    def __init__(self, message=None):
        if message:
            self.message = message
        super().__init__(self.message)


class BadRequestError(APIError):
    code = 400


class NotFoundError(APIError):
    code = 404


class ConflictError(APIError):
    code = 409
