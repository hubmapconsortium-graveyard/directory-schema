#!/usr/bin/env bash
set -o errexit
set -o pipefail

# NOTE: This does not run on Travis. It's just a quicker alternative to nox.

red=`tput setaf 1`
green=`tput setaf 2`
reset=`tput sgr0`
die() { set +v; echo "$red$*$reset" 1>&2 ; exit 1; }

pytest tests
black --check tests src *.py || die 'try:  black tests src *.py'
flake8 tests src *.py
mypy tests src *.py
python setup.py check --metadata --strict
