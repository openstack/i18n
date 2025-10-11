#!/bin/bash
# Set venv and folder structure for migration

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

WORK_DIR="$HOME/$WORKSPACE_NAME"

function create_python_venv() {
    if ! command -v python3 &> /dev/null; then
        echo "[ERROR] Python 3 is not installed"
        return 1
    fi

    # create venv
    if [ ! -d "$WORK_DIR/.venv" ]; then
        python3 -m venv "$WORK_DIR/.venv" >/dev/null 2>&1
        if [ $? -ne 0 ]; then
            echo "[ERROR] Failed to create virtual environment"
            return 1
        fi
    fi

    echo "[INFO] Virtual environment created"
    return 0
}

function install_dependencies() {
    source "$WORK_DIR/.venv/bin/activate"

    cd "$SCRIPTSDIR/setup_env"
    # Install python dependencies
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "[ERROR] Failed to install requirements.txt in venv."
        return 1
    fi

    # Install dependencies with bindep
    bindep_packages=$("$WORK_DIR/.venv/bin/bindep" -b -f bindep.txt 2>/dev/null)
    if [ -n "$bindep_packages" ]; then
        echo "[INFO] Installing system dependencies with bindep: $bindep_packages"
        sudo apt install -y $bindep_packages
        if [ $? -ne 0 ]; then
            echo "[ERROR] Failed to install system dependencies with bindep"
            return 1
        fi
    fi

    return 0
}

function check_zanata_cli() {
    # Check zanata-cli is installed
    if ! command -v zanata-cli &> /dev/null; then
        echo "[ERROR] zanata-cli is not installed"
        return 1
    fi

    # Check zanata.ini file exists
    if [ ! -f "$HOME/.config/zanata.ini" ]; then
        echo "[ERROR] zanata.ini is not found"
        return 1
    fi
    echo "[INFO] zanata-cli is installed and zanata.ini file exists"
    return 0
}

function setup_env() {
    if ! prepare_workspace; then
        echo "[ERROR] Failed to prepare workspace."
        return 1
    fi

    if ! create_python_venv; then
        echo "[ERROR] Failed to create python venv"
        return 1
    fi

    if ! install_dependencies; then
        echo "[ERROR] Failed to install dependencies."
        echo "[ERROR] Please check bindep.txt and requirements.txt"
        return 1
    fi

    if ! check_zanata_cli; then
        echo "[ERROR] Failed to check zanata-cli."
        echo "[ERROR] Please check if zanata-cli is installed and zanata.ini file exists."
        return 1
    fi

    echo "[INFO] Environment setup successfully"
    return 0
}

function prepare_workspace() {
    # Create workspace directory
    if [ ! -d "$WORK_DIR" ]; then
        if ! mkdir -p "$WORK_DIR"; then
            echo "[ERROR] Failed to create $WORKSPACE_NAME directory"
            return 1
        fi
    fi

    # Create projects directory
    if [ ! -d "$WORK_DIR/projects" ]; then
        if ! mkdir -p "$WORK_DIR/projects"; then
            echo "[ERROR] Failed to create projects directory"
            return 1
        fi
    fi

    echo "[INFO] Workspace directory created successfully"
    return 0

}

function prepare_project_workspace() {
    local project=$1

    # Create project directory
    if [ ! -d "$WORK_DIR/projects/$project" ]; then
        mkdir -p $WORK_DIR/projects/$project
    fi

    # Create pot directory
    if [ ! -d "$WORK_DIR/projects/$project/pot" ]; then
        mkdir -p $WORK_DIR/projects/$project/pot
        echo "[INFO] Pot directory created successfully"
    fi

    # Create translations directory
    if [ ! -d "$WORK_DIR/projects/$project/translations" ]; then
        mkdir -p $WORK_DIR/projects/$project/translations
        echo "[INFO] Translations directory created successfully"
    fi

    return 0
}

function setup_env_and_prepare_workspace() {
    local project=$1

    # Create a virtual environment and install system dependencies
    echo "[INFO] Setup the virtual environment and install system dependencies"
    if ! setup_env; then
        echo "[ERROR] Failed to setup environment"
        return 1
    fi

    # Prepare workspace folders for migration tasks
    echo "[INFO] Prepare workspace folders"
    if ! prepare_workspace; then
        echo "[ERROR] Failed to prepare workspace"
        return 1
    fi

    prepare_project_workspace "$project"
    return 0
}