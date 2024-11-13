from typing import ParamSpec, Callable

from response_models.response import Response

P = ParamSpec("P")


def from_requests(endpoint_client: Callable) -> Callable[..., Response]:
    try:
        import requests
    except ImportError:
        raise ImportError("You need to install `requests` to use this adapter")

    def wrapper(*args: P.args, **kwargs: P.kwargs) -> Response:
        result = endpoint_client(*args, **kwargs)
        if not isinstance(result, requests.Response):
            raise TypeError("The endpoint client must return a `requests.Response` object")

        try:
            json_body = result.json()
        except requests.exceptions.JSONDecodeError:
            json_body = {}
        return Response(
            status_code=result.status_code,
            elapsed=result.elapsed.total_seconds(),
            json=json_body,
        )

    return wrapper
