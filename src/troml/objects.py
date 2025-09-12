import re
from dataclasses import dataclass, field

from trove_classifiers import all_classifiers


@dataclass
class Library:
    name: str
    classifier_pattern: str
    versions: set = field(default_factory=set)

    def __init__(self, name: str, classifier_pattern: str):
        self.name = name
        self.classifier_pattern = classifier_pattern
        self.classifier_re = re.compile(classifier_pattern)

        self.versions = set()
        self.get_versions_from_classifiers()

    def get_versions_from_classifiers(self):
        for classifier in all_classifiers:
            if self.classifier_re.match(classifier):
                version = self.classifier_re.sub("", classifier)

                self.versions.add(version)


@dataclass
class Libraries:
    libraries: list[Library] = field(default_factory=list)
    names: set[str] = field(default_factory=set)

    def add(self, library: Library):
        self.libraries.append(library)
        self.names.add(library.name)

    def __iter__(self):
        return self.libraries.__iter__()
