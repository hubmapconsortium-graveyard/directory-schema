#!/usr/bin/env python

from setuptools import setup, find_packages  # type: ignore

with open("README.md") as readme_file:
    readme = readme_file.read()

setup(
    author="C McCallum",
    author_email="mccallucc@gmail.com",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
    ],
    description="Use JSON Schema to validate directory structures",
    entry_points={"console_scripts": ["directory_schema=directory_schema.cli:main",],},
    install_requires=["jsonschema", "pyyaml"],
    license="MIT license",
    long_description=readme,
    long_description_content_type="text/markdown",
    package_data={"directory_schema": ["py.typed"]},
    include_package_data=True,
    keywords="directory_schema",
    name="directory_schema",
    package_dir={"": "src"},
    packages=find_packages(include=["src/directory_schema", "src/directory_schema.*"]),
    setup_requires=[],
    url="https://github.com/hubmapconsortium/directory-schema",
    version="0.0.1",
    zip_safe=False,
)
