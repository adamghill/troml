from unittest.mock import MagicMock, patch

from troml.classifiers import DependencyClassifier


@patch("typer.secho")
def test_django(_):
    actual = set()

    DependencyClassifier(actual).handle("django>=4.2")

    assert "Framework :: Django" in actual
    assert "Framework :: Django :: 4.2" in actual


@patch("typer.secho")
def test_fastapi(_):
    actual = set()

    DependencyClassifier(actual).handle("fastapi>=0.116.1")

    assert "Framework :: FastAPI" in actual


@patch("typer.secho")
def test_flask(_):
    actual = set()

    DependencyClassifier(actual).handle("Flask>=3.1.2")

    assert "Framework :: Flask" in actual


@patch("typer.secho")
def test_django_cms(_):
    actual = set()

    DependencyClassifier(actual).handle("django-cms>=5.0.2")

    assert "Framework :: Django CMS" in actual


@patch("typer.secho")
def test_unsupported(_):
    actual = set()

    DependencyClassifier(actual).handle("nonexistent-package>=1.0.0")

    assert 0 == len(actual)


def test_extracts_specifier_versions():
    expected = {"3.8"}
    classifier = DependencyClassifier(set())

    # Test with a requirement that has multiple specifiers
    requirement = MagicMock()
    requirement.specifier = MagicMock()
    requirement.specifier.__iter__.return_value = [
        MagicMock(operator=">=", version="3.8.0"),
        MagicMock(operator="<", version="4.0.0"),
    ]

    # Mock version_parse to return version objects
    with patch("troml.classifiers.version_parse") as mock_parse:
        mock_parse.side_effect = lambda _: MagicMock(major=3, minor=8, patch=0)
        actual = classifier.get_specifier_versions(requirement)

    assert expected == actual
