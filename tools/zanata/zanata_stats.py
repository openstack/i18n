#!/usr/bin/python

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
import datetime
import io
import json
import operator
import random
import re
import sys

from oslo_log import log as logging
import six
import yaml

ZANATA_URI = 'https://translate.openstack.org/rest/%s'
LOG = logging.getLogger(__name__)

ZANATA_VERSION_PATTERN = re.compile(r'^(master[-,a-z]*|stable-[a-z]+)$')


class ZanataUtility(object):
    """Utilities to invoke Zanata REST API."""
    user_agents = [
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64) Gecko/20100101 Firefox/32.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_6) AppleWebKit/537.78.2',
        'Mozilla/5.0 (Windows NT 6.3; WOW64) Gecko/20100101 Firefox/32.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X) Chrome/37.0.2062.120',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'
    ]

    def read_uri(self, uri, headers):
        try:
            headers['User-Agent'] = random.choice(ZanataUtility.user_agents)
            req = six.moves.urllib.request.Request(url=uri, headers=headers)
            fd = six.moves.urllib.request.urlopen(req)
            raw = fd.read()
            fd.close()
            return raw
        except Exception as e:
            print('exception happen', e)
            LOG.warn('Error "%(error)s" while reading uri %(uri)s',
                     {'error': e, 'uri': uri})

    def read_json_from_uri(self, uri):
        try:
            data = self.read_uri(uri, {'Accept': 'application/json'})
            return json.loads(data)
        except Exception as e:
            LOG.warn('Error "%(error)s" parsing json from uri %(uri)s',
                     {'error': e, 'uri': uri})

    def zanata_get_projects(self):
        uri = ZANATA_URI % ('projects')
        LOG.debug("Reading projects from %s" % uri)
        projects_data = self.read_json_from_uri(uri)
        for project in projects_data:
            yield project['id']

    def _is_valid_version(self, version):
        return bool(ZANATA_VERSION_PATTERN.match(version))

    def zanata_get_project_versions(self, project_id):
        uri = ZANATA_URI % ('projects/p/%s' % project_id)
        LOG.debug("Reading iterations for project %s" % project_id)
        project_data = self.read_json_from_uri(uri)
        if ('iterations' in project_data):
            for interation_data in project_data['iterations']:
                if self._is_valid_version(interation_data['id']):
                    yield interation_data['id']
        else:
            yield None

    def zanata_get_user_stats(self, project_id, iteration_id, zanata_user_id,
                              start_date, end_date):
        uri = ZANATA_URI % ('stats/project/%s/version/%s/contributor/%s/%s..%s'
                            % (project_id, iteration_id, zanata_user_id,
                               start_date, end_date))
        return self.read_json_from_uri(uri)


def _make_language_team(name, team_info):
    return {
        'tag': 'language_team',
        'language_code': name,
        'language': team_info['language'],
        # Zanata ID which only consists of numbers is a valid ID
        # and such entry is interpreted as integer unless it is
        # quoted in the YAML file. Ensure to stringify them.
        'translators': [str(i) for i in team_info['translators']],
        'reviewers': [str(i) for i in team_info.get('reviewers', [])],
        'coordinators': [str(i) for i in team_info.get('coordinators', [])],
    }


def _make_user(user_id, language_code):
    return {
        'user_id': user_id,
        'lang': language_code,
        'translated': 0,
        'approved': 0,
        'rejected': 0
    }


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


def get_zanata_stats(start_date, end_date, language_teams, project_list):
    print('Getting Zanata contributors statistics (from %s to %s) ...' %
          (start_date, end_date))
    zanataUtil = ZanataUtility()
    users = {}
    for language_code in language_teams:
        language_team = language_teams[language_code]
        for user in language_team['translators']:
            users[user] = _make_user(user, language_code)

    if not project_list:
        project_list = zanataUtil.zanata_get_projects()
    for project_id in project_list:
        for version in zanataUtil.zanata_get_project_versions(project_id):
            for user_id in users:
                user = users.get(user_id)
                print('Getting %(project_id)s %(version)s '
                      'for user %(user_id)s %(user_lang)s'
                      % {'project_id': project_id,
                         'version': version,
                         'user_id': user_id,
                         'user_lang': user['lang']})
                statisticdata = zanataUtil.zanata_get_user_stats(
                    project_id, version, user_id, start_date, end_date)
                if statisticdata:
                    user_contributes = statisticdata[user_id]
                    if (user['lang'] in user_contributes):
                        user_stat = user_contributes[user['lang']]
                        user['translated'] += int(user_stat['translated'])
                        user['approved'] += int(user_stat['approved'])
                        user['rejected'] += int(user_stat['rejected'])

    return users


def write_stats_to_file(users, output_file, file_format,
                        include_no_activities):
    stats = [user for user in
             sorted(users.values(), key=operator.itemgetter('lang', 'user_id'))
             if _needs_output(include_no_activities, user)]
    if file_format == 'csv':
        _write_stats_to_csvfile(stats, output_file)
    else:
        _write_stats_to_jsonfile(stats, output_file)
    print('Stats has been written to %s' % output_file)


def _needs_output(include_no_activities, user):
    if include_no_activities:
        return True
    elif user['translated'] or user['approved'] or user['rejected']:
        return True
    else:
        return False


def _write_stats_to_csvfile(stats, output_file):
    with open(output_file, 'wb') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['user_id', 'lang',
                         'translated', 'approved', 'rejected'])
        for stat in stats:
            writer.writerow([stat['user_id'], stat['lang'],
                             stat['translated'], stat['approved'],
                             stat['rejected']])


def _write_stats_to_jsonfile(stats, output_file):
    with open(output_file, 'w') as f:
        f.write(json.dumps(stats, indent=4))


def _comma_separated_list(s):
    return s.split(',')


def main():

    default_end_date = datetime.datetime.now()
    default_start_date = default_end_date - datetime.timedelta(days=180)
    default_start_date = default_start_date.strftime('%Y-%m-%d')
    default_end_date = default_end_date.strftime('%Y-%m-%d')

    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--start-date",
                        default=default_start_date,
                        help=("Specify the start date. "
                              "Default:%s" % default_start_date))
    parser.add_argument("-e", "--end-date",
                        default=default_end_date,
                        help=("Specify the end date. "
                              "Default:%s" % default_end_date))
    parser.add_argument("-o", "--output-file",
                        help=("Specify the output file. "
                              "Default: zanata_stats_output.{csv,json}."))
    parser.add_argument("-p", "--project",
                        type=_comma_separated_list,
                        help=("Specify project(s). Comma-separated list. "
                              "Otherwise all Zanata projects are processed."))
    parser.add_argument("-l", "--lang",
                        type=_comma_separated_list,
                        help=("Specify language(s). Comma-separated list. "
                              "Language code like zh-CN, ja needs to be used. "
                              "Otherwise all languages are processed."))
    parser.add_argument("--include-no-activities",
                        action='store_true',
                        help=("If specified, stats for users with no "
                              "activities are output as well."
                              "By default, stats only for users with "
                              "any activities are output."))
    parser.add_argument("-f", "--format",
                        default='csv', choices=['csv', 'json'],
                        help="Output file format.")
    parser.add_argument("user_yaml",
                        help="YAML file of the user list")
    options = parser.parse_args()

    language_teams = read_language_team_yaml(options.user_yaml, options.lang)

    users = get_zanata_stats(options.start_date, options.end_date,
                             language_teams, options.project)

    output_file = (options.output_file or
                   'zanata_stats_output.%s' % options.format)

    write_stats_to_file(users, output_file, options.format,
                        options.include_no_activities)


if __name__ == '__main__':
    main()
