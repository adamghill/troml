import logging
from datetime import datetime
from json import dumps as json_dumps
from json import loads as json_loads
from pathlib import Path
from typing import Annotated

import httpx
import typer
from packaging.requirements import Requirement
from tomlkit import dumps as toml_dumps

from troml.commands import Output
from troml.commands.hypothesize import Source, hypothesize

logger = logging.getLogger(__name__)

app = typer.Typer()


def get_dependency_requires_python(dependency: str, no_cache: bool = False) -> dict:
    url = f"https://pypi.org/simple/{dependency}/"
    file_cache_key = "pypi-simple"

    app_dir = Path(typer.get_app_dir("troml"))
    app_dir.mkdir(exist_ok=True)
    cache_path = app_dir / dependency

    cache_path.mkdir(exist_ok=True)
    file_path = cache_path / file_cache_key

    # If no_cache is set, always fetch fresh data and overwrite the cache
    if (
        no_cache
        or not file_path.exists()
        or (datetime.now() - datetime.fromtimestamp(file_path.stat().st_mtime)).total_seconds() > 3600
    ):
        logger.debug(f"Fetch data from: {url}")
        res = httpx.get(url, headers={"Accept": "application/vnd.pypi.simple.v1+json"}, follow_redirects=True)
        res.raise_for_status()

        data = json_dumps(res.json())
        file_path.write_text(data)
    else:
        logger.debug(f"Use cached file: {file_path}")

    data = json_loads(file_path.read_text())

    result = {}

    for file in data.get("files", []):
        if file.get("yanked", False):
            continue

        filename = file.get("filename")

        if filename.endswith(".tar.gz"):
            filename = filename[:-7]
        elif filename.endswith(".whl"):
            filename = filename[:-4]

        filename_split = filename.split("-")

        if len(filename_split) > 1:
            name = filename_split[0]
            version = filename_split[1]
        else:
            # logger.debug("Unknown filename")
            continue

        if name.lower() != dependency.lower():
            continue

        if not version:
            continue

        requires_python = file.get("requires-python")

        if not requires_python:
            continue

        result[version] = {"requires_python": requires_python}

    return result


@app.command()
def matrix(
    path: Annotated[Path, typer.Argument(help="The path of the pyproject.toml.")] = Path("."),
    dependencies: Annotated[
        list[str] | None, typer.Option("--dependency", help="The dependency for the matrix.")
    ] = None,
    source: Annotated[Source, typer.Option(help="Source to use to calculate testable versions.")] = Source.CLASSIFIERS,
    output: Annotated[Output, typer.Option(help="The style of output. Defaults to 'json'.")] = Output.JSON,
    pretty: Annotated[bool, typer.Option(help="Prettier output.")] = False,
    no_cache: Annotated[bool, typer.Option("--no-cache", help="Bypass and refresh cache for remote lookups.")] = False,
) -> None:
    """Calculate a matrix of testable dependencies for a requirement."""

    python_versions = hypothesize(path=path, source=source)
    result = {"include": []}

    dependencies = [d.lower() for d in dependencies]

    for python_version in python_versions:
        for dependency in dependencies:
            dependency_versions = hypothesize(path=path, framework=dependency, source=source)

            dependency_requires_python_hash = get_dependency_requires_python(dependency=dependency, no_cache=no_cache)

            for dependency_version in dependency_versions:
                if dependency_data := dependency_requires_python_hash.get(dependency_version):
                    dependency_requires_python = dependency_data["requires_python"]

                    python_requirement = Requirement(f"Python{dependency_requires_python}")

                    if python_requirement.specifier.contains(python_version):
                        result["include"].append(
                            {
                                "python-version": python_version,
                                f"{dependency.lower()}-version": dependency_version,
                            }
                        )

    if output == Output.JSON:
        if pretty:
            print(json_dumps(result, indent=2))
        else:
            print(json_dumps(result))
    elif output == Output.TOML:
        print(toml_dumps(result))
    else:
        raise NotImplementedError(f"Unknown output: {output}")
