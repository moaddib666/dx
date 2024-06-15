from rest_framework.exceptions import APIException


class _GameException(Exception):
    pass


class _GameException(APIException, _GameException):
    @property
    def default_code(self):
        return self.__class__.__name__

    def __init__(self, detail=None, code=None):
        self.detail = {
            "code": code or self.default_code,
            "message": detail,
        }


class GameException(_GameException):
    status_code = 500


class GameLogicException(GameException):
    status_code = 400
