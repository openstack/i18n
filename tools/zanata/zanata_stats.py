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
import collections
import csv
import datetime
import io
import json
import logging
import random
import re
import sys

import requests
import yaml

ZANATA_URI = 'https://translate.openstack.org/rest/%s'
LOG = logging.getLogger('zanata_stats')

ZANATA_VERSION_EXPR = r'^(master[-,a-z]*|stable-[a-z]+|openstack-user-survey)$'
ZANATA_VERSION_PATTERN = re.compile(ZANATA_VERSION_EXPR)


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
            req = requests.get(uri, headers=headers)
            return req.text
        except Exception as e:
            LOG.error('Error "%(error)s" while reading uri %(uri)s',
                      {'error': e, 'uri': uri})
            raise

    def read_json_from_uri(self, uri):
        data = self.read_uri(uri, {'Accept': 'application/json'})
        try:
            return json.loads(data)
        except Exception as e:
            LOG.error('Error "%(error)s" parsing json from uri %(uri)s',
                      {'error': e, 'uri': uri})
            raise

    def get_projects(self):
        uri = ZANATA_URI % ('projects')
        LOG.debug("Reading projects from %s" % uri)
        projects_data = self.read_json_from_uri(uri)
        return [project['id'] for project in projects_data]

    @staticmethod
    def _is_valid_version(version):
        return bool(ZANATA_VERSION_PATTERN.match(version))

    def get_user_stats(self, zanata_user_id, start_date, end_date):
        uri = ZANATA_URI % ('stats/user/%s/%s..%s'
                            % (zanata_user_id, start_date, end_date))
        return self.read_json_from_uri(uri)


class LanguageTeam(object):

    def __init__(self, language_code, team_info):
        self.language_code = language_code
        self.language = team_info['language']
        # Zanata ID which only consists of numbers is a valid ID in Zanata.
        # Such entry is interpreted as integer unless it is quoted
        # in the YAML file. Ensure to stringify them.
        self.translators = [str(i) for i in team_info['translators']]
        self.reviewers = [str(i) for i in team_info.get('reviewers', [])]
        self.coordinators = [str(i) for i in team_info.get('coordinators', [])]

    @classmethod
    def load_from_language_team_yaml(cls, translation_team_uri, lang_list):
        LOG.debug('Process list of language team from uri: %s',
                  translation_team_uri)

        content = yaml.safe_load(io.open(translation_team_uri, 'r'))

        if lang_list:
            lang_notfound = [lang_code for lang_code in lang_list
                             if lang_code not in content]
            if lang_notfound:
                LOG.error('Language %s not tound in %s.',
                          ', '.join(lang_notfound),
                          translation_team_uri)
                sys.exit(1)

        return [cls(lang_code, team_info)
                for lang_code, team_info in content.items()
                if not lang_list or lang_code in lang_list]


class User(object):

    trans_fields = ['total', 'Translated', 'NeedReview',
                    'Approved', 'Rejected']
    review_fields = ['total', 'Approved', 'Rejected']

    def __init__(self, user_id, language_code):
        self.user_id = user_id
        self.lang = language_code
        self.stats = collections.defaultdict(dict)

    def __str__(self):
        return ("<%s: user_id=%s, lang=%s, stats=%s" %
                (self.__class__.__name__,
                 self.user_id, self.lang, self.stats,))

    def __repr__(self):
        return repr(self.convert_to_serializable_data())

    def __lt__(self, other):
        if self.lang != other.lang:
            return self.lang < other.lang
        else:
            return self.user_id < other.user_id

    def read_from_zanata_stats(self, zanata_stats, project_list, version_list):
        # data format (Zanata 4.3.3)
        # [
        #     {
        #         "savedDate": "2020-09-06",
        #         "projectSlug": "i18n",
        #         "projectName": "i18n",
        #         "versionSlug": "master",
        #         "localeId": "ko-KR",
        #         "localeDisplayName": "Korean (South Korea)",
        #         "savedState": "Translated",
        #         "wordCount": 119
        #     }
        # ]
        for zanata_stat in zanata_stats:

            project_id = zanata_stat['projectSlug']
            version = zanata_stat['versionSlug']
            lang = zanata_stat['localeId']
            stat_state = zanata_stat['savedState']
            word_count = zanata_stat['wordCount']

            if project_list and project_id not in project_list:
                continue

            if version_list and version not in version_list:
                continue

            if self.lang != lang:
                continue

            my_project = self.stats[project_id]

            if version not in my_project:
                my_project[version] = {
                    'translation-stats': collections.defaultdict(int),
                    'review-stats': collections.defaultdict(int),
                }
            my_version = my_project[version]

            if stat_state in self.trans_fields:
                my_trans_stats = my_version['translation-stats']
                my_trans_stats[stat_state] += word_count
                my_trans_stats['total'] += word_count

            if stat_state in self.review_fields:
                my_review_stats = my_version['review-stats']
                my_review_stats[stat_state] += word_count
                my_review_stats['total'] += word_count

    def populate_total_stats(self):

        total_trans = dict([(k, 0) for k in self.trans_fields])
        total_review = dict([(k, 0) for k in self.review_fields])

        for project_id, versions in self.stats.items():
            for version, stats in versions.items():
                trans_stats = stats.get('translation-stats', {})
                for k in self.trans_fields:
                    total_trans[k] += trans_stats.get(k, 0)
                review_stats = stats.get('review-stats', {})
                for k in self.review_fields:
                    total_review[k] += review_stats.get(k, 0)
        self.stats['__total__']['translation-stats'] = total_trans
        self.stats['__total__']['review-stats'] = total_review

    def needs_output(self, include_no_activities):
        if include_no_activities:
            return True
        return bool(self.stats) and all(self.stats.values())

    @staticmethod
    def get_flattened_data_title():
        return [
            'user_id',
            'lang',
            'project',
            'version',
            'translation-total',
            'translated',
            'needReview',
            'approved',
            'rejected',
            'review-total',
            'review-approved',
            'review-rejected'
        ]

    def convert_to_flattened_data(self, detail=False):
        self.populate_total_stats()

        data = []

        for project_id, versions in self.stats.items():
            if project_id == '__total__':
                continue
            for version, stats in versions.items():
                trans_stats = stats.get('translation-stats', {})
                review_stats = stats.get('review-stats', {})
                if detail:
                    data.append(
                        [self.user_id, self.lang, project_id, version] +
                        [trans_stats.get(k, 0) for k in self.trans_fields] +
                        [review_stats.get(k, 0) for k in self.review_fields])

        data.append([self.user_id, self.lang, '-', '-'] +
                    [self.stats['__total__']['translation-stats'][k]
                     for k in self.trans_fields] +
                    [self.stats['__total__']['review-stats'][k]
                     for k in self.review_fields])

        return data

    def convert_to_serializable_data(self, detail):
        self.populate_total_stats()
        return {'user_id': self.user_id,
                'lang': self.lang,
                'stats': (self.stats if detail
                          else self.stats['__total__'])}


def get_zanata_stats(start_date, end_date, language_teams, project_list,
                     version_list, user_list):
    LOG.info('Getting Zanata contributors statistics (from %s to %s) ...',
             start_date, end_date)
    zanataUtil = ZanataUtility()
    users = []
    for team in language_teams:
        users += [User(user_id, team.language_code)
                  for user_id in team.translators]

    if not project_list:
        project_list = zanataUtil.get_projects()
    for user in users:
        if user_list and user.user_id not in user_list:
            continue
        LOG.info('Getting for user %(user_id)s %(user_lang)s',
                 {'user_id': user.user_id, 'user_lang': user.lang})
        data = zanataUtil.get_user_stats(
            user.user_id, start_date, end_date)
        LOG.debug('Got: %s', data)
        user.read_from_zanata_stats(data, project_list, version_list)
        LOG.debug('=> %s', user)

    return users


def write_stats_to_file(users, output_file, file_format,
                        include_no_activities, detail):
    users = sorted([user for user in users
                    if user.needs_output(include_no_activities)])
    if file_format == 'csv':
        _write_stats_to_csvfile(users, output_file, detail)
    else:
        _write_stats_to_jsonfile(users, output_file, detail)
    LOG.info('Stats has been written to %s', output_file)


def _write_stats_to_csvfile(users, output_file, detail):
    with open(output_file, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(User.get_flattened_data_title())
        for user in users:
            writer.writerows(user.convert_to_flattened_data(detail))


def _write_stats_to_jsonfile(users, output_file, detail):
    users = [user.convert_to_serializable_data(detail)
             for user in users]
    with open(output_file, 'w') as f:
        f.write(json.dumps(users, indent=4, sort_keys=True))


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
    parser.add_argument("-t", "--target-version",
                        type=_comma_separated_list,
                        help=("Specify version(s). Comma-separated list. "
                              "Otherwise all available versions are "
                              "processed."))
    parser.add_argument("-u", "--user",
                        type=_comma_separated_list,
                        help=("Specify user(s). Comma-separated list. "
                              "Otherwise all users are processed."))
    parser.add_argument('--detail',
                        action='store_true',
                        help=("If specified, statistics per project "
                              "and version are output in addition to "
                              "total statistics."))
    parser.add_argument("--include-no-activities",
                        action='store_true',
                        help=("If specified, stats for users with no "
                              "activities are output as well."
                              "By default, stats only for users with "
                              "any activities are output."))
    parser.add_argument("-f", "--format",
                        default='csv', choices=['csv', 'json'],
                        help="Output file format.")
    parser.add_argument("--debug",
                        action='store_true',
                        help="Enable debug message.")
    parser.add_argument("user_yaml",
                        help="YAML file of the user list")
    options = parser.parse_args()

    logging_level = logging.DEBUG if options.debug else logging.INFO
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    handler = logging.StreamHandler()
    handler.setLevel(logging_level)
    handler.setFormatter(formatter)
    LOG.setLevel(logging_level)
    LOG.addHandler(handler)

    language_teams = LanguageTeam.load_from_language_team_yaml(
        options.user_yaml, options.lang)

    versions = [v.replace('/', '-') for v in options.target_version or []]
    users = get_zanata_stats(options.start_date, options.end_date,
                             language_teams, options.project,
                             versions, options.user)

    output_file = (options.output_file or
                   'zanata_stats_output.%s' % options.format)

    write_stats_to_file(users, output_file, options.format,
                        options.include_no_activities,
                        options.detail)


if __name__ == '__main__':
    main()
