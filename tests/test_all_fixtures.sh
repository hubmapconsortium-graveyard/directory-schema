#!/usr/bin/env bash
set -o errexit
set -o pipefail

red=`tput setaf 1`
green=`tput setaf 2`
cyan=`tput setaf 6`
reset=`tput sgr0`
die() { set +v; echo "$red$*$reset" 1>&2 ; exit 1; }

cd $(dirname $0)/fixtures

for SCHEMA in *.*; do
  SCHEMA_STEM=$(echo $SCHEMA | sed -e 's/\..*//')
  for DIR in */; do
    DIR_STEM=$(basename $DIR)
    CMD="directory_schema $DIR $SCHEMA"
    if [ $SCHEMA_STEM == $DIR_STEM ]; then
      echo "${cyan}Expect '$CMD' to ${green}pass...${reset}"
      $CMD > /dev/null || die "'$CMD' failed, and it should have passed."
    else
      echo "${cyan}Expect '$CMD' to ${red}fail...${reset}"
      ! $CMD > /dev/null || die "'$CMD' passed, and it should have failed."
      # TODO: This does not distinguish between the failures we want,
      # and python errors with tracebacks.
    fi
  done
done
