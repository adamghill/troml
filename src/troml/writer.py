from pathlib import Path

from tomlkit import dumps, parse


def write(path: Path, classifiers: list[str]) -> None:
    doc = parse(path.read_bytes())
    toml_classifiers = doc.get("project", {}).get("classifiers", [])

    for classifier in classifiers:
        if classifier not in toml_classifiers:
            toml_classifiers.append(classifier)

    path.write_text(dumps(doc))
