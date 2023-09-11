#!/bin/bash

set -xe

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

# Exclude atc-stats/data/*.csv from POT file
TARGET=doc/build/gettext/atc-stats.pot
msgfmt --statistics -o /dev/null ${TARGET}
TMPFILE=`mktemp -u`
msggrep -v -N "../../source/data/*.csv" ${TARGET} > $TMPFILE
mv -f $TMPFILE ${TARGET}
msgfmt --statistics -o /dev/null ${TARGET}
