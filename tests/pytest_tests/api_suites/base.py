"""Shared base class and assertion helpers for the DSA API suites.

Every endpoint suite extends :class:`BaseAPITest` so that each test can assert
both the observable behavior of an endpoint and the contract published in
``docs/api_spec.json``. Keeping the assertions here avoids repeating response
envelope knowledge in each of the twelve API domains.
"""

from __future__ import annotations

from typing import Any, ClassVar

from httpx import Response
from jsonschema import Draft202012Validator

JSON_CONTENT_TYPE = "application/json"

# Error envelope produced by api.middlewares.error_handler for HTTPException
# payloads that already use the {"error": ..., "message": ...} shape.
ERROR_KEYS = ("error", "message")


class BaseAPITest:
    """Base class providing spec-aware assertions for API endpoint suites.

    Subclasses declare the documented operation they cover::

        class TestUsageSummary(BaseAPITest):
            ENDPOINT = "/api/v1/usage/summary"
            METHOD = "get"

    The declared ``ENDPOINT``/``METHOD`` become the default target for the
    spec-driven helpers, so individual tests only pass a response object.
    """

    #: Documented OpenAPI path template, e.g. ``/api/v1/history/{record_id}``.
    ENDPOINT: ClassVar[str] = ""
    #: Lowercase HTTP method documented for :attr:`ENDPOINT`.
    METHOD: ClassVar[str] = "get"
    #: Further ``(path, method)`` operations this class also covers, declared so
    #: the spec-coverage contract test can account for them.
    EXTRA_ENDPOINTS: ClassVar[tuple[tuple[str, str], ...]] = ()

    # ------------------------------------------------------------------
    # Generic response assertions
    # ------------------------------------------------------------------

    @staticmethod
    def assert_json(response: Response, expected_status: int) -> Any:
        """Assert the status code and JSON content type, returning the body."""
        assert response.status_code == expected_status, (
            f"{response.request.method} {response.request.url.path} returned "
            f"{response.status_code}, expected {expected_status}. Body: {response.text[:500]}"
        )
        assert response.headers["content-type"].startswith(JSON_CONTENT_TYPE)
        return response.json()

    @classmethod
    def assert_ok(cls, response: Response) -> Any:
        """Assert a successful ``200 OK`` JSON response and return the body."""
        return cls.assert_json(response, 200)

    @classmethod
    def assert_error(
        cls,
        response: Response,
        expected_status: int,
        expected_error: str | None = None,
    ) -> dict[str, Any]:
        """Assert a DSA error envelope with the expected status and error code."""
        body = cls.assert_json(response, expected_status)
        assert isinstance(body, dict), f"Error body must be an object, got {type(body)!r}"
        for key in ERROR_KEYS:
            assert key in body, f"Error envelope missing '{key}': {body}"
        assert isinstance(body["message"], str) and body["message"]
        if expected_error is not None:
            assert body["error"] == expected_error, (
                f"Expected error code '{expected_error}', got '{body['error']}'"
            )
        return body

    @classmethod
    def assert_validation_error(
        cls, response: Response, field: str | None = None
    ) -> dict[str, Any]:
        """Assert a ``422`` request-validation response, optionally naming a field."""
        body = cls.assert_json(response, 422)
        assert body["error"] == "validation_error"
        details = body.get("detail")
        assert isinstance(details, list) and details, f"Expected validation detail list: {body}"
        if field is not None:
            locations = {str(part) for item in details for part in item.get("loc", ())}
            assert field in locations, f"Field '{field}' not reported in {details}"
        return body

    @classmethod
    def assert_not_found(cls, response: Response) -> dict[str, Any]:
        """Assert a ``404`` response using the shared error envelope."""
        return cls.assert_error(response, 404, "not_found")

    @classmethod
    def assert_unauthorized(cls, response: Response) -> dict[str, Any]:
        """Assert the auth middleware rejected the request with ``401``."""
        return cls.assert_error(response, 401, "unauthorized")

    @staticmethod
    def assert_paginated(body: dict[str, Any], *, page: int | None = None) -> list[Any]:
        """Assert a list envelope exposing ``items``/``total`` and return the items."""
        assert isinstance(body, dict), f"Paginated body must be an object, got {type(body)!r}"
        assert "items" in body, f"Paginated body missing 'items': {sorted(body)}"
        assert isinstance(body["items"], list)
        assert isinstance(body["total"], int) and body["total"] >= 0
        size_key = "page_size" if "page_size" in body else "limit"
        assert isinstance(body[size_key], int) and body[size_key] >= 1
        if page is not None:
            assert body["page"] == page
        assert len(body["items"]) <= body[size_key]
        return body["items"]

    # ------------------------------------------------------------------
    # Spec-driven assertions
    # ------------------------------------------------------------------

    @classmethod
    def operation(
        cls,
        api_spec: dict[str, Any],
        path: str | None = None,
        method: str | None = None,
    ) -> dict[str, Any]:
        """Return the documented OpenAPI operation for this endpoint."""
        path = path or cls.ENDPOINT
        method = (method or cls.METHOD).lower()
        assert path, f"{cls.__name__} must define ENDPOINT"
        assert path in api_spec["paths"], f"Path '{path}' is not documented in api_spec.json"
        operations = api_spec["paths"][path]
        assert method in operations, (
            f"Method '{method.upper()}' is not documented for '{path}'. "
            f"Documented: {sorted(k.upper() for k in operations)}"
        )
        return operations[method]

    @classmethod
    def assert_documented_status(
        cls,
        api_spec: dict[str, Any],
        response: Response,
        path: str | None = None,
        method: str | None = None,
    ) -> None:
        """Assert the returned status code is documented for the operation."""
        operation = cls.operation(api_spec, path, method)
        documented = set(operation.get("responses", {}))
        status = str(response.status_code)
        assert status in documented, (
            f"Status {status} is undocumented for {(method or cls.METHOD).upper()} "
            f"{path or cls.ENDPOINT}. Documented: {sorted(documented)}"
        )

    @classmethod
    def response_schema(
        cls,
        api_spec: dict[str, Any],
        status: int,
        path: str | None = None,
        method: str | None = None,
    ) -> dict[str, Any] | None:
        """Return the documented JSON schema for a status code, if any."""
        operation = cls.operation(api_spec, path, method)
        documented = operation.get("responses", {}).get(str(status))
        if not documented:
            return None
        schema = documented.get("content", {}).get(JSON_CONTENT_TYPE, {}).get("schema")
        return schema or None

    @classmethod
    def assert_matches_spec(
        cls,
        api_spec: dict[str, Any],
        response: Response,
        path: str | None = None,
        method: str | None = None,
    ) -> Any:
        """Assert the response status and JSON body honor the documented contract."""
        cls.assert_documented_status(api_spec, response, path, method)
        body = response.json()
        schema = cls.response_schema(api_spec, response.status_code, path, method)
        if schema:
            validate_against_spec(api_spec, schema, body)
        return body


def validate_against_spec(api_spec: dict[str, Any], schema: dict[str, Any], payload: Any) -> None:
    """Validate ``payload`` against an OpenAPI schema from ``api_spec``.

    ``components`` is grafted onto the schema document so that local
    ``#/components/schemas/...`` references resolve without network access.
    """
    if not schema:
        return
    document = dict(schema)
    document["components"] = api_spec["components"]
    errors = sorted(
        Draft202012Validator(document).iter_errors(payload),
        key=lambda error: list(error.absolute_path),
    )
    assert not errors, "Response does not match api_spec.json:\n" + "\n".join(
        f"  - {'/'.join(str(part) for part in error.absolute_path) or '<root>'}: {error.message}"
        for error in errors[:10]
    )
