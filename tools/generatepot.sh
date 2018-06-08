#!/bin/bash -xe

#
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

DOCNAME=doc
DIRECTORY=doc

if [ -x "$(command -v getconf)" ]; then
    NUMBER_OF_CORES=$(getconf _NPROCESSORS_ONLN)
else
    NUMBER_OF_CORES=2
fi

# Temporary build folder for gettext
mkdir -p doc/build/gettext

# Extract messages
sphinx-build -j $NUMBER_OF_CORES -b gettext doc/source doc/build/gettext/
# Manipulates pot translation sources if needed
if [[ -f tools/doc-pot-filter.sh ]]; then
    tools/doc-pot-filter.sh
fi

# New translation target projects may not have locale folder
mkdir -p doc/source/locale

# Sphinx builds a pot file for each directory and for each file
# in the top-level directory.
# We keep the directory files and concatenate all top-level files.
has_other=0
for f in doc/build/gettext/*.pot; do
    fn=$(basename $f .pot)
    # If a pot file corresponds to a directory, we use the pot file as-is.
    if [ -d doc/source/$fn ]; then
        # Remove UUIDs, those are not necessary and change too often
        msgcat --use-first --sort-by-file $f | \
            awk '$0 !~ /^\# [a-z0-9]+$/' > doc/source/locale/doc-$fn.pot
        rm $f
    else
        has_other=1
    fi
done

# We concatenate remaining into a single pot file so that
# "git add ${DIRECTORY}/source/locale" will only add a
# single pot file for all top-level files.
if [ "$has_other" = "1" ]; then
    # Remove UUIDs, those are not necessary and change too often
    msgcat --use-first --sort-by-file doc/build/gettext/*.pot | \
        awk '$0 !~ /^\# [a-z0-9]+$/' > doc/source/locale/doc.pot
fi

rm -rf doc/build/gettext/
