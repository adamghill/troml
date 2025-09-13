from unittest.mock import patch

import pytest

from troml.classifiers import (
    Classifier,
    DependenciesClassifier,
    DependencyClassifier,
    LicenseClassifier,
    PythonClassifier,
    TypingTypedClassifier,
)


def test_base_classifier_raises_not_implemented():
    """Test that the base Classifier raises NotImplementedError."""
    classifier = Classifier(set())
    with pytest.raises(NotImplementedError):
        classifier.handle()


class TestTypingTypedClassifier:
    def test_adds_typed_classifier_when_py_typed_exists(self, tmp_path):
        """Test that TypingTypedClassifier adds the typed classifier when py.typed exists."""
        # Create a temporary py.typed file
        py_typed = tmp_path / "py.typed"
        py_typed.touch()

        classifiers = set()
        classifier = TypingTypedClassifier(classifiers)

        with patch("typer.secho") as mock_secho:
            classifier.handle(tmp_path)

        assert "Typing :: Typed" in classifiers
        mock_secho.assert_called_once()

    def test_no_classifier_added_when_no_py_typed(self, tmp_path):
        """Test that no classifier is added when py.typed doesn't exist."""
        classifiers = set()
        classifier = TypingTypedClassifier(classifiers)

        with patch("typer.secho") as mock_secho:
            classifier.handle(tmp_path)

        assert "Typing :: Typed" not in classifiers
        mock_secho.assert_not_called()


class TestLicenseClassifier:
    def test_removes_legacy_license_classifier(self):
        """Test that legacy license classifiers are removed when license is specified."""
        classifiers = {"License :: OSI Approved :: MIT License"}
        project = {"license": "MIT"}

        classifier = LicenseClassifier(classifiers)

        with patch("typer.secho") as mock_secho:
            classifier.handle(project)

        assert not any(c.startswith("License ::") for c in classifiers)
        mock_secho.assert_called_once()

    def test_no_change_when_no_license_specified(self):
        """Test that license classifiers remain unchanged when no license is specified."""
        classifiers = {"License :: OSI Approved :: MIT License"}
        project = {}

        classifier = LicenseClassifier(classifiers)

        with patch("typer.secho") as mock_secho:
            classifier.handle(project)

        assert "License :: OSI Approved :: MIT License" in classifiers
        mock_secho.assert_not_called()


class TestPythonClassifier:
    def test_processes_python_requirement(self):
        """Test that Python version requirements are processed correctly."""
        classifiers = set()
        project = {"requires-python": ">=3.8"}

        with patch.object(DependencyClassifier, "handle") as mock_handle:
            classifier = PythonClassifier(classifiers)
            classifier.handle(project)

        mock_handle.assert_called_once_with("Python>=3.8")

    def test_no_action_when_no_requires_python(self):
        """Test that nothing happens when requires-python is not specified."""
        classifiers = set()
        project = {}

        with patch("typer.secho") as mock_secho, patch.object(DependencyClassifier, "handle") as mock_handle:
            classifier = PythonClassifier(classifiers)
            classifier.handle(project)

        mock_secho.assert_not_called()
        mock_handle.assert_not_called()


class TestDependenciesClassifier:
    def test_processes_all_dependencies(self):
        """Test that dependencies from all sources are processed."""
        classifiers = set()
        data = {
            "project": {
                "dependencies": ["django>=4.2", "requests"],
                "dependency-groups": {"dev": ["pytest"]},
            },
            "tool": {"uv": {"constraint-dependencies": ["uv>=1.0.0"]}},
        }

        with patch.object(DependencyClassifier, "handle") as mock_handle:
            classifier = DependenciesClassifier(classifiers)
            classifier.handle(data)

        assert mock_handle.call_count == 4  # django, requests, pytest, uv
        mock_handle.assert_any_call("django>=4.2")
        mock_handle.assert_any_call("requests")
        mock_handle.assert_any_call("pytest")
        mock_handle.assert_any_call("uv>=1.0.0")


class TestDependencyClassifier:
    pass
