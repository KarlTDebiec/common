# Instructions

## Tools

* This repository uses `uv`. Use `uv run` when executing tools.
* Formatting: `uv run black`
* Linting: `uv run ruff check`
* Type checking: `uv run pyright`

## Code Style

* Include the standard copyright header at the top of the file.
* Include a module docstring at the top of each file.
* Immediate after the module docstring, include `from __future__ import annotations`,
  unless the file is empty.
* All imports should use relative paths starting with `.` rather than absolute imports.
* In `__init__.py` files, only import classes from the module, not functions or
  variables.
* Use the `logging` module rather than `print` for any user-facing output in scripts or
  libraries.

## Documentation

* Use Markdown for formatting.
* Do not use reStructuredText markup.
* Provide docstrings for all classes and functions, including internal helpers prefixed
  with an underscore.
* Format docstrings using Google style, with the following tweaks.
    * Use "Arguments:" instead of "Args:".
    * Do not include a blank link between the "Arguments:" and "Returns:" sections.
