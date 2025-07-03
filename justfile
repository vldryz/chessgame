[private]
default:
    @just --list

alias fmt := format

# Run formatting
[group('QA')]
format:
    uv run ruff format

# Run lint checks
[group('QA')]
lint:
    uv run ruff check

# Shortcut to fix unsafe ruff errors
[group('QA')]
unsafe-fix:
    uv run ruff check --fix --unsafe-fixes

# Run type checking
[group('QA')]
typecheck:
    uv run mypy

# Run tests
[group('test')]
test:
    uv run pytest

# Run same checks as in CI
[group('CI')]
ci-check: format lint typecheck test

# Clean up caches and build artifacts
[group('misc')]
clean:
    @rm -rf .mypy_cache/
    @rm -rf .pytest_cache/
    @ruff clean
    @find . -type f -name '*.py[co]' -delete -or -type d -name __pycache__ -exec rm -r {} +
