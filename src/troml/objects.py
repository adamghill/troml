import re
from dataclasses import dataclass, field

from trove_classifiers import all_classifiers


@dataclass
class Library:
    name: str
    classifier_pattern: str
    classifier_base: str
    versions: set = field(default_factory=set)

    def __init__(self, name: str, classifier_base: str, classifier_pattern: str):
        self.name = name
        self.classifier_base = classifier_base
        self.classifier_pattern = classifier_pattern
        self.classifier_re = re.compile(classifier_pattern)

        self.set_versions_from_classifiers()

    def set_versions_from_classifiers(self):
        self.versions = set()

        for classifier in all_classifiers:
            if match := self.classifier_re.match(classifier):
                version = match.groupdict().get("version")

                self.versions.add(version)


@dataclass
class Libraries:
    libraries: list[Library] = field(default_factory=list)

    def add(self, library: Library):
        self.libraries.append(library)

    def get(self, name: str) -> Library | None:
        return next(filter(lambda library: library.name.lower() == name.lower(), self.libraries), None)

    def __iter__(self):
        return self.libraries.__iter__()
