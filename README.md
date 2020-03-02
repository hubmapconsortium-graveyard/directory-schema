# directory_schema

Use JSON Schema to validate directory structures:
The specified directory is translated into a JSON structure like the output from `tree -J`,
and is validated against a JSON Schema, provided as a dict inside Python,
or as a JSON or YAML file through the CLI. 

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
  File "<stdin>", line 1, in <module>
  File "/Users/chuck/github/hubmap/directory-schema/src/directory_schema/directory_schema.py", line 65, in validate_dir
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
