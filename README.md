# troml

`troml` investigates a modern Python package, i.e. a package with a `pyproject.toml` file, and provides a list of potential classifiers that could be added.

![Screenshot of troml in action](troml.png)

## Usage

1. Go to a directory with source code for a modern Python package
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

- The classifiers for Python are called "trove classifiers"
- Modern Python packages use TOML

Hence: "trove" + "TOML".

Yes, I agree, the name is a little weird.

## Development

### Run from source

`uv run troml [PATH-TO-PYPROJECT-TOML]`

### Tests

`just test`

## Inspiration

- https://indieweb.social/@adamghill/115174743670090084
- another approach from @kfdm: https://codeberg.org/kfdm/add-classifiers
