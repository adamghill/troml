# troml

`troml` provides a list of potential classifiers that could be added to a Python package. It only supports modern Python packages that use the [`pyproject.toml`](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/) standard.

![Screenshot of troml in action](https://github.com/adamghill/troml/blob/main/troml.png?raw=true)

## Usage

1. Go to a directory with source code for a Python package
2. `uvx troml`

### Specify a path

`troml` also accepts a path as the first argument.

`uvx troml /path/to/pypyproject.toml`

## Supported classifiers

### Python version

`troml` will read `project.python-requires` and suggest classifiers based on it.

### Legacy license

`troml` will suggest removing the legacy license classifiers.

### Dependencies

`troml` will suggest classifiers based on the dependencies in `project.dependencies`, `project.dependency-groups`, and `tool.uv.constraint-dependencies`.

### Typing

`troml` will suggest the "Typing :: Typed" classifier based on the existence of the `py.typed` file in the same directory as the `pyproject.toml` file.

## What's with the name?

- The classifiers for Python are called ["Trove classifiers"](https://pypi.org/classifiers/)
- Modern Python packages use TOML for configuration

"trove" 🤝 "TOML"

Yes, I agree, the name is a little weird.

## Development

### Run from source

`uv run troml [PATH-TO-PYPROJECT-TOML]`

### Commands

- unit tests (via `pytest`): `just test`
- linting (via `ruff`): `just lint`
- type checking (via `mypy`): `just type`
- unit test coverage (via `coverage.py`): `just coverage`

## Inspiration

- https://indieweb.social/@adamghill/115174743670090084
- another approach from @kfdm: https://codeberg.org/kfdm/add-classifiers
- post about `add-classifers`: https://paultraylor.net/blog/2025/add-classifiers/
- https://github.com/jvllmr/trove-setup
