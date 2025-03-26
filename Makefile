.DEFAULT_GOAL := help
SHELL := /bin/bash

.PHONY: lint
lint:  ## Run lint checks
	uv run ruff format --check
	uv run ruff check --no-fix
	uv run mypy

.PHONY: fmt
fmt:  ## Run formatting
	uv run ruff format
	uv run ruff check

.PHONY: test
test:  ## Run tests
	uv run pytest tests/

.PHONY: clean
clean:  ## Clean up caches and build artifacts
	@rm -rf .mypy_cache/
	@rm -rf .pytest_cache/
	@ruff clean
	@find . -type f -name '*.py[co]' -delete -or -type d -name __pycache__ -exec rm -r {} +

.PHONY: help
help:  ## Display this help screen
	@echo -e "\033[1mAvailable commands:\033[0m"
	@grep -E '^[a-z.A-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-22s\033[0m %s\n", $$1, $$2}' | sort
	@echo
