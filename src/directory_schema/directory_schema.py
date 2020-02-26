import os

from jsonschema import validate
from jsonschema.exceptions import ValidationError


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
        validate(as_dict, schema_dict)
    except ValidationError as e:
        raise DirectoryValidationError(e)


class DirectoryValidationError(Exception):
    def __init__(self, error):
        self.json_validation_error = error

    def __str__(self):
        return self.json_validation_error.__str__()

    def _repr__(self):
        return self.json_validation_error.__repr__()
