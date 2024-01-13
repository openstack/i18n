#!/usr/bin/env python3

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import csv
import io
import operator
import os
import sys

from oslo_log import log as logging
import yaml

from weblate_utils import IniConfig
from weblate_utils import WeblateRestService

LOG = logging.getLogger(__name__)


class WeblateAccounts(object):
    """Object that retrieves Weblate account information.

    Retrieve name and e-mail address using Weblate ID.

    Attributes:
    wconfig (IniConfig): weblate.ini values
    verify (Bool): True if communicating with non-SSL server
    """
    def __init__(self, wconfig, verify):
        accept = 'application/json'
        content_type = 'application/json'
        self.rest_service = WeblateRestService(wconfig, accept=accept,
                                               content_type=content_type,
                                               verify=verify)

    def get_users_data(self):
        """Get list of users

        Retrieve list of users using Weblate REST API

        """
        r = self.rest_service.query('users/')
        return r.json()


def _make_language_team(name, team_info):
    return {
        'language_code': name,
        'language': team_info['language'],
        # Retreive only translators for Weblate as we don't have
        # reviewers and coordinators in Weblate.
        'translators': [str(i) for i in team_info['translators']],
        # 'reviewers': [str(i) for i in team_info.get('reviewers', [])],
        # 'coordinators': [str(i) for i in team_info.get('coordinators', [])],
    }


def _make_user(user_name, language_code, language):
    return {
        'user_name': user_name,
        'lang_code': language_code,
        'lang': language,
        'name': '',
        'email': ''
    }


def _simplify_user_data(users):
    """Simplify user data from raw json data

    Extract "email", "full_name" and "username" from raw json data

    """
    simplified_users = {}
    for user in users:
        simplified_users[user['username']] = {
            'email': user['email'],
            'full_name': user['full_name']
        }
    return simplified_users


def read_language_team_yaml(translation_team_uri, lang_list):
    LOG.debug('Process list of language team from uri: %s',
              translation_team_uri)

    content = yaml.safe_load(io.open(translation_team_uri, 'r'))
    language_teams = {}

    if lang_list:
        lang_notfound = [lang_code for lang_code in lang_list
                         if lang_code not in content]
        if lang_notfound:
            print('Language %s not tound in %s.' %
                  (', '.join(lang_notfound),
                   translation_team_uri))
            sys.exit(1)

    for lang_code, team_info in content.items():
        if lang_list and lang_code not in lang_list:
            continue
        language_teams[lang_code] = _make_language_team(lang_code, team_info)

    return language_teams


def get_weblate_userdata(wc, verify, role, language_teams):
    print('Getting user data in Weblate...')
    accounts = WeblateAccounts(wc, verify)
    users = {}

    if not role:
        role = 'translators'

    for language_code in language_teams:
        language_team = language_teams[language_code]
        language_name = language_team['language']
        for user in language_team[role]:
            users[user] = _make_user(user, language_code, language_name)

    # Get all users
    user_list = accounts.get_users_data()

    # Simplify user data
    user_info = _simplify_user_data(user_list['results'])

    for user_name in users:
        user = users.get(user_name)
        print('Getting user detail data for user %(user_name)s'
              % {'user_name': user_name})
        user_data = user_info.get(user_name)

        if user_data:
            user['name'] = user_data['full_name']
            user['email'] = user_data['email']

    return users


def write_userdata_to_file(users, output_file):
    userdata = [user for user in
                sorted(users.values(),
                       key=operator.itemgetter('lang', 'user_name'))]
    _write_userdata_to_csvfile(userdata, output_file)
    print('Userdata has been written to %s' % output_file)


def _write_userdata_to_csvfile(userdata, output_file):
    with open(output_file, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['user_name', 'lang_code', 'lang',
                         'full_name', 'email'])
        for data in userdata:
            d = [data['user_name'], data['lang_code'],
                 data['lang'], data['name'], data['email']]
            writer.writerow(d)


def _comma_separated_list(s):
    return s.split(',')


def main():
    # Loads weblate.ini configuration file
    try:
        wc = IniConfig(os.path.expanduser('~/.config/weblate.ini'))
    except ValueError as e:
        sys.exit(e)

    # Parses command option(s)
    parser = argparse.ArgumentParser(description='Generate a csv file which '
                                     'contains the list of translators for '
                                     'a specified target role with name and '
                                     'e-mail address. Require a privilege '
                                     'to access Weblate accounts API.')
    parser.add_argument("-o", "--output-file",
                        help=("Specify the output file. "
                              "Default: weblate_userinfo_output.csv."))
    parser.add_argument("-r", "--role",
                        help=("Specify the target role. "
                              "Roles: coordinators, translators, reviewers."
                              "Default: translators."))
    parser.add_argument("-l", "--lang",
                        type=_comma_separated_list,
                        help=("Specify language(s). Comma-separated list. "
                              "Language code like zh-CN, ja needs to be used. "
                              "Otherwise all languages are processed."))
    parser.add_argument('--no-verify', action='store_false', dest='verify',
                        help='Do not perform HTTPS certificate verification')
    parser.add_argument("user_yaml",
                        help="YAML file of the user list")
    options = parser.parse_args()

    # Reads language team information
    language_teams = read_language_team_yaml(options.user_yaml, options.lang)

    users = get_weblate_userdata(wc, options.verify, options.role,
                                 language_teams)

    output_file = (options.output_file or 'weblate_userinfo_output.csv')

    write_userdata_to_file(users, output_file)


if __name__ == '__main__':
    main()
