import os

from jsonschema import Draft7Validator
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


def _dir_to_list(path):
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
                item['contents'] = _dir_to_list(os.path.join(path, entry.name))
            items_to_return.append(item)
    return items_to_return


def validate_dir(path, schema_dict):
    '''
    Given a directory path, and a JSON schema as a dict,
    validate the directory structure against the schema.
    '''
    Draft7Validator.check_schema(schema_dict)

    validator = Draft7Validator(schema_dict)
    as_list = _dir_to_list(path)
    errors = list(validator.iter_errors(as_list))

    if errors:
        raise DirectoryValidationErrors(errors)


def validation_error_to_string(error, indent):
    schema_string = ''.join([
        f'\n{indent}{line}' for line in
        dump_yaml(error.schema[error.validator]).split('\n')
    ])

    fail_message = f'''

fails this "{error.validator}" check:
{schema_string}
    '''

    error_type = type(error.instance)

    if error_type == str:
        return f'''This string:
{indent}{error.instance}{fail_message}
        '''

    if error_type == dict:
        return f'''This item:
{to_dir_listing([error.instance], indent)}{fail_message}
        '''

    if error_type == list:
        return f'''This directory:
{to_dir_listing(error.instance, indent)}{fail_message}
        '''

    raise Exception(f'Unrecognized type "{error_type}"')


class DirectoryValidationErrors(Exception):
    def __init__(self, errors):
        self.json_validation_errors = errors

    def __str__(self):
        return '\n'.join([
            validation_error_to_string(e, '    ')
            for e in self.json_validation_errors
        ])

    def _repr__(self):
        return self.json_validation_error.__repr__()
