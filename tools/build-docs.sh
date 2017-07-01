#!/bin/bash

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

# Build English and translated version of the I18n guide.

set -e

DOCNAME=doc
DIRECTORY=doc

# build i18n contributor guide page index.html
sphinx-build -a -W -b html \
    -d ${DIRECTORY}/build/doctrees \
    ${DIRECTORY}/source ${DIRECTORY}/build/html/

if [ "${NO_LANG_BUILD:-0}" = "1" ]; then
    exit 0
fi

sphinx-build -a -W -b gettext \
    -d ${DIRECTORY}/build/doctrees.gettext \
    ${DIRECTORY}/source ${DIRECTORY}/source/locale/

# check all language translation resouce
for locale in `find ${DIRECTORY}/source/locale/ -maxdepth 1 -type d` ; do
    # skip if it is not a valid language translation resource.
    if [ ! -e ${locale}/LC_MESSAGES/${DOCNAME}.po ]; then
        continue
    fi
    language=$(basename $locale)

    echo "===== Building $language translation ====="

    # prepare all translation resources
    for pot in ${DIRECTORY}/source/locale/*.pot ; do
        # get filename
        potname=$(basename $pot)
        resname=${potname%.pot}
        echo $resname
        # merge all translation resources
        msgmerge --silent -o \
            ${DIRECTORY}/source/locale/${language}/LC_MESSAGES/${resname}.po \
            ${DIRECTORY}/source/locale/${language}/LC_MESSAGES/${DOCNAME}.po \
            ${DIRECTORY}/source/locale/${potname}
        # compile all translation resources
        msgfmt -o \
            ${DIRECTORY}/source/locale/${language}/LC_MESSAGES/${resname}.mo \
            ${DIRECTORY}/source/locale/${language}/LC_MESSAGES/${resname}.po
    done

    # build translated guide
    # build i18n contributor guide page index.html
    # TODO(amotoki): Enable -W option in translated version
    sphinx-build -a -b html -D language=${language} \
        -d ${DIRECTORY}/build/doctrees.languages/${language} \
        ${DIRECTORY}/source ${DIRECTORY}/build/html/${language}

    # remove newly created files
    git clean -f -q ${DIRECTORY}/source/locale/${language}/LC_MESSAGES/*.po
    git clean -f -x -q ${DIRECTORY}/source/locale/${language}/LC_MESSAGES/*.mo
    git clean -f -x -q ${DIRECTORY}/source/locale/.doctrees
    # revert changes to po file
    git reset -q ${DIRECTORY}/source/locale/${language}/LC_MESSAGES/${DOCNAME}.po
    git checkout -- ${DIRECTORY}/source/locale/${language}/LC_MESSAGES/${DOCNAME}.po
done

# remove newly created pot files
rm -f ${DIRECTORY}/source/locale/*.pot
