import argparse
import sys
import os

from yaml import safe_load as load_yaml

from directory_schema.directory_schema import validate_dir, DirectoryValidationError


def dir_path(string):
    if os.path.isdir(string):
        return string
    else:
        raise Exception(f'"{string}" is not a directory')


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
    except DirectoryValidationError as e:
        print(e)
        return 1


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
