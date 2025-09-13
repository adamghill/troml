from pathlib import Path
from unittest.mock import patch

import pytest

from troml.loader import get_cwd_and_pyproject_data


def test():
    pass


@patch("typer.secho")
def test_dir_path(_, tmp_path):
    (tmp_path / "pyproject.toml").write_text("""
[project]
license = "MIT"
""")

    (cwd, data) = get_cwd_and_pyproject_data(tmp_path)

    assert tmp_path == cwd
    assert {"project": {"license": "MIT"}} == data


@patch("typer.secho")
def test_file_path(_, tmp_path):
    pyproject_path = tmp_path / "pyproject.toml"
    pyproject_path.write_text("""
[project]
license = "MIT"
""")

    (cwd, data) = get_cwd_and_pyproject_data(pyproject_path)

    assert tmp_path == cwd
    assert {"project": {"license": "MIT"}} == data


def test_get_cwd_and_pyproject_data_file_not_found():
    with pytest.raises(FileNotFoundError) as e:
        get_cwd_and_pyproject_data(Path("/nonexistent/path"))

    assert "FileNotFoundError: [Errno 2] No such file or directory: '/nonexistent/path'" in e.exconly()
