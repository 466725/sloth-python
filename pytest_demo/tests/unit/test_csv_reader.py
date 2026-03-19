from pathlib import Path

import pytest

from utils.csv_reader import read_csv_to_list


def _write_csv(tmp_path: Path, name: str, content: str) -> Path:
    file_path = tmp_path / name
    file_path.write_text(content, encoding="utf-8")
    return file_path


@pytest.mark.unit
def test_read_csv_to_list_returns_raw_strings_when_convert_to_int_is_false(tmp_path: Path):
    csv_file = _write_csv(tmp_path, "mixed.csv", "a,b,c\n1,2,3\n\n4,5,6\n")

    rows = read_csv_to_list(csv_file, convert_to_int=False)

    assert rows == [["1", "2", "3"], ["4", "5", "6"]]


@pytest.mark.unit
def test_read_csv_to_list_converts_numeric_cells_to_int(tmp_path: Path):
    csv_file = _write_csv(tmp_path, "numbers.csv", "a,b,c\n1,2,3\n10,20,30\n")

    rows = read_csv_to_list(csv_file)

    assert rows == [[1, 2, 3], [10, 20, 30]]


@pytest.mark.unit
def test_read_csv_to_list_raises_on_mixed_content_when_convert_to_int_is_true(tmp_path: Path):
    csv_file = _write_csv(tmp_path, "mixed.csv", "a,b,c\n1,2,3\n4,YP,6\n")

    with pytest.raises(ValueError, match="convert_to_int=True"):
        read_csv_to_list(csv_file)


@pytest.mark.unit
def test_read_csv_to_list_keeps_existing_calculator_data_behavior():
    rows = read_csv_to_list("pytest_demo/tests/calculator-data.csv")

    assert rows == [[9, 10, 19], [12, 13, 25]]
