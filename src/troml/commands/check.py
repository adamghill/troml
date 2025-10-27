from pathlib import Path
from typing import Annotated

import typer

from troml.classifiers import get_suggested_classifiers
from troml.loader import get_path

app = typer.Typer()


@app.command()
def command(path: Annotated[Path, typer.Argument(help="The path of the pyproject.toml.")] = Path(".")) -> None:
    """Check if there are suggested classifiers for a library."""

    path = get_path(path)
    (classifiers, suggested_classifiers) = get_suggested_classifiers(cwd=path)

    if sorted(classifiers) != suggested_classifiers:
        typer.secho("\nThere are suggested classifiers", err=True, fg=typer.colors.RED)
        raise typer.Exit(1)

    typer.secho("\nNo suggested classifiers ✨", fg=typer.colors.GREEN)
