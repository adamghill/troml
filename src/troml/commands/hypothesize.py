import re
from datetime import date
from enum import Enum
from json import dumps as json_dumps
from pathlib import Path
from typing import Annotated

import typer
from packaging.requirements import Requirement
from packaging.version import Version
from packaging.version import parse as version_parse
from tomlkit import dumps as toml_dumps

from troml.classifiers import DependenciesClassifier
from troml.commands import Output
from troml.loader import get_path, get_pyproject_data

app = typer.Typer()


class Source(str, Enum):
    DEPENDENCIES = "dependencies"
    CLASSIFIERS = "classifiers"


PYTHON_EOL_DATES = {
    "3.13": date(2029, 10, 31),
    "3.12": date(2028, 10, 31),
    "3.11": date(2027, 10, 31),
    "3.10": date(2026, 10, 31),
    "3.9": date(2025, 10, 31),
    "3.8": date(2024, 10, 7),
    "3.7": date(2023, 6, 27),
    "3.6": date(2021, 12, 23),
    "3.5": date(2020, 9, 30),
    "3.4": date(2019, 3, 18),
    "3.3": date(2017, 9, 29),
    "3.2": date(2016, 2, 20),
    "2.7": date(2020, 1, 1),
    "3.1": date(2012, 4, 9),
    "3.0": date(2009, 6, 27),
    "2.6": date(2013, 10, 29),
}


def supported_python_versions() -> set[str]:
    """Return a list of supported (non-EOL) Python versions."""

    today = date.today()  # noqa: DTZ011

    return {v for v, eol in PYTHON_EOL_DATES.items() if today <= eol}


current_supported_python_versions = supported_python_versions()


@app.command(name="hypothesize")
def command(
    path: Annotated[Path, typer.Argument(help="The path of the pyproject.toml.")] = Path("."),
    framework: Annotated[str | None, typer.Option(help="sadf")] = None,
    source: Annotated[
        Source, typer.Option(help="Source to use to calculate testable versions. Defaults to 'classifiers'.")
    ] = Source.CLASSIFIERS,
    output: Annotated[Output, typer.Option(help="The style of output. Defaults to 'json'.")] = Output.JSON,
) -> None:
    results = hypothesize(path=path, framework=framework, source=source)

    if output == Output.JSON:
        typer.echo(json_dumps(results))
    elif output == Output.TOML:
        typer.echo(toml_dumps(results))
    elif output == Output.NEW_LINE_DELIMITED:
        for v in results:
            typer.echo(v)
    else:
        raise NotImplementedError(f"Unknown output: {output}")


def hypothesize(
    path: Path = Path("."),
    framework: str | None = None,
    source: Source = Source.CLASSIFIERS,
) -> list[str]:
    """Calculate testable dependencies for a requirement."""

    path = get_path(path)
    data = get_pyproject_data(path, is_verbose=False)
    project = data.get("project")

    if source == Source.DEPENDENCIES:
        requirement = get_requirement(data=data, framework=framework)

        versions = set()
        minor_versions = set()

        """
        Add versions for the floor and ceilings of major.minor versions of the specifier.

        Examples:
            - if the specifier is "Python>=3.9.7", include 3.9.7 in the `versions`
            - if the specifier is "Python<=3.9.7", include 3.9.7 in the `versions`
            - if the specifier is "Python<3.9.7", include 3.9.6 in the `versions`
            - if the specifier is "Python>3.9.7", include 3.9.8 in the `versions`
        """
        for specifier in requirement.specifier:
            version = version_parse(specifier.version)
            minor_versions.add(version.minor)

            if framework is None:
                if f"{version.major}.{version.minor}" not in current_supported_python_versions:
                    continue

            if specifier.operator in ("<=", ">=", "=="):
                versions.add(version)
            elif specifier.operator == "<":
                if version.micro > 0:
                    version = Version(f"{version.major}.{version.minor}.{version.micro - 1}")
                    versions.add(version)
            elif specifier.operator == ">":
                # TODO: Check that micro version is valid before adding it
                # Could use https://endoflife.date/api/python.json, maybe
                version = Version(f"{version.major}.{version.minor}.{version.micro + 1}")
                versions.add(version)
            elif specifier.operator == "!=":
                raise AssertionError("Operator not supported")

        add_supported_versions(
            versions=versions, minor_versions=minor_versions, requirement=requirement, framework=framework
        )

        return sorted([str(version) for version in versions])
    elif source == Source.CLASSIFIERS:
        classifiers = project.get("classifiers")
        requirement_name = framework or "Python"

        dependency_pattern = rf"^(Framework|Programming Language) :: {requirement_name} :: (?P<version>\d+(\.\d+)?)$"
        versions = set()

        for classifier in classifiers:
            if match := re.match(dependency_pattern, classifier, re.IGNORECASE):
                versions.add(match.groupdict()["version"])

        return sorted(versions)

    raise AssertionError("Unknown source")


def get_requirement(data: dict, framework: str | None) -> Requirement:
    requirement = None

    if framework is None:
        requires_python = data.get("project", {}).get("requires-python")
        requirement_specifier = f"Python{requires_python}"

        requirement = Requirement(requirement_specifier)
    else:
        classifiers = set()
        dependencies = DependenciesClassifier(classifiers).get_dependencies(data)

        for dependency in dependencies:
            dependency_requirement = Requirement(dependency)

            if dependency_requirement.name.lower() == framework.lower():
                requirement = dependency_requirement

    if requirement is None:
        raise AssertionError(f"Framework could not be found: {framework}")

    return requirement


def add_supported_versions(versions, minor_versions: set[str], requirement: Requirement, framework: str | None):
    # TODO: Support other dependencies
    if framework is None:
        # Add versions of Python that are currently supported and fit within the specifiers
        for supported_version in current_supported_python_versions:
            version = version_parse(supported_version)

            if requirement.specifier.contains(version):
                if version.minor not in minor_versions:
                    versions.add(version)
