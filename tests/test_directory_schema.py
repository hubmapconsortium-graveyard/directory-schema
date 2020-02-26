import os

from directory_schema import directory_schema


def test_directory_schema():
    assert directory_schema is not None


def test_dir_to_dict():
    fixture_path = os.path.join(os.path.dirname(__file__), "fixtures", "fake-directory")
    assert directory_schema.dir_to_dict(fixture_path) == [
        {"type": "file", "name": ".dot-files-should-be-listed"},
        {"type": "file", "name": "README.md"},
        {
            "type": "directory",
            "name": "src",
            "contents": [{"type": "file", "name": "fake.py"}],
        },
    ]
