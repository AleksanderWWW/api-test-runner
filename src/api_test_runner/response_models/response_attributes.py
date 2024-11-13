from dataclasses import dataclass
from typing import Any


@dataclass
class StatusCode:
    code: int

    def equal(self, code: int) -> bool:
        return self.code == code

    def between(self, start: int, end: int) -> bool:
        return start <= self.code <= end

    def is_500_like(self) -> bool:
        return self.between(500, 599)

    def is_400_like(self) -> bool:
        return self.between(400, 499)

    def is_300_like(self) -> bool:
        return self.between(300, 399)

    def is_200_like(self) -> bool:
        return self.between(200, 299)

    def is_100_like(self) -> bool:
        return self.between(100, 199)

    def is_success(self) -> bool:
        return self.is_200_like()

    def is_redirect(self) -> bool:
        return self.is_300_like()


@dataclass
class ResponseTime:
    time: float

    def less_than(self, value: float) -> bool:
        return self.time < value

    def greater_than(self, value: float) -> bool:
        return self.time > value

    def equal(self, value: float) -> bool:
        return self.time == value

    def between(self, start: float, end: float) -> bool:
        return start <= self.time <= end


@dataclass
class ResponseJson:
    data: dict[str, Any]

    def not_empty(self) -> bool:
        return bool(self.data)

    def is_empty(self) -> bool:
        return not self.data

    def has_key(self, key: str) -> bool:
        return key in self.data

    def key_equal(self, key: str, value: Any) -> bool:
        return self.data.get(key) == value