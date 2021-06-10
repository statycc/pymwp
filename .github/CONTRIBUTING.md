### Checking code changes

Any changes to source code must pass lint + unit tests and these are
checked automatically. Here are some helpful commands for checking your changes:

In the project root, run:

```text
make pre-commit   # check everything
```

```text
make test         # check unit tests only (1
```

```text
make lint         # check code style only (2
```

```text
make clean        # clean generated files
```


1) Unit tests are in `tests` directory. You can run unit tests on specific files or the entire source. 
See [pytest documentation](https://docs.pytest.org/en/stable/contents.html) for more details.

2) This project uses [flake8](https://flake8.pycqa.org/en/latest/index.html) for linting.
You can use it to check specific files or run it against all Python source files by specifying a path.
