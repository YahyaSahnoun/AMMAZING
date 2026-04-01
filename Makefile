# ── A-Maze-ing Makefile ─────────────────────────────────────────────────────
#
# Usage:
#   make install      Install dependencies
#   make run          Run the program with the default config
#   make debug        Run under pdb debugger
#   make clean        Remove caches and build artefacts
#   make lint         Run flake8 + mypy
#   make lint-strict  Run flake8 + mypy --strict
#   make build        Build the mazegen pip package (.whl + .tar.gz)
#   make test         Run the test suite
#
PYTHON     := python3
PIP        := pip3
CONFIG     := config.txt
MAIN       := a_maze_ing.py
PKG_DIR    := mazegen

.PHONY: install run debug clean lint lint-strict build test help

# Install
install:
	$(PIP) install flake8 mypy build --quiet

# Run
run:
	$(PYTHON) $(MAIN) $(CONFIG)

# Debug
debug:
	$(PYTHON) -m pdb $(MAIN) $(CONFIG)

# Clean
clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .mypy_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name dist       -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name build      -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc"            -delete 2>/dev/null || true
	@echo "Clean done."

# Lint (mandatory flags)
lint:
	$(Python) -m flake8 .
	$(PYTHON) -m mypy . \
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs

# Lint strict (optional, recommended)
lint-strict:
	$(Python) -m flake8 .
	$(PYTHON) -m mypy . --strict

# Build pip package
build:
	$(PYTHON) -m build --outdir dist/ .
	@echo ""
	@echo "Package built:"
	@ls -1 dist/


# Help
help:
	@echo ""
	@echo "A-Maze-ing — available targets:"
	@echo "  install      Install dev dependencies (flake8, mypy, build)"
	@echo "  run          Run the program with config.txt"
	@echo "  debug        Run under Python debugger (pdb)"
	@echo "  clean        Remove __pycache__, .mypy_cache, dist/, etc."
	@echo "  lint         Run flake8 + mypy with mandatory flags"
	@echo "  lint-strict  Run flake8 + mypy --strict"
	@echo "  build        Build the mazegen pip package"
	@echo "  test         Run the pytest test suite"
	@echo ""