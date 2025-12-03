#!/bin/bash
# Migration script to create Weblate components and translations

# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

PROJECT=$1
BRANCH_NAME=${2:-"master"}
WORKSPACE_NAME=${3:-"workspace"}

# Replace /'s in branch names with -'s because Zanata doesn't
# allow /'s in version names.
ZANATA_VERSION=${BRANCH_NAME//\//-}

# List the components to be handled
COMPONENTS=()

SCRIPTSDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source $SCRIPTSDIR/setup_env/setup.sh

# We need a UTF-8 locale, set it properly in case it's not set.
export LANG=en_US.UTF-8

# You should set WEBLATE_URL and WEBLATE_TOKEN
# system environment variables.
echo "[INFO] Check variables"
if [ -z "$WEBLATE_URL" ] || [ "$WEBLATE_URL" == "<weblate_url>" ]; then
    echo "[ERROR] WEBLATE_URL is not set"
    exit 1
fi
if [ -z "$WEBLATE_TOKEN" ] || [ "$WEBLATE_TOKEN" == "<weblate_token>" ]; then
    echo "[ERROR] WEBLATE_TOKEN is not set"
    exit 1
fi
echo "[INFO] WEBLATE_URL and WEBLATE_TOKEN are set"

echo "[INFO] Setup environment and prepare workspace"
if ! setup_env_and_prepare_workspace "$PROJECT"; then
    echo "[ERROR] Failed to setup environment and prepare workspace"
    exit 1
fi
