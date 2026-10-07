"""Contract tests covering the published OpenAPI document as a whole.

These tests guard the suite itself: every documented operation must be claimed
by an endpoint test class, the document must stay internally consistent, and it
must stay in step with the application the suites exercise.
"""

from __future__ import annotations

import importlib
import pkgutil
from collections.abc import Iterator
from typing import Any

import pytest
from fastapi.testclient import TestClient

import tests.pytest_tests.api_suites as api_suites
from tests.pytest_tests.api_suites.base import BaseAPITest

pytestmark = pytest.mark.api

HTTP_METHODS = frozenset({"get", "post", "put", "patch", "delete", "head", "options"})


def _import_endpoint_suites() -> None:
    """Import every endpoint test module so its classes are registered."""
    for module in pkgutil.walk_packages(api_suites.__path__, f"{api_suites.__name__}."):
        if module.name.rsplit(".", 1)[-1].startswith("test_"):
            importlib.import_module(module.name)


def _subclasses(cls: type) -> Iterator[type]:
    """Yield every direct and indirect subclass of ``cls``."""
    for subclass in cls.__subclasses__():
        yield subclass
        yield from _subclasses(subclass)


def covered_operations() -> set[tuple[str, str]]:
    """Return the ``(path, method)`` pairs claimed by the endpoint suites."""
    _import_endpoint_suites()

    covered: set[tuple[str, str]] = set()
    for suite in _subclasses(BaseAPITest):
        if not suite.ENDPOINT:
            continue
        covered.add((suite.ENDPOINT, suite.METHOD.lower()))
        covered.update((path, method.lower()) for path, method in suite.EXTRA_ENDPOINTS)
    return covered


def documented_operations(api_spec: dict[str, Any]) -> set[tuple[str, str]]:
    """Return the ``(path, method)`` pairs published in the OpenAPI document."""
    return {
        (path, method)
        for path, operations in api_spec["paths"].items()
        for method in operations
        if method in HTTP_METHODS
    }


def collect_refs(node: Any) -> Iterator[str]:
    """Yield every ``$ref`` string found anywhere in the document."""
    if isinstance(node, dict):
        for key, value in node.items():
            if key == "$ref" and isinstance(value, str):
                yield value
            else:
                yield from collect_refs(value)
    elif isinstance(node, list):
        for item in node:
            yield from collect_refs(item)


class TestSpecCoverage:
    """The suites must exercise every documented operation."""

    def test_every_documented_operation_has_a_test_class(self, api_spec: dict[str, Any]) -> None:
        """No published endpoint may go untested."""
        missing = documented_operations(api_spec) - covered_operations()

        assert not missing, "Documented operations without an endpoint test class: " + ", ".join(
            f"{method.upper()} {path}" for path, method in sorted(missing)
        )

    def test_no_test_class_targets_an_undocumented_operation(
        self, api_spec: dict[str, Any]
    ) -> None:
        """Suites must not drift away from the published contract."""
        unknown = covered_operations() - documented_operations(api_spec)

        assert not unknown, "Endpoint test classes targeting undocumented operations: " + ", ".join(
            f"{method.upper()} {path}" for path, method in sorted(unknown)
        )

    def test_every_test_class_declares_a_lowercase_method(self) -> None:
        """``METHOD`` is compared case-sensitively by the spec helpers."""
        _import_endpoint_suites()

        offenders = [
            suite.__name__
            for suite in _subclasses(BaseAPITest)
            if suite.ENDPOINT and suite.METHOD != suite.METHOD.lower()
        ]

        assert not offenders, f"METHOD must be lowercase on: {offenders}"


class TestSpecIntegrity:
    """The published document must be self-consistent."""

    def test_declares_an_openapi_version_and_title(self, api_spec: dict[str, Any]) -> None:
        """The document carries the metadata clients rely on."""
        assert api_spec["openapi"].startswith("3.")
        assert api_spec["info"]["title"]
        assert api_spec["info"]["version"]

    def test_every_reference_resolves(self, api_spec: dict[str, Any]) -> None:
        """No operation may point at a schema that is not defined."""
        schemas = api_spec["components"]["schemas"]
        dangling = sorted(
            {
                ref
                for ref in collect_refs(api_spec)
                if not ref.startswith("#/components/schemas/")
                or ref.rsplit("/", 1)[-1] not in schemas
            }
        )

        assert not dangling, f"Unresolvable references: {dangling}"

    def test_every_schema_is_referenced(self, api_spec: dict[str, Any]) -> None:
        """Unused schemas indicate the document drifted from the application."""
        referenced = {
            ref.rsplit("/", 1)[-1]
            for ref in collect_refs(api_spec)
            if ref.startswith("#/components/schemas/")
        }
        orphans = sorted(set(api_spec["components"]["schemas"]) - referenced)

        assert not orphans, f"Schemas defined but never referenced: {orphans}"

    def test_every_operation_documents_a_success_response(self, api_spec: dict[str, Any]) -> None:
        """Clients need at least one documented 2xx outcome per operation."""
        undocumented = [
            f"{method.upper()} {path}"
            for path, method in sorted(documented_operations(api_spec))
            if not any(
                status.startswith("2")
                for status in api_spec["paths"][path][method].get("responses", {})
            )
        ]

        assert not undocumented, f"Operations without a 2xx response: {undocumented}"


class TestSpecMatchesApplication:
    """The document must describe the application the suites run against."""

    def test_the_served_schema_matches_the_published_document(
        self, api_client: TestClient, api_spec: dict[str, Any]
    ) -> None:
        """``docs/api_spec.json`` must be regenerated when routes change."""
        served = api_client.get("/openapi.json").json()

        assert sorted(served["paths"]) == sorted(api_spec["paths"])
        assert sorted(served["components"]["schemas"]) == sorted(api_spec["components"]["schemas"])

    def test_the_served_operations_match_the_published_document(
        self, api_client: TestClient, api_spec: dict[str, Any]
    ) -> None:
        """Methods, not just paths, must stay in step with the application."""
        served = api_client.get("/openapi.json").json()

        assert documented_operations(served) == documented_operations(api_spec)
