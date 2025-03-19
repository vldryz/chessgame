.DEFAULT_GOAL := help
SHELL := /bin/bash

.PHONY: lint
lint:  ## Run lint checks
	ruff format --check
	ruff check --no-fix
	mypy

.PHONY: fmt
fmt:  ## Run formatting
	ruff format
	ruff check

.PHONY: test
test:  ## Run tests
	pytest tests/

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
	@echo The build commands support LTS_CPU=1 for building for older CPUs, and ARGS which is passed through to maturin.
	@echo 'For example to build without default features use: make build ARGS="--no-default-features".'
