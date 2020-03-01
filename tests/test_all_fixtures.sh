#!/usr/bin/env bash
set -o errexit
set -o pipefail

die() { set +v; echo "$*" 1>&2 ; exit 1; }

cd $(dirname $0)/fixtures

for SCHEMA in *.*; do
  SCHEMA_STEM=$(echo $SCHEMA | sed -e 's/\..*//')
  for DIR in */; do
    DIR_STEM=$(basename $DIR)
    CMD="directory_schema $DIR $SCHEMA"
    if [ $SCHEMA_STEM == $DIR_STEM ]; then
      echo "Expect '$CMD' to pass..."
      $CMD > /dev/null || die "'$CMD' failed, and it should have passed."
    else
      echo "Expect '$CMD' to fail..."
      ! $CMD > /dev/null || die "'$CMD' passed, and it should have failed."
    fi
  done
done
