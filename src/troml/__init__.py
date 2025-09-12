from copy import copy
from pathlib import Path

import typer
from packaging.requirements import Requirement
from tomllib import load as toml_load

from troml.objects import Libraries, Library

app = typer.Typer()


SUPPORTED_LIBRARIES = Libraries()
SUPPORTED_LIBRARIES.add(Library(name="django", classifier_pattern=r"Framework :: Django :: "))


@app.command()
def suggest(path: Path):
    data = get_pyproject_data(path)
    dependencies = get_dependencies(data)

    project = data.get("project", {})
    classifiers = set(project.get("classifiers", []))
    original_classifiers = copy(classifiers)

    for dependency in dependencies:
        add_classifiers_for_dependency(classifiers=classifiers, dependency=dependency)

    typer.secho("\nCurrent classifiers", fg=typer.colors.YELLOW)
    for classifier in original_classifiers:
        typer.secho(classifier)

    typer.secho("\nSuggested classifiers", fg=typer.colors.YELLOW)

    for classifier in sorted(classifiers):
        typer.secho(classifier)


def get_pyproject_data(path: Path) -> dict:
    pyproject_path = path

    if path.is_dir():
        pyproject_path = path / "pyproject.toml"

    with pyproject_path.open("rb") as f:
        return toml_load(f)


def get_dependencies(data: dict) -> list[str]:
    project = data.get("project", {})
    tool = data.get("tool", {})

    dependencies = []

    for dependency in project.get("dependencies", []):
        typer.secho(f"Found dependency in project.dependencies: {dependency}", fg=typer.colors.GREEN)
        dependencies.append(dependency)

    for dependency_groups in project.get("dependency_groups", []):
        for dependency_group, dependencies in dependency_groups.items():
            for dependency in dependencies:
                typer.secho(
                    f"Found dependency in dependency group, {dependency_group},: {dependency}", fg=typer.colors.GREEN
                )
                dependencies.append(dependency)

    for dependency in tool.get("uv", {}).get("constraint-dependencies", []):
        typer.secho(f"Found dependency in tool.uv.constraint-dependencies: {dependency}", fg=typer.colors.GREEN)
        dependencies.append(dependency)

    return dependencies


def add_classifiers_for_dependency(classifiers: set, dependency: str) -> None:
    requirement = Requirement(dependency)

    if requirement.name.lower() not in SUPPORTED_LIBRARIES.names:
        return

    for library in SUPPORTED_LIBRARIES:
        for version in library.versions:
            if requirement.specifier.contains(version):
                potential_classifier = f"{library.classifier_pattern} {version}"

                if potential_classifier not in classifiers:
                    classifiers.add(potential_classifier)


if __name__ == "__main__":
    app()
