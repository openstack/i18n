#!/usr/bin/env python3

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

import argparse
import configparser
from pathlib import Path
import sys
import tomllib


DJANGO_PROJECT_SUFFIXES = (
    '-dashboard',
    'horizon',  # to match horizon and *-horizon
    '-ui',
)


def get_args():
    parser = argparse.ArgumentParser(
        description='Find module names in a repository.')
    parser.add_argument('-p', '--project', required=True)
    parser.add_argument('-t', '--target',
                        choices=['python', 'django'],
                        default='python',
                        help='Type of modules to search (default: python).')
    parser.add_argument('-f', '--file', default='setup.cfg',
                        help='Path of setup.cfg file.')
    return parser.parse_args()


def split_multiline(value):
    value = [element for element in
             (line.strip() for line in value.split('\n'))
             if element]
    return value


def read_config(path):
    config = read_config_cfg(path)
    config.update(read_config_toml())

    return config


def read_config_cfg(path):
    if not Path(path).exists():
        return {}

    parser = configparser.ConfigParser()
    parser.read(path)

    config = {}
    for section in parser.sections():
        config[section] = dict(parser.items(section))

    return config


def read_config_toml():
    pyproject_path = Path('pyproject.toml')
    if not pyproject_path.exists():
        return {}

    with open(pyproject_path, 'rb') as f:
        config = tomllib.load(f)

    return config


def get_option(config, section, option, multiline=False):
    if section not in config:
        return []
    value = config[section].get(option)
    if not value:
        return []
    if multiline:
        value = split_multiline(value)
    return value


def get_translate_options(config, target):
    translate_options = {}
    for key, value in config['openstack_translations'].items():
        values = split_multiline(value)
        if values:
            translate_options[key] = values
    return translate_options.get('%s_modules' % target, [])


def get_valid_modules(config, project, target):
    is_django = any(project.endswith(suffix)
                    for suffix in DJANGO_PROJECT_SUFFIXES)
    if is_django != (target == 'django'):
        return []

    # setup.cfg
    modules_files = get_option(config, 'files', 'packages', multiline=True)

    # pyproject.toml
    modules_toml_options = get_option(config, 'options', 'packages')
    modules_toml_tool = get_option(
        config.get('tool', {}), 'setuptools', 'packages'
    )
    modules_toml_tool_find = get_option(
        config.get('tool', {}).get('setuptools', {}).get('packages', {}),
        'find',
        'include',
    )

    # get all modules
    modules = list(set(
        modules_files + modules_toml_options + modules_toml_tool +
        modules_toml_tool_find
    ))

    # if no modules has been found in config files,
    # let's assume the project name as a module name.
    if not modules:
        print(
            '[files] packages entry not found in setup.cfg. '
            '[options] packages entry not found in pyproject.toml. '
            '[tool.setuptools] packages entry not found in pyproject.toml. '
            'Use project name "%s" as a module name.' % project,
            file=sys.stderr,
        )
        modules = [project.replace("-", "_")]

    return modules


def main():
    args = get_args()
    config = read_config(args.file)

    if 'openstack_translations' in config:
        translate_options = get_translate_options(config, args.target)
        print(' '.join(translate_options))
        return

    modules = get_valid_modules(config, args.project, args.target)

    if modules:
        print(' '.join(modules))


if __name__ == '__main__':
    main()
