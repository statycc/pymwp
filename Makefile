SHELL := /bin/bash

help:
	@echo "clean - remove all build, test, coverage and Python artifacts"
	@echo "pre-commit - run unit tests and linter"
	@echo "profile - run cProfile on all examples"
	@echo "test - run unit tests only"
	@echo "lint - check code style only"

clean:
	@rm -fr output/
	@rm -fr dist/
	@rm -fr build/
	@rm -fr pages/
	@rm -fr profile/
	@rm -fr .pytest_cache/
	@rm -fr .eggs/
	@rm -fr .coverage
	@find . -name '*.egg-info' -exec rm -fr {} +
	@find . -name '*.egg' -exec rm -f {} +
	@find . -name '*.pyc' -exec rm -f {} +
	@find . -name '*.pyo' -exec rm -f {} +
	@find . -name '*~' -exec rm -f {} +
	@find . -name '__pycache__' -exec rm -fr {} +

C_FILES = basics implementation_paper infinite not_infinite original_paper other tool_paper

pre-commit: dev-env lint-only test-only

test: dev-env test-only

lint: dev-env lint-only

profile: dev-env cprofile

bench: dev-env bench-only plot

dev-env:
	@test -d venv || python3 -m venv venv;
	@source venv/bin/activate;
	@pip3 install -q -r requirements-test.txt

test-only:
	pytest --cov=./pymwp tests

test-missing:
	pytest --cov-report term-missing --cov=./pymwp tests

lint-only:
	flake8 ./pymwp --count --show-source --statistics

cprofile:
	python3 utilities/profiler.py --lines=100 --no-external --out profile

bench-only:
	@$(foreach cat, $(C_FILES), $(foreach f, $(shell find c_files/$(cat) -type f -iname '*.c'), \
 		python3 -m pymwp $(f) --fin --silent && echo "DONE -- $(f)" ; )) \
 		python3 utilities/runtime.py output

plot:
	python3 utilities/plot.py -r output -f tex

compute-ast:
	rm -rf test/mocks/*.txt
	python3 utilities/ast_util.py tests/test_examples tests/mocks
