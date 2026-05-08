.PHONY: help requirements upgrade lint format test test-with-coverage docs clean
.PHONY: extract_translations


REPO_ROOT := $(shell pwd)
SRC_DIRECTORY := src
EXTRACT_DIR := conf/locale/en/LC_MESSAGES
COMBINED_LOCALE_DIR := conf/locale/en/LC_MESSAGES
# XBlock directories
XBLOCKS=$(shell find $(REPO_ROOT)/$(SRC_DIRECTORY) -mindepth 2 -maxdepth 2 -type d -name 'conf' -exec dirname {} \;)


help:  ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

requirements:  ## Sync dev dependencies
	uv sync

upgrade:  ## Upgrade python dependencies
	uv lock --upgrade

lint:  ## Run linting checks
	uv run ruff check .
	uv run ruff format --check .

format:  ## Auto-fix formatting issues
	uv run ruff check --fix .
	uv run ruff format .

test:  ## Run tests with pytest
	uv run pytest

test-with-coverage:  ## Run tests with coverage reporting
	uv run pytest --cov=$(SRC_DIRECTORY) --cov-report=xml

docs:  ## Build documentation
	$(MAKE) -C docs html

clean:  ## Clean build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .ruff_cache/
	rm -rf docs/_build/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

## Localization targets

extract_translations: ## extract strings to be translated, outputting .po files under <module_name>/conf/locale/
	@for xblock in $(XBLOCKS); do \
		module_name=$$(basename $$xblock); \
		echo "Extracting translations for $$module_name..."; \
		cd $$xblock && i18n_tool extract --no-segment; \
		if [ -f $$xblock/$(EXTRACT_DIR)/djangojs.po ]; then \
			msgcat $$xblock/$(EXTRACT_DIR)/django.po $$xblock/$(EXTRACT_DIR)/djangojs.po \
				-o $$xblock/$(EXTRACT_DIR)/django.po && rm -f $$xblock/$(EXTRACT_DIR)/djangojs.po; \
		fi; \
		mkdir -p $(REPO_ROOT)/$$module_name/$(EXTRACT_DIR); \
		if [ -f $$xblock/$(EXTRACT_DIR)/django.po ]; then \
 			mv $$xblock/$(EXTRACT_DIR)/django.po $(REPO_ROOT)/$$module_name/$(EXTRACT_DIR)/django.po; \
		fi; \
	done

selfcheck: ## check that the Makefile is well-formed
	@echo "The Makefile is well-formed."
