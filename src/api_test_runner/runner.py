import time
from typing import (
    Any,
    Callable,
    Optional,
)

from api_test_runner.response_models.response import Response
from api_test_runner.response_models.response_attributes import (
    ResponseJson,
    ResponseTime,
    StatusCode,
)


class EndpointTestRunner:
    def __init__(
        self,
        *,
        endpoint_client: Callable[..., Response],
        cache: bool = False,
        **endpoint_params: Any,
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
