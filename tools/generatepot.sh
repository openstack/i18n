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

# First remove the old pot file, otherwise the new file will contain
# old references

rm -f ${DIRECTORY}/source/locale/$DOCNAME.pot

# build i18n contributor guide page index.html
for i in ${DIRECTORY}/source/data/*; do echo -n > $i ; done
sphinx-build -j $NUMBER_OF_CORES -b html -b gettext ${DIRECTORY}/source \
    ${DIRECTORY}/source/locale/
git checkout -- ${DIRECTORY}/source/data/*

# Take care of deleting all temporary files so that
# "git add ${DIRECTORY}/source/locale" will only add the
# single pot file.
# Remove UUIDs, those are not necessary and change too often
msgcat --use-first --sort-by-file ${DIRECTORY}/source/locale/*.pot | \
    awk '$0 !~ /^\# [a-z0-9]+$/' > ${DIRECTORY}/source/$DOCNAME.pot
rm  ${DIRECTORY}/source/locale/*.pot
rm -rf ${DIRECTORY}/source/locale/.doctrees/
mv ${DIRECTORY}/source/$DOCNAME.pot ${DIRECTORY}/source/locale/$DOCNAME.pot
