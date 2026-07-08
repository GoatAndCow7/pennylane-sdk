from __future__ import annotations

import httpx
import pytest

from pennylane_sdk._exceptions import (
    APIStatusError,
    AuthenticationError,
    BadRequestError,
    ConflictError,
    NotFoundError,
    PermissionDeniedError,
    RateLimitError,
    ServerError,
    ValidationError,
    make_status_error,
)


def _response(status: int, json_body: object = None, text: str | None = None, headers: dict[str, str] | None = None) -> httpx.Response:
    request = httpx.Request("GET", "https://app.pennylane.com/api/external/v2/me")
    if json_body is not None:
        return httpx.Response(status, json=json_body, request=request, headers=headers)
    return httpx.Response(status, text=text or "", request=request, headers=headers)


class TestStatusMapping:
    @pytest.mark.parametrize(
        ("status", "expected"),
        [
            (400, BadRequestError),
            (401, AuthenticationError),
            (403, PermissionDeniedError),
            (404, NotFoundError),
            (409, ConflictError),
            (422, ValidationError),
            (429, RateLimitError),
            (500, ServerError),
            (503, ServerError),
        ],
    )
    def test_maps_status_to_class(self, status: int, expected: type[APIStatusError]) -> None:
        error = make_status_error(_response(status, {"error": "boom"}))
        assert type(error) is expected
        assert error.status_code == status

    def test_unknown_4xx_falls_back_to_base_class(self) -> None:
        error = make_status_error(_response(418, {"error": "teapot"}))
        assert type(error) is APIStatusError


class TestBodyParsing:
    def test_guide_format_error_message_details(self) -> None:
        body = {
            "error": "unprocessable_entity",
            "message": "Entry lines are not balanced",
            "details": {"debit_total": "100.00", "credit_total": "80.00"},
        }
        error = make_status_error(_response(422, body))
        assert error.error_code == "unprocessable_entity"
        assert error.message == "Entry lines are not balanced"
        assert error.details == {"debit_total": "100.00", "credit_total": "80.00"}
        assert error.body == body

    def test_spec_format_error_status(self) -> None:
        error = make_status_error(_response(401, {"error": "Unauthorized", "status": 401}))
        assert error.error_code == "Unauthorized"
        assert error.message == "Unauthorized"
        assert error.details is None

    def test_conflict_format_with_status_field(self) -> None:
        body = {"status": 409, "error": "A document with ID 42 already exists."}
        error = make_status_error(_response(409, body))
        assert isinstance(error, ConflictError)
        assert error.message == "A document with ID 42 already exists."

    def test_non_json_body(self) -> None:
        error = make_status_error(_response(503, text="Service Unavailable"))
        assert isinstance(error, ServerError)
        assert error.message == "Service Unavailable"
        assert error.body is None

    def test_empty_body(self) -> None:
        error = make_status_error(_response(500))
        assert error.message == "HTTP 500"

    def test_non_dict_json_body(self) -> None:
        error = make_status_error(_response(400, ["weird"]))
        assert isinstance(error, BadRequestError)
        assert error.body == ["weird"]


class TestRateLimitError:
    def test_parses_retry_after(self) -> None:
        error = make_status_error(
            _response(429, {"error": "Rate limit exceeded"}, headers={"retry-after": "3"})
        )
        assert isinstance(error, RateLimitError)
        assert error.retry_after == 3.0

    def test_missing_retry_after(self) -> None:
        error = make_status_error(_response(429, {"error": "Rate limit exceeded"}))
        assert isinstance(error, RateLimitError)
        assert error.retry_after is None

    def test_invalid_retry_after(self) -> None:
        error = make_status_error(
            _response(429, {"error": "x"}, headers={"retry-after": "soon"})
        )
        assert isinstance(error, RateLimitError)
        assert error.retry_after is None
