SHELL := /bin/bash

SOURCES ?= chess/

lint:
	ruff format $(SOURCES) --check
	ruff check $(SOURCES)
	mypy $(SOURCES)

format:
	ruff format $(SOURCES)
	ruff check $(SOURCES) --select I,F401 --fix

fix:
	ruff check $(SOURCES) --fix

unsafe_fixes:
	ruff check $(SOURCES) --fix  --unsafe-fixes

tests:
	pytest tests/
