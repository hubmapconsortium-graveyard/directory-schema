import argparse
import sys
import os

from jsonschema.exceptions import SchemaError
from yaml import dump as dump_yaml, safe_load as load_yaml

from directory_schema.directory_schema import validate_dir, DirectoryValidationErrors


def dir_path(string):
    if os.path.isdir(string):
        return string
    else:
        raise Exception(f'"{string}" is not a directory')


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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('dir', metavar='DIRECTORY', type=dir_path,
                        help='Directory to validate')
    parser.add_argument('schema', metavar='SCHEMA', type=argparse.FileType('r'),
                        help='Schema (JSON or YAML) to validate against')
    args = parser.parse_args()

    try:
        schema_dict = load_yaml(args.schema)
        validate_dir(args.dir, schema_dict)
        return 0
    except DirectoryValidationErrors as e:
        err = e.json_validation_errors[0]
        schema_string = '\n'.join([f'  {line}' for line in dump_yaml(err.schema).split('\n')])
        print(f'''
This directory:
{to_dir_listing(err.instance, '  ')}

fails this "{err.validator}" check:

{schema_string}
        ''')
        return 1
    except SchemaError as e:
        print(f'Provided document is not valid JSON Schema: {e.message}') # noqa B306
        return 2


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
