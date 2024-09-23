# Contributing Guidelines

This guide explains how to set up a development environment, how to make various changes, including documentation and deployments.
It also explains the relevant workflows for various development tasks.


## Environment Setup

1. Create a Python virtual environment
    
    Typically, this requires:

    ```
    python3 -m venv venv
    source venv/bin/activate
    ```

    For additional details and troubleshooting, see Python documentation on [virtual environments](https://docs.python.org/3/library/venv.html).

3. Install required development dependencies

    ```
    python -m pip install -r requirements-dev.txt
    ```

---

## Source Code Changes

<h3>Debugging Changes</h3>

The source code is in `pymwp` directory. When running from source, use the command:

```
python3 -m pymwp [args]
```

<h3>Checking Changes</h3>

Any changes to source code must pass lint and unit tests. These are checked automatically for PRs
and commits to main branch. 

```text
make pre-commit   # check everything
make test         # check unit tests only
make lint         # check code style only
```

* This project uses [flake8](https://flake8.pycqa.org/en/latest/index.html) for linting.
  You can use it to check specific files, or run against all Python source files, by specifying a path.

* Unit tests are in `tests` directory. You can run unit tests on specific files or the entire source.
  See [pytest documentation](https://docs.pytest.org/en/stable/contents.html) for more details.

* There are additional interesting performance checks, e.g., benchmarking and profiling.
  These are documented in [utilities](https://statycc.github.io/pymwp/utilities/).

**Relevant workflows**

[![Build](https://github.com/statycc/pymwp/actions/workflows/build.yaml/badge.svg)](https://github.com/statycc/pymwp/actions/workflows/build.yaml) checks code changes using the latest Python runtime.

[![Version test](https://github.com/statycc/pymwp/actions/workflows/pyversion.yaml/badge.svg)](https://github.com/statycc/pymwp/actions/workflows/pyversion.yaml) checks code changes against various Python runtimes.              

---

## Documentation

Setting up the code environment and dependencies, also includes the setup for pymwp docs.
The documentation is built with [mkdocs](https://squidfunk.github.io/mkdocs-material/).

If you want to build and run the documentation website locally, run:

``` 
python -m pip install -r requirements-doc.txt
mkdocs serve
```

This will launch a web server, by default at port 8000 (`https://localhost:8000`).
Then it is possible to preview documentation changes locally in browser.

Once those changes are satisfactory, commits to main branch will automatically deploy the documentation changes.

**Relevant workflows**

[![Docs](https://github.com/statycc/pymwp/actions/workflows/docs.yaml/badge.svg)](https://github.com/statycc/pymwp/actions/workflows/docs.yaml) builds and pushes documentation to gh-pages branch.

[![pages-build-deployment](https://github.com/statycc/pymwp/actions/workflows/pages/pages-build-deployment/badge.svg)](https://github.com/statycc/pymwp/actions/workflows/pages/pages-build-deployment) deploys gh-pages branch. 

---

## Code Releases

Tagging a commit in `main` branch will automatically kick off a deployment and release,
for all configured distribution channels.

: Python Package Index

    - Builds and uploads a distribution version of the software.
    - The meta data for PyPI release is defined in `setup.py`

: GitHub Release

    - Creates a release with relevant release assets.
    - These assets are defined in the publish-workflow.
    - Release details can be edited manually and after release.

: Zenodo archival deposit

    - Following GH release event, Zenodo webhook will generate a comparable archival release.
    - Pre-set meta data for Zenodo deposit is defined in `.zenodo.json`.
    - See [deposit meta data docs](https://developers.zenodo.org/#representation) for possible options.

**Relevant workflows**

[![Publish](https://github.com/statycc/pymwp/actions/workflows/publish.yaml/badge.svg)](https://github.com/statycc/pymwp/actions/workflows/publish.yaml) handles all release and deployment tasks.
