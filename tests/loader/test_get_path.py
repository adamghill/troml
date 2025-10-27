from pathlib import Path

import pytest

from troml.loader import get_path


def test_missing_path():
    with pytest.raises(FileNotFoundError) as e:
        get_path(Path("/nonexistent/path"))

    assert "No such directory" in e.exconly()


def test_file_path(tmp_path):
    expected = tmp_path

    file_path = tmp_path / "pyproject.toml"
    file_path.touch()
    actual = get_path(file_path)

    assert expected == actual
