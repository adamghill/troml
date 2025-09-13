from dataclasses import dataclass
from pathlib import Path

import typer
from packaging.requirements import Requirement
from packaging.version import parse as version_parse

from troml.config import SUPPORTED_LIBRARIES


@dataclass
class Classifier:
    """Base classifier."""

    classifiers: set

    def handle(self, *args, **kwargs) -> None:
        raise NotImplementedError()


@dataclass
class TypingTypedClassifier(Classifier):
    """Typing :: Typed classifier."""

    def handle(self, cwd: Path) -> None:
        if (cwd / "py.typed").exists():
            typer.secho(" - Add typed classifier based on py.typed file", fg=typer.colors.GREEN)
            self.classifiers.add("Typing :: Typed")


@dataclass
class LicenseClassifier(Classifier):
    """Deal with the legacy license classifier."""

    def handle(self, project: dict) -> None:
        if project.get("license") or project.get("license-files"):
            for classifier in list(self.classifiers):
                if classifier.startswith("License :: "):
                    typer.secho(
                        " - Remove legacy license classifier (https://peps.python.org/pep-0639/#deprecate-license-classifiers)",
                        fg=typer.colors.RED,
                    )
                    self.classifiers.remove(classifier)


@dataclass
class PythonClassifier(Classifier):
    """Python classifiers."""

    def handle(self, project: dict) -> None:
        if requires_python := project.get("requires-python"):
            typer.secho(f" - Python requirement: {requires_python}", fg=typer.colors.GREEN)

            dependency = f"Python{requires_python}"
            DependencyClassifier(self.classifiers).handle(dependency)


@dataclass
class DependenciesClassifier(Classifier):
    """Dependencies classifiers."""

    def handle(self, data: dict) -> None:
        for dependency in self.get_dependencies(data=data):
            DependencyClassifier(self.classifiers).handle(dependency)

    def get_dependencies(self, data: dict) -> list[str]:
        project = data.get("project", {})
        tool = data.get("tool", {})

        dependencies = []

        if project_dependencies := project.get("dependencies", []):
            for dependency in project_dependencies:
                dependencies.append(dependency)

        for _, group_dependencies in project.get("dependency-groups", {}).items():
            for dependency in group_dependencies:
                # `dependency`` can be a `dict` with a "include-group" key, however those will already be added to the
                # list of dependencies
                if isinstance(dependency, str):
                    dependencies.append(dependency)

        if constraint_dependencies := tool.get("uv", {}).get("constraint-dependencies", []):
            for dependency in constraint_dependencies:
                dependencies.append(dependency)

        # TODO: Handle non-standard tools here, e.g. poetry, etc

        return dependencies


@dataclass
class DependencyClassifier(Classifier):
    """Dependency classifiers"""

    def handle(self, dependency: str) -> None:
        requirement = Requirement(dependency)

        if library := SUPPORTED_LIBRARIES.get(requirement.name):
            specifier_versions = self.get_specifier_versions(requirement=requirement)
            new_classifiers: set = set()

            for version in library.versions:
                potential_classifier = ""

                if not version:
                    potential_classifier = library.classifier_base
                elif requirement.specifier.contains(version) or version in specifier_versions:
                    potential_classifier = f"{library.classifier_base} :: {version}"
                else:
                    continue

                if potential_classifier and potential_classifier not in (self.classifiers | new_classifiers):
                    new_classifiers.add(potential_classifier)

            self.classifiers.update(new_classifiers)

            if len(new_classifiers) > 1:
                typer.secho(f" - Add {len(new_classifiers)} classifiers for {requirement.name}", fg=typer.colors.GREEN)
            elif len(new_classifiers) == 1:
                typer.secho(f" - Add classifier for {requirement.name}", fg=typer.colors.GREEN)

    def get_specifier_versions(self, requirement: Requirement) -> set[str]:
        """Get the major.minor versions in requirement specifier for potential inclusion in classifiers.

        This ensures `Python>=3.9.7` requirement includes "Programming Language :: Python :: 3.9" in classifiers
        """

        specifier_versions = set()

        for specifier in requirement.specifier:
            version = version_parse(specifier.version)
            major_minor_version = f"{version.major}.{version.minor}"

            if major_minor_version not in specifier_versions:
                specifier_versions.add(major_minor_version)

        return specifier_versions
