# 0.4.1

- Fix to only show typed output when that classified is added.

# 0.4.0

- Add `check` command.
- Add `--fix` option to `suggest` command.
- Add `--multiline` extra option for `--fix`.

# 0.3.0

- Much more generic handling of dependency classifiers, so Flask, Django CMS, FastAPI, etc. now work as expected.

# 0.2.0

- Improve output.

# 0.1.1

- Fix missing `packaging` requirement.

# 0.1.0

- Python classifiers based on `project.python-requires`
- Framework classifiers based on dependencies defined in `project.dependencies`, `project.dependency-groups`, `tool.uv.constraint-dependencies` (only supports Django for now)
- Typed classifer for an existing `py.typed` file
