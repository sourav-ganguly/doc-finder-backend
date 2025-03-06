# Python Linting with Ruff

This project uses [Ruff](https://github.com/charliermarsh/ruff) for Python linting and formatting. Ruff is an extremely fast Python linter, written in Rust.

## GitHub Actions Workflow

A GitHub Actions workflow is set up to automatically run Ruff on all pull requests and pushes to the main branches. This helps ensure code quality and consistency.

## Local Setup

To use Ruff locally:

1. Install Ruff:

```bash
pip install ruff
```

2. Run the linter:

```bash
ruff check .
```

3. Run the formatter:

```bash
# Check formatting without modifying files
ruff format --check .

# Fix formatting issues
ruff format .
```

## Pre-commit Hook (Optional)

You can set up a pre-commit hook to automatically run Ruff before each commit:

1. Install pre-commit:

```bash
pip install pre-commit
```

2. Create a `.pre-commit-config.yaml` file in the root of your project:

```yaml
repos:
-   repo: https://github.com/charliermarsh/ruff-pre-commit
    rev: 'v0.1.3'  # Use the latest version
    hooks:
    -   id: ruff
        args: [--fix, --exit-non-zero-on-fix]
    -   id: ruff-format
```

3. Install the pre-commit hook:

```bash
pre-commit install
```

## Configuration

Ruff is configured in the `pyproject.toml` file. See the [Ruff documentation](https://github.com/charliermarsh/ruff) for more details on configuration options.

## Common Issues and Fixes

Here are some common linting issues you might encounter and how to fix them:

1. **Unused imports**: Remove unused imports or add `# noqa: F401` to the line.
2. **Line too long**: Break long lines into multiple lines or use line continuation.
3. **Missing docstrings**: Add docstrings to functions, classes, and modules.
4. **Undefined variables**: Fix typos or import missing variables.

## Ignoring Rules

If you need to ignore a specific rule for a specific line:

```python
# This line has an intentional issue  # noqa: E501
```

For a whole file, add at the top:

```python
# ruff: noqa: E501, F401
```

Or configure rule exceptions in `pyproject.toml`. 