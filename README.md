# directory_schema

Use JSON Schema to validate directory structures:
The specified directory is translated into a JSON structure like the output from `tree -J`,
and is validated against a JSON Schema, provided as a dict inside Python,
or as a JSON or YAML file through the CLI.

Sample schemas and directories are in the [test fixtures](tests/fixtures).

Instructions for contributors are [here](CONTRIBUTING.md).

## CLI

```
$ directory_schema -h
usage: directory_schema [-h] DIRECTORY SCHEMA

positional arguments:
  DIRECTORY   Directory to validate
  SCHEMA      Schema (JSON or YAML) to validate against

optional arguments:
  -h, --help  show this help message and exit
```

## Python

```
>>> from directory_schema import directory_schema
>>> directory_schema.validate_dir(
...   'tests/fixtures/just-a-placeholder',
...   {'items':
...     {'properties':
...       {'name':
...         {'pattern': 'not-placeholder'}}}}
... )
Traceback (most recent call last):
  ...
    raise DirectoryValidationErrors(errors)
directory_schema.directory_schema.DirectoryValidationErrors: This string:
    placeholder

fails this "pattern" check:

    not-placeholder
    ...
```

## Thank you
This package was created with Cookiecutter and the `cs01/cookiecutter-pypackage` project template.
- [Cookiecutter](https://github.com/audreyr/cookiecutter)
- [cs01/cookiecutter-pypackage](https://github.com/cs01/cookiecutter-pypackage)
