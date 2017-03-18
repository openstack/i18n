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
from collections import OrderedDict
import random

import bs4
import requests
import yaml

base_url = "https://translate.openstack.org/%s"


class ZanataUtility(object):
    """Utilities to collect Zanata language contributors"""
    user_agents = [
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64) Gecko/20100101 Firefox/32.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_6) AppleWebKit/537.78.2',
        'Mozilla/5.0 (Windows NT 6.3; WOW64) Gecko/20100101 Firefox/32.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X) Chrome/37.0.2062.120',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'
    ]

    def read_uri(self, uri):
        headers = {
            'User-Agent': random.choice(ZanataUtility.user_agents)
        }
        req = requests.get(url=uri, headers=headers)
        return req.text

    def iter_language_members(self, uri):
        data = self.read_uri(base_url % uri)
        soup = bs4.BeautifulSoup(data, 'html.parser')
        users = soup.find('ul', {'class': 'list--stats'}) \
            .findAll('li', {'class': 'l--pad-all-quarter'})

        for user in users:
            user_id = user.find('a').text.strip()

            roles_tag = user.find('ul', {'class': 'list--horizontal'}) \
                .find('li')
            roles = roles_tag.text.strip().split(', ')

            for role_name in roles:
                yield role_name, user_id

    def get_languages(self):
        data = self.read_uri(base_url % 'language/list')
        soup = bs4.BeautifulSoup(data, 'html.parser')
        languages = {}
        ul = soup.find('ul', {'class': 'list--stats'}).findAll('li')
        for li in ul:
            lang_tag = li.find('h3', {'class': 'list__title'}).text
            language = lang_tag.split('\n')[1].lstrip()

            span_txt = li.find('span', {'class': 'list__item__meta'}).text
            language_meta = span_txt.split(' ')[0]

            member_url = li.find('a')['href']

            span_txt = li.find('span', {'class': 'txt--understated'}).text
            total_user = span_txt.lstrip().rstrip()
            if total_user == '0':
                continue

            languages[language_meta] = {
                'language': language,
                'member_url': member_url
            }
        return languages


def save_to_yaml(data, output_file):
    with open(output_file, 'w') as out:
        out.write("# Use the order of Zanata language team info.\n")
        out.write("# Do not use the alphabetical order to make the "
                  "maitenance easier.\n")

        for (k, v) in data.items():
            yaml.safe_dump({k: v}, out, allow_unicode=True, indent=4,
                           encoding='utf-8', default_flow_style=False)


def convert_role_name(role):
    roles = {
        'Translator': 'translators',
        'Reviewer': 'reviewers',
        'Coordinator': 'coordinators'
    }
    return roles.get(role)


def collect_zanata_language_and_members():
    zanata = ZanataUtility()

    print("Retreiving language list")
    languages = zanata.get_languages()

    for language in languages.keys():
        print("Getting member list from language %s" % language)
        member_url = languages[language].pop('member_url')
        for role, user_id in zanata.iter_language_members(member_url):
            role = convert_role_name(role)
            if not role:
                print('[Warn] Unknown role : %s' % role)
                continue

            if role not in languages[language]:
                languages[language][role] = list()
            languages[language][role].append(user_id)

    sorted_key = sorted(languages, reverse=True,
                        # Need to consider a case where no tranlators in a team
                        key=lambda k: len(languages[k].get('translators', [])))
    result = OrderedDict((k, languages[k]) for k in sorted_key)
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output-file",
                        default="translation_team.yaml",
                        help=("Specify the output file. "
                              "Default: translation_team.yaml"))
    options = parser.parse_args()

    output_file = options.output_file
    data = collect_zanata_language_and_members()
    save_to_yaml(data, output_file)
    print("output is saved to filename: %s" % output_file)
