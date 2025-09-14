from pathlib import Path

import pytest
from tomlkit.exceptions import ParseError

from troml.loader import get_pyproject_data


def test_file_path(tmp_path):
    expected = "MIT"

    pyproject_path = tmp_path / "pyproject.toml"
    pyproject_path.write_text("""
[project]
license = "MIT"
""")

    actual = get_pyproject_data(tmp_path)

    assert expected == actual["project"]["license"]


def test_dir_path(tmp_path):
    expected = "MIT"

    pyproject_path = tmp_path / "pyproject.toml"
    pyproject_path.write_text("""
[project]
license = "MIT"
""")

    actual = get_pyproject_data(tmp_path)

    assert expected == actual["project"]["license"]


def test_not_found():
    with pytest.raises(FileNotFoundError) as e:
        get_pyproject_data(Path("/nonexistent/path"))

    assert "FileNotFoundError: [Errno 2] No such file or directory" in e.exconly()


def test_invalid_toml(tmp_path):
    pyproject_path = tmp_path / "pyproject.toml"
    pyproject_path.write_text("invalid toml content")

    with pytest.raises(ParseError) as e:
        get_pyproject_data(tmp_path)

    assert 'Invalid key "invalid toml content"' in e.exconly()
