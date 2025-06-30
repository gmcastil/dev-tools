.PHONY: install test clean

SHELL			:= /bin/bash

PRINTF			:= printf
RM			:= rm
TOUCH			:= touch
FIND			:= find
GREP			:= grep

VENV 			:= .venv
VENV_INSTALLED_STAMP	:= .venv_installed_stamp
PYTHON 			:= $(VENV)/bin/python3
PIP			:= $(VENV)/bin/pip
PYTEST			:= $(VENV)/bin/pytest

PROJ_FILES		:= $(shell git ls-files)

# Keywords to filter tests on (defaults to everything)
TESTS			?= ""
COVERAGE_ARGS		:= --cov=$(PKG_NAME) --cov-report=term-missing

$(VENV_INSTALLED_STAMP): requirements.txt
	@$(PRINTF) '%s\n' "Initializing virtual environment"
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	$(TOUCH) $(VENV_INSTALLED_STAMP)

test: $(VENV_INSTALLED_STAMP)
	@$(PYTHON) -m pytest -k $(TESTS)

debug: $(VENV_INSTALLED_STAMP)
	$(PYTHON) -m pytest -k $(TESTS) -s --pdb

coverage: $(VENV_INSTALLED_STAMP)
	@$(PYTHON) -m pytest $(COVERAGE_ARGS)

check-venv: $(VENV_INSTALLED_STAMP)
	@$(PYTHON) -m site
	@$(PRINTF) '%s\n' "Executable: $(PYTHON)"
	@$(PRINTF) '%s' "Sys.path: "
	@$(PYTHON) -c "import sys; from pprint import pprint; pprint(sys.path)"

clean-pyc:
	$(FIND) . -type f -iname '*.py[co]' -delete
	$(FIND) . -type d -iname '__pycache__' -delete
	$(RM) -rf .pytest_cache

check-ascii:
	@$(PRINTF) '%s\n' "Checking for non-ASCII characters..."
	@LC_ALL=C $(GREP) --color='always' -Pn "[^\x00-\x7F]" $(PROJ_FILES) || $(PRINTF) 'OK\n'

clean: clean-pyc
	$(RM) -rf $(VENV)
	$(RM) -f $(VENV_INSTALLED_STAMP)
	$(RM) -f .coverage

