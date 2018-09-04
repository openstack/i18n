#!/bin/bash

set -ex

TEAM_LIST=tools/zanata/translation_team.yaml

# This is to detect the change of the team list location.
# It is just a safe guard.
if [ ! -f $TEAM_LIST ]; then
    echo "$TEAM_LIST not found. Something wrong."
    exit 1
fi

if ! git diff --name-only HEAD^ | grep -q $TEAM_LIST; then
    echo "The recent commit does not touch $TEAM_LIST, so skipping the check."
    exit 0
fi

TMPFILE=`mktemp`
trap "rm -f $TMPFILE" EXIT

python3 tools/zanata/zanata_users.py --output-file $TMPFILE
if ! diff -u $TEAM_LIST $TMPFILE; then
    set -x
    cat <<EOF
The proposed $TEAM_LIST does not match the current Zanata team member list.
Consider reproposing it after syncing it with Zanata.
To do so, run 'tox -e zanata-users-sync'.
EOF
    set +x
    exit 1
fi
