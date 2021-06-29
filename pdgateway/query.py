from flask import Request, Response


class UserQuery():
    def query(request: Request) -> Response:
        raise NotImplementedError