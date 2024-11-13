import requests

from api_test_runner.adapters.requests_adapter import from_requests
from api_test_runner.runner import EndpointTestRunner


@from_requests
def call_endpoint_with_json() -> requests.Response:
    return requests.get("https://jsonplaceholder.typicode.com/posts")

@from_requests
def call_endpoint_without_json() -> requests.Response:
    return requests.get("https://www.google.com")

@from_requests
def call_endpoint_with_post() -> requests.Response:
    return requests.post("https://jsonplaceholder.typicode.com/posts", json={"title": "foo", "body": "bar", "userId": 1})


def test_requests_get_with_json():
    runner = EndpointTestRunner(endpoint_client=call_endpoint_with_json, cache=True)

    runner.status_code.is_200_like()
    runner.response_time.less_than(1)
    runner.response_json.not_empty()


def test_requests_get_without_json():
    runner = EndpointTestRunner(endpoint_client=call_endpoint_with_json, cache=True)

    runner.status_code.is_200_like()
    runner.response_time.less_than(1)
    runner.response_json.is_empty()


def test_request_post():
    runner = EndpointTestRunner(endpoint_client=call_endpoint_with_post, cache=True)

    runner.status_code.is_200_like()
    runner.response_time.less_than(1)
    runner.response_json.not_empty()
    runner.response_json.key_equal("title", "foo")
