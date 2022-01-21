SHELL := /bin/bash

help:
	@echo "clean - remove all build, test, coverage and Python artifacts"
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "pre-commit - run unit tests and linter"
	@echo "profile - run cProfile on all examples"
	@echo "test - run unit tests only"
	@echo "lint - check code style only"

clean: clean-build clean-pyc

clean-build:
	rm -fr output/
	rm -fr dist/
	rm -fr build/
	rm -fr profile/
	rm -fr .pytest_cache/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +
	rm -fr .coverage

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

pre-commit: dev-env lint-only test-only

test: dev-env test-only

lint: dev-env lint-only

profile: dev-env cprofile

dev-env:
	test -d venv || python3 -m venv venv;
	source venv/bin/activate;
	pip3 install -q -r requirements-dev.txt

test-only:
	@echo "running unit tests..."
	pytest --cov=./pymwp tests

test-missing:
	@echo "running unit tests..."
	pytest --cov-report term-missing --cov=./pymwp tests

lint-only:
	@echo "checking code style..."
	flake8 ./pymwp --count --show-source --statistics

cprofile:
	python3 utilities/profiler.py --lines=100