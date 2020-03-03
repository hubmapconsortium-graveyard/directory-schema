import os

import pytest
from jsonschema.exceptions import SchemaError

from directory_schema import directory_schema


def test_directory_schema():
    assert directory_schema is not None


def test_dir_to_list():
    fixture_path = os.path.join(os.path.dirname(__file__), 'fixtures', 'index-in-every-directory')
    assert directory_schema._dir_to_list(fixture_path) == [
        {'type': 'file', 'name': 'index.html'},
        {'type': 'directory', 'name': 'sub', 'contents': [
            {'type': 'file', 'name': 'index.html'}
        ]},
    ]


def test_validate_dir():
    fixture_path = os.path.join(os.path.dirname(__file__), 'fixtures', 'has-readme-and-license')

    arr_schema = {'type': 'array'}
    directory_schema.validate_dir(fixture_path, arr_schema)

    obj_schema = {'type': 'object'}
    with pytest.raises(directory_schema.DirectoryValidationErrors):
        directory_schema.validate_dir(fixture_path, obj_schema)

    not_a_schema = {'type': 'invalid'}
    with pytest.raises(SchemaError):
        directory_schema.validate_dir(fixture_path, not_a_schema)
