from pathlib import Path
from typing import Annotated

import typer

from troml.classifiers import get_suggested_classifiers
from troml.loader import get_path
from troml.utils import echo_classifiers
from troml.writer import write

app = typer.Typer()


@app.command()
def command(
    path: Annotated[Path, typer.Argument(help="The path of the pyproject.toml.")] = Path("."),
    fix: Annotated[bool, typer.Option(help="Automatically update classifiers.")] = False,  # noqa: FBT002
    multiline: Annotated[bool, typer.Option(help="Make classifiers multiline.")] = True,  # noqa: FBT002
) -> None:
    """Suggest new classifiers for a library."""

    path = get_path(path)
    (classifiers, suggested_classifiers) = get_suggested_classifiers(path=path)

    if sorted(classifiers) == suggested_classifiers:
        typer.secho("\nNo classifier suggestions", fg=typer.colors.GREEN)
    else:
        # Print out current and suggested classifiers
        echo_classifiers("\nCurrent classifiers TOML", classifiers)
        echo_classifiers("\nSuggested classifiers TOML", suggested_classifiers)

        if fix:
            pyproject_path = path / "pyproject.toml"
            typer.secho(f"\nWriting classifier suggestions to {pyproject_path}", fg=typer.colors.GREEN)
            write(pyproject_path=pyproject_path, classifiers=suggested_classifiers, multiline=multiline)
