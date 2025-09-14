from copy import copy
from pathlib import Path
from typing import Annotated

import typer

from troml.classifiers import (
    DependenciesClassifier,
    LicenseClassifier,
    PythonClassifier,
    TypingTypedClassifier,
)
from troml.loader import get_cwd_and_pyproject_data
from troml.utils import echo_classifiers
from troml.writer import write

app = typer.Typer()


@app.command()
def suggest(
    path: Annotated[Path, typer.Argument(help="The path of the pyproject.toml.")] = Path("."),
    fix: Annotated[bool, typer.Option(help="Automatically update classifiers.")] = False,  # noqa: FBT002
) -> None:
    """Suggest new trove classifiers for a project."""

    (cwd, data) = get_cwd_and_pyproject_data(path)

    project = data.get("project", {})
    classifiers = set(project.get("classifiers", []))
    current_classifiers = copy(classifiers)

    TypingTypedClassifier(classifiers).handle(cwd=cwd)
    LicenseClassifier(classifiers).handle(project=project)
    PythonClassifier(classifiers).handle(project=project)
    DependenciesClassifier(classifiers).handle(data=data)

    classifiers = sorted(classifiers)

    if sorted(current_classifiers) == classifiers:
        typer.secho("\nNo classifier suggestions", fg=typer.colors.GREEN)
    else:
        # Print out current and suggested classifiers
        echo_classifiers("\nCurrent classifiers TOML", current_classifiers)
        echo_classifiers("\nSuggested classifiers TOML", classifiers)

        if fix:
            pyproject_path = cwd / "pyproject.toml"
            write(path=pyproject_path, classifiers=classifiers)


if __name__ == "__main__":
    app()
