#!/usr/bin/env bash
set -o errexit
set -o pipefail

# NOTE: This does not run on Travis. It's just a quicker alternative to nox.

red=`tput setaf 1`
green=`tput setaf 2`
reset=`tput sgr0`
die() { set +v; echo "$red$*$reset" 1>&2 ; exit 1; }

pytest tests
flake8 tests src *.py || die 'Try: "autopep8 --in-place --aggressive -r ."'
mypy tests src *.py --ignore-missing-imports
python setup.py check --metadata --strict
check-manifest
