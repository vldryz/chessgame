[private]
default:
    @just --list

alias format := fmt

# Run formatting
[group('QA')]
fmt:
    uv run ruff format

# Run lint checks
[group('QA')]
lint:
    uv run ruff check

# Shortcut to fix unsafe ruff errors
[group('QA')]
unsafe-fix:
    uv run ruff check --fix --unsafe-fixes

# Run type checking with mypy
[group('QA')]
mypy:
    uv run mypy

# Run type checking with ty
[group('QA')]
ty:
    uvx ty check

# Run tests
[group('test')]
test:
    uv run pytest

# Run same checks as in CI
[group('CI')]
ci-check: lint fmt mypy test

# Clean up caches and build artifacts
[group('misc')]
clean:
    @rm -rf .mypy_cache/
    @rm -rf .pytest_cache/
    @ruff clean --quiet
    @find . -type f -name '*.py[co]' -delete -or -type d -name __pycache__ -exec rm -r {} +

# Format the justfile itself
[group('misc')]
format-justfile:
    just --fmt --unstable
