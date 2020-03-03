On Travis, tests are run by [`nox`](https://nox.thea.codes/en/stable/),
but in development that can be slow, because each run creates an new virtual environment.

As a shortcut, `test.sh` can run all the tests locally,
but you will need to pip install the dependencies in `setup.py` by hand.

When you do want to run nox, first install:
```
python -m pip install --user nox
```

run unit tests:
```
nox -s tests
```

lint:
```
nox -s lint
```

and publish to PyPI:
```
nox -s publish
```

and afterwards update the [CHANGELOG](CHANGELOG.md) with a new `in progress` version.
