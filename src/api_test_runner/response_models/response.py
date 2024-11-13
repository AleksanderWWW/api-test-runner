from typing import Any


class Response:
    def __init__(self, status_code: int, elapsed: float, json: dict[str, Any]) -> None:
        self.status_code = status_code
        self.elapsed = elapsed
        self.json = json
