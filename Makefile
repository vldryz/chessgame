SHELL := /bin/bash

SOURCES := chess/ tests/

lint:
	ruff format $(SOURCES) --check
	ruff check $(SOURCES)
	mypy $(SOURCES)

format:
	ruff format $(SOURCES)
	ruff check $(SOURCES) --select I,F401 --fix

fix:
	ruff check $(SOURCES) --fix

unsafe-fixes:
	ruff check $(SOURCES) --fix  --unsafe-fixes

test:
	pytest tests/
