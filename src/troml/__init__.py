from copy import copy
from pathlib import Path
from typing import Annotated

import typer
from typer import Context

from troml.classifiers import (
    DependenciesClassifier,
    LicenseClassifier,
    PythonClassifier,
    TypingTypedClassifier,
)
from troml.loader import get_cwd, get_pyproject_data
from troml.utils import echo_classifiers
from troml.writer import write

app = typer.Typer()


@app.callback(invoke_without_command=True)
def callback(ctx: Context) -> None:
    """Suggests classifiers for a Python package."""

    if ctx.invoked_subcommand is None:
        ctx.invoke(suggest)


@app.command()
def check(path: Annotated[Path, typer.Argument(help="The path of the pyproject.toml.")] = Path(".")) -> None:
    """Check if there are suggested classifiers for a library."""

    cwd = get_cwd(path)
    (classifiers, suggested_classifiers) = get_suggested_classifiers(cwd=cwd)

    if sorted(classifiers) != suggested_classifiers:
        typer.secho("\nThere are suggested classifiers", err=True, fg=typer.colors.RED)
        raise typer.Exit(1)

    typer.secho("\nNo suggested classifiers ✨", fg=typer.colors.GREEN)


@app.command()
def suggest(
    path: Annotated[Path, typer.Argument(help="The path of the pyproject.toml.")] = Path("."),
    fix: Annotated[bool, typer.Option(help="Automatically update classifiers.")] = False,  # noqa: FBT002
    multiline: Annotated[bool, typer.Option(help="Make classifiers multiline.")] = True,  # noqa: FBT002
) -> None:
    """Suggest new classifiers for a library."""

    cwd = get_cwd(path)
    (classifiers, suggested_classifiers) = get_suggested_classifiers(cwd=cwd)

    if sorted(classifiers) == suggested_classifiers:
        typer.secho("\nNo classifier suggestions", fg=typer.colors.GREEN)
    else:
        # Print out current and suggested classifiers
        echo_classifiers("\nCurrent classifiers TOML", classifiers)
        echo_classifiers("\nSuggested classifiers TOML", suggested_classifiers)

        if fix:
            pyproject_path = cwd / "pyproject.toml"
            typer.secho(f"\nWriting classifier suggestions to {pyproject_path}", fg=typer.colors.GREEN)
            write(pyproject_path=pyproject_path, classifiers=suggested_classifiers, multiline=multiline)


def get_suggested_classifiers(cwd: Path) -> tuple[list[str], list[str]]:
    """Get suggested classifiers for a library."""

    data = get_pyproject_data(cwd)

    project = data.get("project", {})
    classifiers = project.get("classifiers", [])

    suggested_classifiers = set(copy(classifiers))

    TypingTypedClassifier(suggested_classifiers).handle(cwd=cwd)
    LicenseClassifier(suggested_classifiers).handle(project=project)
    PythonClassifier(suggested_classifiers).handle(project=project)
    DependenciesClassifier(suggested_classifiers).handle(data=data)

    sorted_suggested_classifiers = sorted(suggested_classifiers)

    return (classifiers, sorted_suggested_classifiers)


if __name__ == "__main__":
    app()
