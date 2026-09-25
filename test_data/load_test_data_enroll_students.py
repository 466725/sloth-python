"""Export student records from MySQL for enrollment load testing.
From the repository root, copy, paste, and run: 
python -m test_data.load_test_data_enroll_students
"""
from __future__ import annotations

import csv
from collections.abc import Callable, Mapping
from pathlib import Path
from typing import Any

from test_data.csv_reader import resolve_path
from utils.data_base import connect_mysql, connection_scope, fetch_all

STUDENTS_QUERY = """
	SELECT
		id,
		student_number,
		first_name,
		last_name,
		email,
		date_of_birth,
		department_id,
		status,
		created_at
	FROM students
	ORDER BY id;
"""

STUDENT_COLUMNS = (
	"id",
	"student_number",
	"first_name",
	"last_name",
	"email",
	"date_of_birth",
	"department_id",
	"status",
	"created_at",
)

DEFAULT_OUTPUT_FILE = Path("test_data/load_test_data_enroll_students.csv")
ConnectionFactory = Callable[[], Any]


def fetch_student_data(connection: Any) -> list[Mapping[str, Any]]:
	"""Fetch every student column needed by the enrollment load test."""

	return fetch_all(connection, STUDENTS_QUERY, as_dict=True)


def write_student_data(
	rows: list[Mapping[str, Any]], output_file: str | Path = DEFAULT_OUTPUT_FILE
) -> Path:
	"""Write student records to a headered CSV and return its resolved path."""

	output_path = resolve_path(output_file)
	output_path.parent.mkdir(parents=True, exist_ok=True)
	with output_path.open("w", encoding="utf-8", newline="") as file:
		writer = csv.DictWriter(file, fieldnames=STUDENT_COLUMNS, extrasaction="ignore")
		writer.writeheader()
		writer.writerows(rows)
	return output_path


def export_student_data(
	connection_factory: ConnectionFactory = connect_mysql,
	output_file: str | Path = DEFAULT_OUTPUT_FILE,
) -> Path:
	"""Fetch students from MySQL and save them to the enrollment CSV."""

	with connection_scope(connection_factory) as connection:
		rows = fetch_student_data(connection)
	return write_student_data(rows, output_file)


if __name__ == "__main__":
	print(f"Student data exported to: {export_student_data()}")
