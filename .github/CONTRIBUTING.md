### Checking code changes

Any changes to source code must pass lint + unit tests and these are
checked automatically. 

Run this commands locally, to check your changes.

```text
make pre-commit   # check everything
```

#### Details

Pre-commit check runs unit tests and lints the source code.
To debug, you can run these steps individually.

```text
make test         # check unit tests only
```

Unit tests are in `tests` directory. You can run unit tests on specific files or the entire source.
See [pytest documentation](https://docs.pytest.org/en/stable/contents.html) for more details.


```text
make lint         # check code style only
```

This project uses [flake8](https://flake8.pycqa.org/en/latest/index.html) for linting.
You can use it to check specific files or run it against all Python source files by specifying a path.
