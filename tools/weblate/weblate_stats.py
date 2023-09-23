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
from datetime import timedelta
import io
import json
import logging
import os
import re
import sys
from typing import Optional
from weblate_records import WeblateComponentInfo
from weblate_records import WeblateObjectStats
from weblate_records import WeblateProjectStats
from weblate_records import WeblateUserInfo
from weblate_records import WeblateUserStats
from weblate_utils import IniConfig
from weblate_utils import WeblateRestService
import yaml

WEBLATE_HOST = "https://openstack.weblate.cloud"
WEBLATE_URI = WEBLATE_HOST + "/%s"
LOG = logging.getLogger("weblate_stats")

WEBLATE_VER_EXPR = r"^(master[-,a-z]*|stable-[a-z]+|openstack-user-survey)$"
WEBLATE_VER_PATTERN = re.compile(WEBLATE_VER_EXPR)


DEFAULT_STATS = {
    "translated": 0,
    "approved": 0,
    "needReview": 0,
    "fuzzy": 0,
    "failingCheck": 0,
    "pending": 0,
}


class WeblateUtility(object):
    """Utilities to invoke Weblate REST API.

    https://docs.weblate.org/en/weblate-4.18.2/api.html#projects
    https://docs.weblate.org/en/weblate-4.18.2/api.html#get--api-users-(str-username)-statistics-
    """

    user_agents = [
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64) Gecko/20100101 Firefox/32.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_6) AppleWebKit/537.78.2",
        "Mozilla/5.0 (Windows NT 6.3; WOW64) Gecko/20100101 Firefox/32.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X) Chrome/37.0.2062.120",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
    ]

    def __init__(
        self,
        wconfig,
        verify: bool = True,
    ):
        self.weblateRestService = WeblateRestService(wconfig, verify)

    def _unify(self, locale: str) -> str:
        return locale.replace("-", "").replace("_", "").lower()

    # API REQUEST

    def read_uri(self, uri):
        try:
            req = self.weblateRestService.query(uri)
            return req.text
        except Exception as e:
            LOG.error('Error "%s" while reading uri %s', e, uri)
            raise

    def read_json_from_uri(self, uri):
        data = self.read_uri(uri)
        try:
            return json.loads(data)
        except Exception as e:
            LOG.error(
                'Error "%(error)s" parsing json from uri %(uri)s',
                {"error": e, "uri": uri},
            )
            raise

    def get_projects(self, **kargs) -> list:
        uri = WEBLATE_URI % ("api/projects/")

        if "url" in kargs:
            uri = kargs.get("url")

        LOG.debug("Reading projects from %s" % uri)
        projects_data = self.read_json_from_uri(uri)

        return projects_data["results"]

    def get_project_statistics(self, project_slug: str, **kargs):
        uri = WEBLATE_URI % ("api/projects/%s/statistics/" % (project_slug))

        if "url" in kargs:
            uri = kargs.get("url")

        LOG.debug("Reading project statistics from %s" % uri)
        project_statistics_data = self.read_json_from_uri(uri)
        return WeblateProjectStats.from_dict(project_statistics_data)

    def get_object_statistics(self, obj: str, **kargs):
        uri = WEBLATE_URI % ("api/%s/statistics/" % (obj))

        if "url" in kargs:
            uri = kargs.get("url")

        LOG.debug("Reading object statistics from %s" % uri)
        object_data = self.read_json_from_uri(uri)
        return WeblateObjectStats.from_dict(object_data)

    def get_users(self, **kargs) -> list:
        uri = WEBLATE_URI % ("api/users/")

        if "url" in kargs:
            uri = kargs.get("url")

        LOG.debug("Reading users from %s" % uri)
        users_data = self.read_json_from_uri(uri)
        return users_data["results"]

    def get_user(self, username: str, **kargs):
        uri = WEBLATE_URI % ("api/users/%s/" % (username))

        if "url" in kargs:
            uri = kargs.get("url")

        LOG.debug("Reading user from %s" % uri)
        user_data = self.read_json_from_uri(uri)
        return user_data

    def get_user_statistics(self, username: str, **kargs):
        uri = WEBLATE_URI % ("api/users/%s/statistics/" % (username))

        if "url" in kargs:
            uri = kargs.get("url")

        LOG.debug("Reading user statistics from %s" % uri)
        user_data = self.read_json_from_uri(uri)
        return WeblateUserStats.from_dict(user_data)

    def get_group(self, group_id: int, **kargs):
        uri = WEBLATE_URI % ("api/groups/%s/" % (group_id))

        if "url" in kargs:
            uri = kargs.get("url")

        LOG.debug("Reading group from %s" % uri)
        group_data = self.read_json_from_uri(uri)
        return WeblateUserInfo.from_dict(group_data)

    def get_component(
        self, project: str, component: str, **kargs
    ) -> WeblateComponentInfo:
        uri = WEBLATE_URI % ("api/components/%s/%s/" % (project, component))

        if "url" in kargs:
            uri = kargs.get("url")

        LOG.debug("Reading component from %s" % uri)
        component_data = self.read_json_from_uri(uri)
        return WeblateComponentInfo.from_dict(component_data)

    def get_translation_changes(
        self, project: str, component: str, lang: str, **kargs
    ) -> list:
        uri: str = WEBLATE_URI % (
            "api/translations/%s/%s/%s/changes/" % (project, component, lang)
        )

        if "url" in kargs:
            uri = kargs.get("url")

        if "checksum" in kargs:
            uri += "?checksum=%s" % (kargs.get("checksum"))

        LOG.debug("Reading translation changes from %s" % uri)
        translation_data = self.read_json_from_uri(uri)
        return translation_data

    def get_translations(
        self, project: str, component: str, language: str, **kargs
    ) -> Optional[dict]:
        uri: str = WEBLATE_URI % (
            "api/translations/%s/%s/%s/" % (project, component, language)
        )

        checksum: str = ""
        if "?checksum" in kargs.get("checksum"):
            checksum = kargs.get("checksum").split("?checksum=")[1]

        if "url" in kargs:
            uri = kargs.get("url")

        if "checksum" in kargs:
            uri += "?checksum=%s" % (checksum)

        LOG.debug("Reading translation from %s" % uri)
        translation_data = self.read_json_from_uri(uri)

        langs = set()
        langs.add(self._unify(translation_data["language"]["code"]))
        langs.add(self._unify(translation_data["language"]["name"]))
        langs.add(self._unify(translation_data["language_code"]))
        for lang in translation_data["language"]["aliases"]:
            langs.add(self._unify(lang))

        user_lang = self._unify(kargs.get("user_lang"))
        if "user_lang" in kargs and user_lang not in langs:
            return None

        return translation_data

    def get_change(self, id: int, **kargs) -> dict:
        uri = WEBLATE_URI % ("api/changes/%d/" % (id))

        if "url" in kargs:
            uri = kargs.get("url")

        LOG.debug("Reading change from %s" % uri)
        change_data = self.read_json_from_uri(uri)
        return change_data

    def get_units(self, start_datetime: str, end_datetime: str, **kargs):
        change_date_query = "?q=changed:>=%s AND changed:<=%s " % (
            start_datetime,
            end_datetime,
        )
        uri = WEBLATE_URI % ("api/units/%s" % (change_date_query))

        if "url" in kargs:
            uri = kargs.get("url")

        LOG.debug("Reading units from %s" % uri)
        units_data = self.read_json_from_uri(uri)
        return units_data["results"]


class LanguageTeam(object):
    def __init__(self, language_code, team_info):
        self.language_code = language_code
        self.language = team_info["language"]
        # Weblate ID which only consists of numbers is a valid ID in Weblate
        # Such entry is interpreted as integer unless it is quoted
        # in the YAML file. Exnsure to stringify them.
        self.translators = [str(i) for i in team_info["translators"]]
        self.reviewers = [str(i) for i in team_info.get("reviewers", [])]
        self.coordinators = [str(i) for i in team_info.get("coordinators", [])]

    @classmethod
    def load_from_language_team_yaml(cls, trans_team_uri, lang_list):
        LOG.debug("Process list of language team from uri: %s", trans_team_uri)

        content = yaml.safe_load(io.open(trans_team_uri, "r"))

        if lang_list:
            lang_notfound = [
                lang_code for lang_code in lang_list
                if lang_code not in content
            ]

            if lang_notfound:
                LOG.error(
                    "Language %s not tound in %s.",
                    ", ".join(lang_notfound),
                    trans_team_uri,
                )
                sys.exit(1)

        return [
            cls(lang_code, team_info)
            for lang_code, team_info in content.items()
            if not lang_list or lang_code in lang_list
        ]


class User(object):
    trans_fields = [
        "translated",
        "approved",
        "needReview",
        "fuzzy",
        "failingCheck",
        "pending",
    ]
    review_fields = ["total", "approved"]  # Todo

    def __init__(self, user_id, language_code):
        self.user_id = user_id
        self.lang = language_code
        self.stats = collections.defaultdict(dict)

    def __str__(self):
        return "<%s: user_id=%s, lang=%s, stats=%s" % (
            self.__class__.__name__,
            self.user_id,
            self.lang,
            self.stats,
        )

    # def __repr__(self):
    #     return repr(self.convert_to_serializable_data())

    def __lt__(self, other):
        if self.lang != other.lang:
            return self.lang < other.lang
        else:
            return self.user_id < other.user_id

    def needs_output(self, include_no_activities):
        if include_no_activities:
            return True
        return bool(self.stats) and all(self.stats.values())

    @staticmethod
    def get_flattened_data_title():
        return [
            "user_id",
            "main_lang",
            "translated",
            "needReview",
            "approved",
            "fuzzy",
            "failingCheck",
            "pending",
        ]

    def convert_to_flattened_data(self, detail=False):
        data = []
        for stat, count in self.stats.items():
            if detail:
                data.append(
                    [self.user_id, self.lang]
                    + [count for k in self.trans_fields]
                )

        stat_sum: int = sum([self.stats[k] for k in self.trans_fields])
        if stat_sum > 0:
            data.append(
                [self.user_id, self.lang]
                + [self.stats[k] for k in self.trans_fields]
            )

        return data


def write_stats_to_file(users, output_file, include_no_activities, detail):
    before_sort = []
    for user in users:
        if not user.stats.keys():
            user.stats = DEFAULT_STATS

        if user.needs_output(include_no_activities):
            before_sort.append(user)

    users = sorted(before_sort)

    _write_stats_to_csvfile(users, output_file, detail)

    LOG.info("Stats has been written to %s", output_file)


def _write_stats_to_csvfile(users, output_file, detail):
    with open(output_file, "w") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(User.get_flattened_data_title())
        for user in users:
            writer.writerows(user.convert_to_flattened_data(detail))


def _comma_separated_list(s):
    return s.split(",")


def main():
    # Loads weblate.ini configuration file
    try:
        wc = IniConfig(os.path.expanduser("~/.config/weblate.ini"))
    except ValueError as e:
        sys.exit(e)

    default_end_date = datetime.datetime.now()
    default_start_date = default_end_date - timedelta(days=180)
    default_start_date = default_start_date.strftime("%Y-%m-%d")
    default_end_date = default_end_date.strftime("%Y-%m-%d")

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s",
        "--start-date",
        default=default_start_date,
        help=("Specify the start date. " "Default:%s" % default_start_date),
    )
    parser.add_argument(
        "-e",
        "--end-date",
        default=default_end_date,
        help=("Specify the end date. " "Default:%s" % default_end_date),
    )
    parser.add_argument(
        "-o",
        "--output-file",
        help=(
            "Specify the output file. "
            "Default: weblate_stats_output.csv."
        ),
    )
    parser.add_argument(
        "-p",
        "--project",
        type=_comma_separated_list,
        help=(
            "Specify project(s). Comma-separated list. "
            "Otherwise all Weblate projects are processed."
        ),
    )
    parser.add_argument(
        "-l",
        "--lang",
        type=_comma_separated_list,
        help=(
            "Specify language(s). Comma-separated list. "
            "Language code like zh-CN, ja needs to be used. "
            "Otherwise all languages are processed."
        ),
    )
    parser.add_argument(
        "-t",
        "--target-version",
        type=_comma_separated_list,
        help=(
            "Specify version(s). Comma-separated list. "
            "Otherwise all available versions are "
            "processed."
        ),
    )
    parser.add_argument(
        "-u",
        "--user",
        type=_comma_separated_list,
        help=(
            "Specify user(s). Comma-separated list. "
            "Otherwise all users are processed."
        ),
    )
    parser.add_argument(
        "--detail",
        action="store_true",
        help=(
            "If specified, statistics per project "
            "and version are output in addition to "
            "total statistics."
        ),
    )
    parser.add_argument(
        "--include-no-activities",
        action="store_true",
        help=(
            "If specified, stats for users with no "
            "activities are output as well."
            "By default, stats only for users with "
            "any activities are output."
        ),
    )
    parser.add_argument(
        "--no-verify",
        action="store_false",
        dest="verify",
        help="Do not perform HTTPS certificate verification",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug message."
    )
    parser.add_argument("user_yaml", help="YAML file of the user list")
    options = parser.parse_args()

    if "format" not in options:
        options.format = "csv"

    logging_level = logging.DEBUG if options.debug else logging.INFO
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    handler = logging.StreamHandler()
    handler.setLevel(logging_level)
    handler.setFormatter(formatter)
    LOG.setLevel(logging_level)
    LOG.addHandler(handler)

    language_teams = LanguageTeam.load_from_language_team_yaml(
        options.user_yaml, options.lang
    )

    versions = [v.replace("/", "-") for v in options.target_version or []]
    users = get_weblate_stats(
        wc,
        options.verify,
        options.start_date,
        options.end_date,
        language_teams,
        options.project,
        versions,
        options.user,
    )

    output_file = "weblate_stats_output.%s" % options.format
    output_file = output_file or options.output_file

    write_stats_to_file(
        users,
        output_file,
        options.include_no_activities,
        options.detail,
    )


def get_weblate_stats(
    wc,
    verify,
    start_date,
    end_date,
    language_teams,
    project_list,
    version_list,
    user_list,
):
    LOG.info(
        "Getting Weblate contributors statistics (from %s to %s) ...",
        start_date,
        end_date,
    )

    weblateUtil = WeblateUtility(wc, verify)

    if not project_list:
        project_list = weblateUtil.get_projects()
    users = []
    for team in language_teams:
        users += [
            User(user_id, team.language_code)
            for user_id in team.translators
        ]

    data = dict()
    for user in users:
        if user_list and user.user_id not in user_list:
            continue
        user_data = weblateUtil.get_user(user.user_id)

        if "detail" in user_data and user_data["detail"] == "Not found.":
            continue

        LOG.info(
            "Getting for user %(user_id)s %(user_lang)s",
            {"user_id": user.user_id, "user_lang": user.lang},
        )

        unit_data = weblateUtil.get_units(start_date, end_date)
        for unit in unit_data:
            translation_data = weblateUtil.get_translations(
                None,
                None,
                None,
                url=unit["translation"],
                checksum=unit["web_url"],
                user_lang=user.lang,
            )

            if translation_data is None:
                continue

            user_full_name = translation_data["last_author"]
            if user_full_name not in data:
                data[user_full_name] = dict()
                data[user_full_name]["translated"] = 0
                data[user_full_name]["approved"] = 0
                data[user_full_name]["needReview"] = 0
                data[user_full_name]["fuzzy"] = 0
                data[user_full_name]["failingCheck"] = 0
                data[user_full_name]["pending"] = 0

            if unit["translated"]:
                data[user_full_name]["translated"] += 1

            if unit["approved"]:
                data[user_full_name]["approved"] += 1

            if unit["has_suggestion"] or unit["has_comment"]:
                data[user_full_name]["needReview"] += 1

            if unit["fuzzy"]:
                data[user_full_name]["fuzzy"] += 1

            if unit["has_failing_check"]:
                data[user_full_name]["failingCheck"] += 1

            if unit["pending"]:
                data[user_full_name]["pending"] += 1

            LOG.debug("Got: %s", data)

            user.stats = data.get(user_full_name)

    return users


if __name__ == "__main__":
    main()
