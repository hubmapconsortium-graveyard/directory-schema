import os

from jsonschema import Draft7Validator, validate, ValidationError
from yaml import dump as dump_yaml


def to_dir_listing(dir_as_list, indent=''):
    next_indent = indent + '    '
    return ''.join([
        '\n' + indent + item['name']
        + to_dir_listing(
            item['contents'] if 'contents' in item else [],
            next_indent
        )
        for item in dir_as_list
    ])


def dir_to_dict(path):
    '''
    Walk the directory at `path`, and return a dict like that from `tree -J`:

    [
      {
        "type": "directory",
        "name": "some-directory",
        "contents": [
          { "type": "file", "name": "some-file.txt" }
        ]
      }
    ]
    '''

    items_to_return = []
    with os.scandir(path) as scan:
        for entry in sorted(scan, key=lambda entry: entry.name):
            is_dir = entry.is_dir()
            item = {
                'type': 'directory' if is_dir else 'file',
                'name': entry.name
            }
            if is_dir:
                item['contents'] = dir_to_dict(os.path.join(path, entry.name))
            items_to_return.append(item)
    return items_to_return


def validate_dir(path, schema_dict):
    '''
    Given a directory path, and a JSON schema as a dict,
    validate the directory structure against the schema.
    '''
    as_dict = dir_to_dict(path)
    try:
        validate(as_dict, schema_dict, cls=Draft7Validator)
    except ValidationError:
        # validate() can throw SchemaError;
        # ValidationError will be handled in the next phase.
        pass

    validator = Draft7Validator(schema_dict)
    errors = list(validator.iter_errors(as_dict))

    if errors:
        raise DirectoryValidationErrors(errors)

def validation_error_to_string(error):
    schema_string = ''.join([f'\n  {line}' for line in dump_yaml(error.schema).split('\n')])
    return f'''
This directory:
{to_dir_listing(error.instance, '  ')}

fails this "{error.validator}" check:
{schema_string}
    '''


class DirectoryValidationErrors(Exception):
    def __init__(self, errors):
        self.json_validation_errors = errors

    def __str__(self):
        return '\n'.join([
            validation_error_to_string(e)
            for e in self.json_validation_errors
        ])

    def _repr__(self):
        return self.json_validation_error.__repr__()
