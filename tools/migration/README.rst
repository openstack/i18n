=======================================
Migration Tools from Zanata to Weblate
=======================================

This folder provides tools to migrate translation projects from Zanata
to Weblate.

.. note:

  The tool currently works with horizon and plugin projects.

Background
----------

OpenStack I18n team has been using
`Zanata <https://github.com/zanata/zanata-platform>`__
as translation platform, which development and release is discountinued
from August 2018.
To ensure continued translation management and improve OpenStack
internationalization workflow, OpenStack I18n SIG is migrating
Zanata projects to Weblate.

Objectives
----------

* Preserve existing translation structure and format as much as possible

Migration Workflow
------------------

1. Set up the workspace.
2. Generate POT files from cloned project repositories.
3. Create ``zanata.xml`` and export translations (PO files) from Zanata.
4. Create a Weblate project, category, and component.
5. Create translations and upload a translation file for each locale.

How to use
----------

1. Clone the repository
2. Run the migration script:

.. code-block:: bash

   ./migration_resources.sh <project_name> <version> <workspace_name>

Arguments:

* project_name: The name of the OpenStack project to migrate.
* version: The version of the project. The default is "master".
  e.g. stable-2025.1
* workspace_name: The folder name for the migration workspace.
It will be installed in the home directory. The default is "workspace".

Folder and File Structure
--------------
.. code-block:: text

  ├── setup_env/
  └── migration_resources.sh

* setup_env/: Scripts to create a virtual environment and install dependencies.
These scripts also create a workspace folder for migration tasks.
* migration_resources.sh: Main script to migrate translation resources.
They include various modules to perform actual tasks for resource
migration step by step.

.. note::

  The current tool mainly focuses on translation resource migration,
  and actual resource migration process currently requires careful
  supervision to make sure that each migration step is performed
  well or not.

Workspace Structure
-------------------

By default, the migration workspace is installed to your home directory
with the following folder structure:

.. note::

  You can change the base directory by manually setting WORK_DIR
  on setup_env/setup.sh.

* .venv/: Python virtual environment containing migration dependencies
* projects/: Migration workspace

  * <project_name>/: Project-specific workspace

    * <cloned_project_name>/: Cloned project repository
    * pot/: POT files for each component
    * translations/: Exported translations from Zanata

Directory Layout::

.. code-block:: text

  <workspace_name>/
  ├── .venv/
  └── projects/
      └── <project_name>/
          ├── <cloned_project_name>/
          ├── pot/
          └── translations/
