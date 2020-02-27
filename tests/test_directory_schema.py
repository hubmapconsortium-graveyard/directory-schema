import os

import pytest

from directory_schema import directory_schema


def test_directory_schema():
    assert directory_schema is not None


def test_dir_to_dict():
    fixture_path = os.path.join(os.path.dirname(__file__), "fixtures", "has-readme")
    assert directory_schema.dir_to_dict(fixture_path) == [
        {"type": "file", "name": ".dot-files-should-be-listed"},
        {"type": "file", "name": "README.md"},
        {
            "type": "directory",
            "name": "src",
            "contents": [{"type": "file", "name": "fake.py"}],
        },
    ]


def test_validate_dir():
    fixture_path = os.path.join(os.path.dirname(__file__), "fixtures", "has-readme")

    arr_schema = {'type': 'array'}
    directory_schema.validate_dir(fixture_path, arr_schema)

    obj_schema = {'type': 'object'}
    with pytest.raises(directory_schema.DirectoryValidationError):
        directory_schema.validate_dir(fixture_path, obj_schema)
