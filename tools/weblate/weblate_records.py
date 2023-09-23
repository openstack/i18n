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

from abc import ABC
from dataclasses import asdict
from dataclasses import dataclass
from typing import Optional


class AbstractWeblateRecord(ABC):
    def to_dict(self):
        return asdict(self)


@dataclass
class WeblateObjectStats(AbstractWeblateRecord):
    """Object statistics API response

    weblate-4.18.2
    GET /api/(str: object)/statistics/
    """

    total: int
    total_words: int
    total_chars: int
    last_change: str
    translated: int
    translated_percent: float
    translated_words: int
    translated_words_percent: float
    translated_chars: int
    translated_chars_percent: float
    fuzzy: int
    fuzzy_percent: float
    failing: int
    failing_percent: float
    approved: int
    approved_percent: float
    readonly: int
    readonly_percent: float
    suggestions: int
    comments: int
    name: str
    url: str
    url_translate: str
    code: str

    @classmethod
    def from_dict(cls, data_dict):
        return cls(**data_dict)


@dataclass
class WeblateProject(AbstractWeblateRecord):
    """Project API response

    weblate-4.18.2
    GET /api/projects/
    GET /api/projects/(str: project)/
    GET /api/(str: project)/statistics/
    """

    name: str
    slug: str
    web: str
    components_list_url: str
    repository_url: str
    changes_list_url: str
    translation_review: bool
    source_review: bool
    set_language_team: bool
    enable_hooks: bool
    instructions: str
    language_aliases: str

    @classmethod
    def from_dict(cls, data_dict):
        return cls(**data_dict)


@dataclass
class WeblateProjectStats(AbstractWeblateRecord):
    """Project statistics API response

    weblate-4.18.2
    GET /api/(str: project)/statistics/
    """

    total: int
    total_words: int
    total_chars: int
    last_change: str
    translated: int
    translated_percent: float
    translated_words: int
    translated_words_percent: float
    translated_chars: int
    translated_chars_percent: float
    fuzzy: int
    fuzzy_percent: float
    failing: int
    failing_percent: float
    approved: int
    approved_percent: float
    readonly: int
    readonly_percent: float
    recent_changes: int
    suggestions: int
    comments: int
    name: str
    url: str
    url_translate: Optional[str] = None
    code: Optional[str] = None

    @classmethod
    def from_dict(cls, data_dict):
        return cls(**data_dict)


@dataclass
class WeblateUserStats(AbstractWeblateRecord):
    """User statistics API response

    weblate-4.18.2
    GET /api/users/(str: username)/statistics/
    """

    translated: int
    suggested: int
    uploaded: int
    commented: int
    languages: int

    @classmethod
    def from_dict(cls, data_dict):
        return cls(**data_dict)


@dataclass
class WeblateUserInfo(AbstractWeblateRecord):
    """User information API response

    weblate-4.18.2
    GET /api/users/(str: username)/
    """

    username: str
    full_name: str
    email: str
    is_superuser: bool
    is_active: bool
    is_bot: bool
    date_joined: str
    groups: list
    url: Optional[str] = None
    statistics_url: Optional[str] = None

    @classmethod
    def from_dict(cls, data_dict):
        return cls(**data_dict)


@dataclass
class WeblateGroupInfo(AbstractWeblateRecord):
    """Group information API response

    weblate-4.18.2
    GET /api/groups/(int: id)/
    """

    name: str
    project_selection: int
    language_selection: int
    roles: list
    projects: list
    components: list
    componentlists: list
    defining_project: Optional[str]
    url: Optional[str] = None

    @classmethod
    def from_dict(cls, data_dict):
        return cls(**data_dict)


@dataclass
class WeblateComponentInfo(AbstractWeblateRecord):
    """Component API response

    weblate-4.18.2
    GET /api/components/(string: project)/(string: component)/
    """

    project: str
    name: str
    slug: str
    vcs: str
    repo: str
    git_export: str
    branch: str
    push_branch: str
    filemask: str
    template: str
    edit_template: str
    intermediate: str
    new_base: str
    file_format: str
    license: str
    agreement: str
    new_lang: str
    language_code_style: str
    push: str
    check_flags: str
    priority: str
    enforced_checks: str
    restricted: str
    repoweb: str
    report_source_bugs: str
    merge_style: str
    commit_message: str
    add_message: str
    delete_message: str
    merge_message: str
    addon_message: str
    pull_message: str
    allow_translation_propagation: str
    enable_suggestions: str
    suggestion_voting: str
    suggestion_autoaccept: str
    push_on_commit: str
    commit_pending_age: str
    auto_lock_error: str
    language_regex: str
    variant_regex: str
    is_glossary: bool
    glossary_color: str
    repository_url: str
    translations_url: str
    lock_url: str
    changes_list_url: str
    task_url: str
    source_language: dict

    @classmethod
    def from_dict(cls, data_dict):
        return cls(**data_dict)


@dataclass
class WeblateTranslationInfo(AbstractWeblateRecord):
    """Translation API response

    weblate-4.18.2
    GET /api/translations/(string: project)/(string: component)/(string: lang)/
    """

    component: dict
    failing_checks: int
    failing_checks_percent: float
    failing_checks_words: int
    filename: str
    fuzzy: int
    fuzzy_percent: float
    fuzzy_words: int
    have_comment: int
    have_suggestion: int
    is_template: bool
    language: dict
    language_code: str
    last_author: str
    last_change: str
    revision: str
    share_url: str
    total: int
    total_words: int
    translate_url: str
    translated: int
    translated_percent: float
    translated_words: int
    repository_url: str
    file_url: str
    changes_list_url: str
    units_list_url: str

    @classmethod
    def from_dict(cls, data_dict):
        return cls(**data_dict)


@dataclass
class WeblateChangeInfo(AbstractWeblateRecord):
    """Change API response

    weblate-4.18.2
    GET /api/changes/(int: id)/
    """

    unit: str
    translation: str
    component: str
    user: str
    author: str
    timestamp: str
    action: int
    action_name: str
    target: str
    id: int

    @classmethod
    def from_dict(cls, data_dict):
        return cls(**data_dict)
