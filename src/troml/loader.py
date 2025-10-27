from pathlib import Path
from typing import Any

import typer
from tomlkit import parse


def get_path(path: Path | None = None) -> Path:
    path = path or Path(".").resolve()

    if not path.exists():
        raise FileNotFoundError("No such directory")

    if not path.is_dir():
        path = path.parent

    return path


def get_pyproject_data(path: Path, is_verbose: bool = True) -> dict[str, Any]:
    pyproject_path = path / "pyproject.toml"

    if is_verbose:
        typer.secho(f"Loading data from '{pyproject_path.parent}'", fg=typer.colors.BLUE)

    return dict(parse(pyproject_path.read_bytes()))
