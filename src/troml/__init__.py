from copy import copy
from pathlib import Path
from typing import Annotated

import typer

from troml.classifiers import DependenciesClassifier, LicenseClassifier, PythonClassifier, TypingTypedClassifier
from troml.loader import get_cwd_and_pyproject_data
from troml.utils import echo_classifiers

app = typer.Typer()


@app.command()
def suggest(path: Annotated[Path, typer.Argument(help="The path of the pyproject.toml.")] = Path(".")) -> None:
    """Suggest new trove classifiers for a project."""

    (cwd, data) = get_cwd_and_pyproject_data(path)

    project = data.get("project", {})
    classifiers = set(project.get("classifiers", []))
    current_classifiers = copy(classifiers)

    TypingTypedClassifier(classifiers).handle(cwd=cwd)
    LicenseClassifier(classifiers).handle(project=project)
    PythonClassifier(classifiers).handle(project=project)
    DependenciesClassifier(classifiers).handle(data=data)

    # Print out current and suggested classifiers
    echo_classifiers("\nCurrent classifiers TOML", current_classifiers)
    echo_classifiers("\nSuggested classifiers TOML", sorted(classifiers))


if __name__ == "__main__":
    app()
