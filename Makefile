# weltenfw — Developer Makefile

.PHONY: install test test-v lint clean help

PYTHON := python3
PIP    := pip

help:
	@echo "Available targets:"
	@echo "  install   — pip install -e '.[dev]'"
	@echo "  test      — pytest (quiet)"
	@echo "  test-v    — pytest (verbose)"
	@echo "  lint      — ruff check src/ tests/"
	@echo "  clean     — remove __pycache__ + .pytest_cache"

install:
	$(PIP) install -e ".[dev]"

test:
	.venv/bin/python -m pytest tests/ --tb=short -q

test-v:
	.venv/bin/python -m pytest tests/ --tb=short -v

lint:
	ruff check src/ tests/

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -name '*.pyc' -delete 2>/dev/null || true
	@echo "Cleaned."

# Fleet-Standard-Einstieg (pkg-agents-v1, platform #2075 K2): make setup && make test
setup:
	python3 -m venv .venv
	.venv/bin/pip install -U pip
	.venv/bin/pip install -e ".[dev]" || .venv/bin/pip install -e .
	.venv/bin/pip install pytest
