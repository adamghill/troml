from pathlib import Path

import pytest

from troml.loader import get_cwd


def test_missing_path():
    with pytest.raises(FileNotFoundError) as e:
        get_cwd(Path("/nonexistent/path"))

    assert "No such directory" in e.exconly()


def test_invalid_path(tmp_path):
    with pytest.raises(AssertionError) as e:
        file_path = tmp_path / "pyproject.toml"
        file_path.touch()
        get_cwd(file_path)

    assert "Path is not a directory" in e.exconly()
