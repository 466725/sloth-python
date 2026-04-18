import requests
from typing import Optional


class QTestClient:
    def __init__(self, base_url: str, project_id: int, token: str):
        self.base_url = base_url.rstrip("/")
        self.project_id = project_id
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

    def create_test_run(self, name: str, test_case_id: int) -> Optional[int]:
        url = f"{self.base_url}/api/v3/projects/{self.project_id}/test-runs"

        payload = {
            "name": name,
            "test_case": {"id": test_case_id}
        }

        resp = requests.post(url, json=payload, headers=self.headers)
        resp.raise_for_status()

        return resp.json().get("id")

    def submit_test_log(self, test_run_id: int, status: str, note: str = ""):
        url = f"{self.base_url}/api/v3/projects/{self.project_id}/test-runs/{test_run_id}/test-logs"

        payload = {
            "status": status,  # PASSED / FAILED / BLOCKED
            "note": note
        }

        resp = requests.post(url, json=payload, headers=self.headers)
        resp.raise_for_status()
