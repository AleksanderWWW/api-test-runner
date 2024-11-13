import time

import urllib3

from typing import ParamSpec, Callable

from api_test_runner.response_models.response import Response

P = ParamSpec("P")


def from_urllib(endpoint_client: Callable) -> Callable[..., Response]:
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> Response:
        start = time.perf_counter()
        result = endpoint_client(*args, **kwargs)
        elapsed = time.perf_counter() - start
        if not isinstance(result, urllib3.HTTPResponse):
            raise TypeError("The endpoint client must return a `urllib3.HTTPResponse` object")

        return Response(
            status_code=result.status,
            elapsed=elapsed,
            json=result.data,
        )

    return wrapper
