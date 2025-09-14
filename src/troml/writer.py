from pathlib import Path

from tomlkit import dumps, parse
from tomlkit.items import Array, Trivia


def write(pyproject_path: Path, classifiers: list[str], multiline: bool = True) -> None:  # noqa: FBT001, FBT002
    doc = parse(pyproject_path.read_text())

    if "project" not in doc:
        raise AssertionError("Missing `project` table")

    array = Array([], trivia=Trivia(), multiline=multiline)

    for classifier in sorted(classifiers):
        if multiline:
            array.add_line(classifier)
        else:
            array.append(classifier)

    doc["project"]["classifiers"] = array  # type: ignore[index]

    pyproject_path.write_text(dumps(doc))
