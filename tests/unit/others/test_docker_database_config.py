import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


@unittest.skipUnless(shutil.which("docker"), "Docker Compose is not installed")
class TestDockerDatabaseConfig(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        result = subprocess.run(["docker", "compose", "version"], capture_output=True, text=True)
        if result.returncode:
            raise unittest.SkipTest("Docker Compose is not installed")

    def test_compose_uses_persistent_database_instead_of_local_path(self):
        source = Path(__file__).resolve().parents[3] / "docker" / "docker-compose.yml"
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            docker_dir = root / "docker"
            docker_dir.mkdir()
            shutil.copyfile(source, docker_dir / "docker-compose.yml")
            env_file = root / ".env"
            env_file.write_text(
                "DATABASE_PATH=./ai_stock/stock_data/stock_analysis.db\nSQLITE_WAL_ENABLED=true\n"
            )
            env = os.environ.copy()

            for override, expected, wal_override in (
                (None, "/app/data/stock_analysis.db", None),
                ("/app/data/custom.db", "/app/data/custom.db", None),
                (None, "/app/data/stock_analysis.db", "true"),
            ):
                with self.subTest(override=override, wal_override=wal_override):
                    env.pop("DOCKER_DATABASE_PATH", None)
                    env.pop("DOCKER_SQLITE_WAL_ENABLED", None)
                    if override is not None:
                        env["DOCKER_DATABASE_PATH"] = override
                    if wal_override is not None:
                        env["DOCKER_SQLITE_WAL_ENABLED"] = wal_override
                    result = subprocess.run(
                        [
                            "docker",
                            "compose",
                            "--env-file",
                            str(env_file),
                            "-f",
                            str(docker_dir / "docker-compose.yml"),
                            "config",
                            "--format",
                            "json",
                        ],
                        capture_output=True,
                        text=True,
                        check=True,
                        env=env,
                    )
                    services = json.loads(result.stdout)["services"]
                    for service_name in ("server", "analyzer"):
                        service = services[service_name]
                        self.assertEqual(service["environment"]["DATABASE_PATH"], expected)
                        self.assertEqual(
                            service["environment"]["SQLITE_WAL_ENABLED"], wal_override or "false"
                        )
                        self.assertTrue(
                            any(
                                volume["target"] == "/app/data"
                                and Path(volume["source"]) == root / "ai_stock" / "stock_data"
                                for volume in service["volumes"]
                            )
                        )
