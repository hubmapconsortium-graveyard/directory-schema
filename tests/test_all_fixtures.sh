#!/usr/bin/env bash
set -o errexit
set -o pipefail

cd fixtures

for SCHEMA in *.*; do
  for DIR in */; do
    echo "Test $SCHEMA on $DIR"
  done
done
