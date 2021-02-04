=====================
Debugging job scripts
=====================

While it would be rare, you may would like to debug the translation
job scripts. This section describes tips for such cases.
``propose_translation_update.sh`` is mainly covered.

.. note::

   It is not a complete document for debugging.
   It was just written as a note. Feel free to add more topics.

Environment
-----------

It is better to use the same environment (e.g., Linux distribution version)
used in the translation job. To find the information, check ``nodeset`` of the
``propose-translation-update`` job definition in
`zuul configuration <https://opendev.org/openstack/project-config/src/branch/master/zuul.d/jobs.yaml>`__
in openstack/project-config repository.
As of Feb 2021, ``ubuntu-bionic`` is used.

Preparations
------------

You can prepare dependencies by following
`prepare-zanata-client role <https://opendev.org/openstack/openstack-zuul-jobs/src/branch/master/roles/prepare-zanata-client/tasks/main.yaml>`__.

What you need are:

* Installing Zanata CLI and its dependencies.
  Ensure ``zanata-cli`` command is found in your path.
* Prepare ``~/.config/zanata.ini``.
  See :ref:`Zanata CLI <zanata-cli>` for more detail.
* Copy the translation scripts to your working directory from
  `openstack-zuul-jobs/roles/prepare-zanata-client/files <https://opendev.org/openstack/openstack-zuul-jobs/src/branch/master/roles/prepare-zanata-client/files>`__.
  In addition, you need to copy ``common.sh`` from
  `project-config/roles/copy-proposal-common-scripts/files <https://opendev.org/openstack/project-config/src/branch/master/roles/copy-proposal-common-scripts/files>`__
  to the same working directory.

Commenting out CI-specific codes
--------------------------------

The job scripts contain codes specific to OpenStack CI.
For example, there is a code to communicate with OpenStack gerrit
and the account is hardcoded.
It looks convenient to comment out such code blocks
to debug the scripts in a local env. It should be useful
unless you are debuging a CI-specific issue.

Code blocks which look better to be commented out are:

* common_translation_update.sh

  * ``trap "finish" EXIT`` (It depends on testrepository and usually fails in
    local envs)

* propose_translation_update.sh

  * ``setup_review`` and a logic to check an existing change
    (It is unnecessary as we do not propose a real change to gerrit.
    The account used is hardcoded and it always fails in local runs.)
  * ``send_patch`` (It is unnecessary as we do not want to propose
    a real change to gerrit.)
  * (optional)
    The main logic (from ``case "$PROJECT" in`` to ``filter_commits``)
    (we will debug the main logic, so perhaps we would like to run the script
    piece by piece.)

The diff would be like http://paste.openstack.org/show/802260/.

Copying upper-constraints.txt
-----------------------------

The job scripts assume that upper-constraints.txt exists in the top directory of
the target project repository.

.. code-block:: console

   $ cd $PROJECT_DIR
   $ wget https://releases.openstack.org/constraints/upper/master

Note that you need to adjust the URL of the upper-constraints file
when you work on a stable branch.

Creating ~/.venv virtualenv
---------------------------

The job scripts assume that required python modules are installed in
``~/.venv`` virtualenv. In the zuul job, this virtualenv is prepared via
``ensure-sphinx`` and ``ensure-babel`` roles in zuul/zuul-jobs.
You need to do the same.

Note that doc/requirements.txt in most projects are almost samer so perhaps you
can reuse this virtualenv for most projects. If it does not work, consider
recreating the virtualenv.

.. code-block:: bash

   $ python3 -m venv ~/.venv
   $ . ~/.venv/bin/activate
   # $PROJECT_DIR is a target project repository like horizon, ironic-ui ....
   (.venv) $ cd $PROJECT_DIR
   # Install sphinx related modules ensure-sphinx installs
   (.venv) $ pip install -r doc/requirements.txt -c ../requirements/upper-constraints.txt
   # Install modules ensure-babel installs
   (.venv) $ pip install Babel lxml pbr requests -c ../requirements/upper-constraints.txt
   (.venv) $ deactivate

Loading scripts
---------------

.. code-block:: bash

   # It is better to start a new shell when debugging the script
   $ bash
   > cd $PROJECT_REPO
   # The arguments are: {{ zuul.project.short_name }} {{ zuul.branch }} {{ zuul.job }} $HORIZON_REPO
   > . $WORKDIR/propose_translation_update.sh ironic-ui master propose-translation-update ../horizon
   >

Simulating translation changes
------------------------------

If you would like to simulate translation changes, you can download translations
in advance (using zanata-cli) and modify them as you want.
In such case, you can modify the script as follows:

.. code-block:: console

   --- a/roles/prepare-zanata-client/files/common_translation_update.sh
   +++ b/roles/prepare-zanata-client/files/common_translation_update.sh
   @@ -734,7 +732,8 @@ function pull_from_zanata {
        # Since Zanata does not currently have an option to not download new
        # files, we download everything, and then remove new files that are not
        # translated enough.
   -    zanata-cli -B -e pull
   +    #zanata-cli -B -e pull
   +    cp -r $DOWNLOAD_TRANSLATIONS/$project/* .

        # We skip directories starting with '.' because they never contain
        # translations for the project (in particular, '.tox'). Likewise

You can download translations as below.
``zanata.xml`` will be created once you run the propose_translation_update.sh
(or you can prepare it by following :ref:`zanata-cli` "Project configuration").

.. code-block:: console

   $ cd $DOWNLOAD_TRANSLATIONS/$project
   $ zanata-cli -B -e pull --project-config $PROJECT_DIR/zanata.xml
