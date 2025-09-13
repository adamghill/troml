import re
from unittest.mock import patch

from troml.config import DJANGO_LIBRARY
from troml.objects import Library

mock_classifiers = [
    "Framework :: Django :: 4.2",
    "Framework :: Django :: 4.1",
    "Framework :: Django :: 3.2",
    "Framework :: Django :: 3.2.1",
    "Framework :: Django :: 2",
    "Framework :: Django",
    "Framework :: Flask",
    "Framework :: Pydantic :: 1",
]


@patch("troml.objects.all_classifiers", mock_classifiers)
def test():
    DJANGO_LIBRARY.set_versions_from_classifiers()

    assert isinstance(DJANGO_LIBRARY.classifier_re, re.Pattern)
    assert DJANGO_LIBRARY.versions == {
        "4.2",
        "4.1",
        "3.2",
        "2",
        None,
    }


def test_no_versions():
    actual = Library(
        name="fake-library",
        classifier_base="Framework :: FakeLibrary",
        classifier_pattern=r"^Framework :: FakeLibrary( :: (?P<version>\d+(\.\d+)*))?$",
    )

    assert actual.versions == set()
