#!/bin/bash -xe

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

PROJECT=$1
BRANCH=$2
JOBNAME=$3
HORIZON_DIR=$4

# Replace /'s in the branch name with -'s because Zanata does not
# allow /'s in version names.
ZANATA_VERSION=${BRANCH//\//-}

SCRIPTSDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source $SCRIPTSDIR/common_translation_update.sh

init_branch $BRANCH

function cleanup_module {
    local modulename=$1

    # Remove obsolete files.
    cleanup_po_files "$modulename"
    cleanup_pot_files "$modulename"

    # Compress downloaded po files, this needs to be done after
    # cleanup_po_files since that function needs to have information the
    # number of untranslated strings.
    compress_po_files "$modulename"
}

# Add all po files to the git repo in a target directory
function git_add_po_files {
    local target_dir=$1

    local po_file_count

    po_file_count=`find $1 -name *.po | wc -l`

    if [ $po_file_count -ne 0 ]; then
        git add $target_dir/*/*
    fi
}

# Add all JSON files to the git repo (used in javascript translations)
function git_add_json_files {
    local target_dir=$1

    local json_file_count

    json_file_count=`find $1 -name '*.json' | wc -l`

    if [ $json_file_count -ne 0 ]; then
        git add $target_dir/*
    fi
}

# Propose updates for manuals
function propose_manuals {

    # Pull updated translations from Zanata.
    pull_from_zanata "$PROJECT"

    # Compress downloaded po files
    case "$PROJECT" in
        openstack-manuals)
            # Cleanup po and pot files
            cleanup_module "doc"
            ;;
        api-site)
            # Cleanup po and pot files
            cleanup_module "api-quick-start"
            cleanup_module "firstapp"
            ;;
        security-doc)
            cleanup_module "security-guide"
            ;;
    esac

    # Add imported upstream translations to git
    for FILE in ${DocFolder}/*; do
        DOCNAME=${FILE#${DocFolder}/}
        if [ -d ${DocFolder}/${DOCNAME}/locale ] ; then
            git_add_po_files ${DocFolder}/${DOCNAME}/locale
        fi
        if [ -d ${DocFolder}/${DOCNAME}/source/locale ] ; then
            git_add_po_files ${DocFolder}/${DOCNAME}/source/locale
        fi
    done
}

# Propose updates for training-guides
function propose_training_guides {

    # Pull updated translations from Zanata.
    pull_from_zanata "$PROJECT"

    # Cleanup po and pot files
    cleanup_module "doc/upstream-training"

    # Add all changed files to git
    git_add_po_files doc/upstream-training/source/locale
}

# Propose updates for i18n
function propose_i18n {

    # Pull updated translations from Zanata.
    pull_from_zanata "$PROJECT"

    # Cleanup po and pot files
    cleanup_module "doc"

    # Add all changed files to git
    git_add_po_files doc/source/locale
}

# Propose updates for python and django projects
function propose_python_django {
    local modulename=$1
    local version=$2

    # Check for empty directory and exit early
    local content

    content=$(ls -A $modulename/locale/)

    if [[ "$content" == "" ]] ; then
        return
    fi

    # Now add all changed files to git.
    # Note we add them here to not have to differentiate in the functions
    # between new files and files already under git control.
    git_add_po_files $modulename/locale

    # Cleanup po and pot files
    cleanup_module "$modulename"
    if [ "$version" == "master" ] ; then
        # Remove not anymore translated log files on master, but not
        # on released stable branches.
        cleanup_log_files "$modulename"
    fi

    # Check first whether directory exists, it might be missing if
    # there are no translations.
    if [[ -d "$modulename/locale/" ]] ; then

        # Some files were changed, add changed files again to git, so
        # that we can run git diff properly.
        git_add_po_files $modulename/locale
    fi
}


# Handle either python or django proposals
function handle_python_django_project {
    local project=$1

    setup_project "$project" "$ZANATA_VERSION"
    pull_from_zanata "$project"
    rename_django_chinese_locales "$project" "$BRANCH"
    handle_python_django $project python
    handle_python_django $project django
    handle_project_doc $project
}

# Handle project doc proposals
function handle_project_doc {
    local project=$1
    # Doing only things in the test repos for project doc translation
    if ! [[ ${DOC_TARGETS[*]} =~ "$project" ]]; then
        return
    fi
    # setup_project and pull_from_zanata are already done
    # we start directly with generating .pot files
    extract_messages_doc
    # cleanup po and pot files
    cleanup_module "doc"
    # Add all changed files to git
    git_add_po_files doc/source/locale
}

# Rename existing Chinese locales in the project repository
# (zh_CN -> zh_Hans, zh_TW -> zh_Hant)
# NOTE: This is expected to call after pulling translations from zanata.
function rename_django_chinese_locales {
    local project=$1
    local branch=$2
    local module_name module_names
    local old_locale new_locale

    # Renaming Chinese locales is unnecessary for Victoria or earlier.
    # TODO(amotoki): Once all stable branches support the new Chinese locales
    # in horizon and its plugins, this branch check can be dropped.
    case "$branch" in
        stable/ussuri|stable/victoria) return ;;
        *) ;;
    esac

    declare -A locale_rename_map=(
        ["zh_CN"]="zh_Hans"
        ["zh_TW"]="zh_Hant"
    )

    module_names=$(get_modulename $project django)
    for module_name in $module_names; do
        for old_locale in "${!locale_rename_map[@]}"; do
            new_locale=${locale_rename_map[$old_locale]}
            rm -rf $module_name/locale/$new_locale
            if [ -d $module_name/locale/$old_locale ]; then
                mv $module_name/locale/$old_locale $module_name/locale/$new_locale
            fi
            if git ls-files | grep -q $module_name/locale/$old_locale; then
                git rm -r $module_name/locale/$old_locale
            fi
        done
    done
}


# Handle either python or django proposals
function handle_python_django {
    local project=$1
    # kind can be "python" or "django"
    local kind=$2
    local module_names

    module_names=$(get_modulename $project $kind)
    if [ -n "$module_names" ]; then
        if [[ "$kind" == "django" ]] ; then
            install_horizon
        fi
        propose_releasenotes "$ZANATA_VERSION"
        for modulename in $module_names; do
            # Note that we need to generate the pot files so that we
            # can calculate how many strings are translated.
            case "$kind" in
                django)
                    # Update the .pot file
                    extract_messages_django "$modulename"
                    ;;
                python)
                    # Extract messages from project except log messages
                    extract_messages_python "$modulename"
                    ;;
            esac
            propose_python_django "$modulename" "$ZANATA_VERSION"
        done
    fi
}


function propose_releasenotes {
    local version=$1

    # This function does not check whether releasenote publishing and
    # testing are set up in zuul/layout.yaml. If releasenotes exist,
    # they get pushed to the translation server.

    # Note that releasenotes only get translated on master.
    if [[ "$version" == "master" && -f releasenotes/source/conf.py ]]; then

        # Note that we need to generate these so that we can calculate
        # how many strings are translated.
        extract_messages_releasenotes "keep_workdir"

        local lang_po
        local locale_dir=releasenotes/source/locale
        for lang_po in $(find $locale_dir -name 'releasenotes.po'); do
            check_releasenotes_per_language $lang_po
        done

        # Remove the working directory. We no longer needs it.
        rm -rf releasenotes/work

        # Cleanup POT files.
        # PO files are already clean up in check_releasenotes_translations.
        cleanup_pot_files "releasenotes"

        # Compress downloaded po files, this needs to be done after
        # cleanup_po_files since that function needs to have information the
        # number of untranslated strings.
        compress_po_files "releasenotes"

        # Add all changed files to git - if there are
        # translated files at all.
        if [ -d releasenotes/source/locale/ ] ; then
            git_add_po_files releasenotes/source/locale
        fi
    fi

    # Remove any releasenotes translations from stable branches, they
    # are not needed there.
    if [[ "$version" != "master" && -d releasenotes/source/locale ]]; then
        # Note that content might exist, e.g. from downloaded translations,
        # but are not under git control.
        git rm --ignore-unmatch -rf releasenotes/source/locale
    fi
}


function propose_reactjs {
    pull_from_zanata "$PROJECT"

    # Clean up files (removes incomplete translations and untranslated strings)
    cleanup_module "i18n"

    # Convert po files to ReactJS i18n JSON format
    for lang in `find i18n/*.po -printf "%f\n" | sed 's/\.po$//'`; do
        npm run po2json -- ./i18n/$lang.po -o ./i18n/$lang.json
        # The files are created as a one-line JSON file - expand them
        python -m json.tool ./i18n/$lang.json ./i18n/locales/$lang.json
        rm ./i18n/$lang.json
    done

    # Add JSON files to git
    git_add_json_files i18n/locales
}


# Setup git repository for git review.
setup_git

# Check whether a review already exists, setup review commit message.
# Function setup_review calls setup_commit_message which will set CHANGE_ID and
# CHANGE_NUM if a change exists and will always set COMMIT_MSG.
setup_review "$BRANCH"

# If a change already exists, let's pull it in and compute the
# 'git patch-id' of it.
PREV_PATCH_ID=""
if [[ -n ${CHANGE_NUM} ]]; then
    # Ignore errors we get in case we can't download the patch with
    # git-review. If that happens then we will submit a new patch.
    set +e
    git review -d ${CHANGE_NUM}
    RET=$?
    if [[ "$RET" -eq 0 ]]; then
        PREV_PATCH_ID=$(git show | git patch-id | awk '{print $1}')
    fi
    set -e
    # The git review changed our branch, go back to our correct branch
    git checkout -f ${BRANCH}
fi

# Setup venv - needed for all projects for subunit
setup_venv

case "$PROJECT" in
    api-site|openstack-manuals|security-doc)
        init_manuals "$PROJECT"
        setup_manuals "$PROJECT" "$ZANATA_VERSION"
        propose_manuals
        propose_releasenotes "$ZANATA_VERSION"
        ;;
    training-guides)
        setup_training_guides "$ZANATA_VERSION"
        propose_training_guides
        ;;
    i18n)
        setup_i18n "$ZANATA_VERSION"
        propose_i18n
        ;;
    tripleo-ui)
        setup_reactjs_project "$PROJECT" "$ZANATA_VERSION"
        propose_reactjs
        ;;
    *)
        # Common setup for python and django repositories
        handle_python_django_project $PROJECT
        ;;
esac

# Filter out commits we do not want.
filter_commits

# Propose patch to gerrit if there are changes.
send_patch "$BRANCH"

if [ $INVALID_PO_FILE -eq 1 ] ; then
    echo "At least one po file in invalid. Fix all invalid files on the"
    echo "translation server."
    exit 1
fi
# Tell finish function that everything is fine.
ERROR_ABORT=0
