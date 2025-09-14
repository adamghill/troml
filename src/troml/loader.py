from pathlib import Path
from typing import Any

import typer
from tomlkit import parse


def get_cwd(path: Path | None = None) -> Path:
    path = path or Path(".").resolve()

    if not path.exists():
        raise FileNotFoundError("No such directory")

    if not path.is_dir():
        raise AssertionError("Path is not a directory")

    return path


def get_pyproject_data(cwd: Path) -> dict[str, Any]:
    pyproject_path = cwd / "pyproject.toml"

    typer.secho(f"Loading data from '{pyproject_path.parent}'", fg=typer.colors.BLUE)

    return dict(parse(pyproject_path.read_bytes()))
