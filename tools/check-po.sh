#!/bin/bash

set -e

FIND_DIRS=${*:-"."}

find $FIND_DIRS -type f \( -name '*.po' -o -name '*.pot' \) -print0 | \
while read -r -d '' FILE; do
  msgfmt --check-format -o /dev/null "$FILE"
done
