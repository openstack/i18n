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

# This script manipulates pot files which are the target of
# translation source strings since some translation source strings
# do not need to be translated.

# This script assumes that the script locates in /tools,
# and project documentation sources are in /doc/source directory.

DIRECTORY=doc

# Exclude atc-stats/data/*.csv from POT file
TMPFILE=`mktemp -u`
msggrep -v -N "doc/source/data/*.csv" \
     ${DIRECTORY}/build/gettext/atc-stats.pot > $TMPFILE
mv -f $TMPFILE ${DIRECTORY}/build/gettext/atc-stats.pot
