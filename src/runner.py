import time
from typing import Callable, Any, Optional

from adapters.requests_adapter import from_requests
from response_models.response import Response

from response_models.response_attributes import StatusCode, ResponseTime, ResponseJson


class ApiTestRunner:
    def __init__(
            self, *, endpoint_client: Callable[..., Response], cache: bool = False,  **endpoint_params: Any,
    ) -> None:
        self._endpoint_client = endpoint_client
        self._endpoint_params = endpoint_params

        self._cache = cache
        self._response: Optional[Response] = None

    def _run_endpoint_test(self) -> Response:
        response = self._response or self._endpoint_client(**self._endpoint_params)
        if self._cache:
            self._response = response
        return response

    @property
    def status_code(self) -> StatusCode:
        return StatusCode(self._run_endpoint_test().status_code)

    @property
    def response_time(self) -> ResponseTime:
        start = time.perf_counter()
        self._run_endpoint_test()
        return ResponseTime(time.perf_counter() - start)

    @property
    def response_json(self) -> ResponseJson:
        return ResponseJson(self._run_endpoint_test().json)


if __name__ == "__main__":
    @from_requests
    def call_google() -> Response:
        import requests
        return requests.get("https://www.google.com")

    runner = ApiTestRunner(endpoint_client=call_google, cache=True)
    print(runner.status_code.is_200_like())
    print(runner.response_time.less_than(1))
