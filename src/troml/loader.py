from pathlib import Path
from tomllib import load as toml_load
from typing import Any

import typer


def get_cwd_and_pyproject_data(path: Path | None = None) -> tuple[Path, dict]:
    path = path or Path(".").resolve()

    data = get_pyproject_data(path)
    cwd = path

    if not path.is_dir():
        cwd = path.parent

    return (cwd, data)


def get_pyproject_data(path: Path) -> dict[str, Any]:
    pyproject_path = path

    if path.is_dir():
        pyproject_path = path / "pyproject.toml"

    typer.secho(f"Loading data from '{pyproject_path.parent}'", fg=typer.colors.BLUE)

    with pyproject_path.open("rb") as f:
        return dict(toml_load(f))
