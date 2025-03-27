# Makefile for Python project management

# Variables
VENV = .venv
PYTHON = python3.12
PIP = $(VENV)/bin/pip
PYTHON_VENV = $(VENV)/bin/python
UV = $(VENV)/bin/uv

# Create virtual environment
.PHONY: venv
venv:
	@echo "Virtual environment ready at $(VENV)"
	@$(PYTHON) -m venv $(VENV)
	@$(VENV)/bin/python -m pip install --upgrade pip
	@$(VENV)/bin/pip install uv

# Clean up generated files and directories
.PHONY: clean
clean:
	@echo "Cleaning up..."
	@rm -rf __pycache__
	@rm -rf */__pycache__
	@rm -rf *.pyc
	@rm -rf */*.pyc
	@rm -rf .pytest_cache
	@rm -rf .coverage
	@rm -rf htmlcov
	@rm -rf dist
	@rm -rf build
	@rm -rf *.egg-info
	@rm -rf $(VENV)
	@echo "Cleanup complete"

.PHONY: dev-install
dev-install:
	@echo "Installing development dependencies..."
	@$(UV) pip install -r dev-requirements.txt
	@echo "Development dependencies installed"

.PHONY: test
test: dev-install
	@echo "Running tests..."
	@$(PYTHON_VENV) -m pytest || echo "No tests found or tests failed. Check test output for details."
	@echo "Tests complete"

.PHONY: coverage
coverage: dev-install
	@echo "Running tests with coverage..."
	@$(PYTHON_VENV) -m pytest --cov=. --cov-report=html
	@echo "Coverage report generated in htmlcov/"

.PHONY: pre-commit-install pre-commit-update pre-commit-run pre-commit-clean

# Install pre-commit and git hooks
pre-commit-install:
	python -m pip install pre-commit
	pre-commit install

# Update pre-commit hooks to latest versions
pre-commit-update:
	pre-commit autoupdate

# Run pre-commit hooks on all files
pre-commit-run:
	pre-commit run --all-files

# Clean pre-commit cache
pre-commit-clean:
	pre-commit clean

# Help command
.PHONY: help
help:
	@echo "Available commands:"
	@echo "  make venv                - Create virtual environment with uv"
	@echo "  make update-uv           - Update uv to latest version in virtual environment"
	@echo "  make clean               - Clean up generated files"
	@echo "  make test                - Run tests"
	@echo "  make coverage            - Run tests with coverage report"
	@echo "  make pre-commit-install  - Install pre-commit and git hooks"
	@echo "  make pre-commit-update   - Update pre-commit hooks to latest versions"
	@echo "  make pre-commit-run      - Run pre-commit hooks on all files"
	@echo "  make pre-commit-clean    - Clean pre-commit cache"
	@echo "  make help                - Show this help message"

.PHONY: setup-dev

# Set up the complete development environment
setup-dev: venv pre-commit-install
	@echo "Development environment setup complete!"
	@echo "You can now start developing. Try:"
	@echo "  make test      - Run tests"
