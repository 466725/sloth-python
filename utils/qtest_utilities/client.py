"""qTest API client used by the pytest reporting hooks."""

from __future__ import annotations

from typing import Optional

import requests


class QTestClient:
    """Small client for creating qTest runs and submitting test results."""

    def __init__(self, base_url: str, project_id: int, token: str):
        self.base_url = base_url.rstrip("/")
        self.project_id = project_id
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

    def create_test_run(self, name: str, test_case_id: int) -> Optional[int]:
        """Create a qTest run and return its ID."""

        url = f"{self.base_url}/api/v3/projects/{self.project_id}/test-runs"
        response = requests.post(
            url,
            json={"name": name, "test_case": {"id": test_case_id}},
            headers=self.headers,
        )
        response.raise_for_status()
        return response.json().get("id")

    def submit_test_log(self, test_run_id: int, status: str, note: str = "") -> None:
        """Submit a qTest result for an existing test run."""

        url = (
            f"{self.base_url}/api/v3/projects/{self.project_id}/test-runs/"
            f"{test_run_id}/test-logs"
        )
        response = requests.post(
            url,
            json={"status": status, "note": note},
            headers=self.headers,
        )
        response.raise_for_status()