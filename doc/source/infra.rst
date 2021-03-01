==========================
Translation infrastructure
==========================

A series of tasks in OpenStack infrastructure is used to manage translation
changes in Zanata. Without running the tasks, translation changes will not
be reflected into OpenStack projects. This page explains how the infrastructure
tasks run actual scripts as `Zuul <https://docs.openstack.org/infra/zuul/>`_
jobs and monitor the job status.

.. _translation-jobs:

Translation jobs
----------------

We have two types of Zuul jobs for translations: syncing source strings into
Zanata with the latest repositories and pushing translations from Zanata into
the repositories.
The first job is for Zanata-side updates. Up-to-date source strings to be
translated are compared and updated between OpenStack project repositories
and Zanata. If source texts in OpenStack project repositories are changed,
then change sets are pushed into Zanata so translators deal with up-to-date
source strings.
On the other hand, the second job is aimed to reflect changes in translated
strings in Zanata (after translators do translation activities) into
corresponding OpenStack project repositories. The job will propose changes
as :doc:`Translation Import <reviewing-translation-import>` Gerrit patches.

Update jobs for Zanata start after patches are merged on OpenStack project
repositories, and Zuul starts to run tasks everyday at **6:00 UTC** for
the updates on OpenStack project repositories.

Note that not all translation changes are the target for translation
jobs. The goal is to have consistent translated programs, UIs, and
documentation. There is not much sense if only a few lines are
translated. The team has decided that files that have at least 75
percent of messages translated will be in the git repositories.

To not have too much churn and last minute string fixes lead to files
get removed, there is also a lower threshold for releases of **66
percent** of messages translated as policy - which is only manually
enforced.

The OpenStack infra scripts executed by tasks currently download new files that
are at least **75 percent** translated and if files grow over time but do not
get new translations (or strings change too much), they will be
removed again automatically from the project with a lower threshold of
currently **40 percent**.

.. _monitoring-translation-job-status:

Monitoring translation jobs status
----------------------------------

The `Zuul Builds Page <https://zuul.opendev.org/t/openstack/builds>`__
provides us a convenient way to check the translation job status.

* `Post jobs - Syncing to Zanata <https://zuul.opendev.org/t/openstack/builds?job_name=upstream-translation-update>`__
* `Periodic jobs: Syncing into repos <http://zuul.opendev.org/t/openstack/builds?job_name=propose-translation-update>`__

.. _translation_scripts:

Translation infrastructure tasks and scripts
--------------------------------------------

Translation infrastructure tasks are stored and managed in
`openstack/project-config <https://opendev.org/openstack/project-config/>`__
repository. The translation infrastructure scripts are stored and managed in `openstack/openstack-zuul-jobs <https://opendev.org/openstack/openstack-zuul-jobs>`__
repository.

* `upstream-translation-update.yaml <https://opendev.org/openstack/project-config/src/playbooks/translation/upstream-translation-update.yaml>`__

  * Implements the first Zuul job (Syncing to Zanata) by executing
    `upstream_translation_update.sh <https://opendev.org/openstack/openstack-zuul-jobs/src/roles/prepare-zanata-client/files/upstream_translation_update.sh>`__

* `propose-translation-update.yaml <https://opendev.org/openstack/project-config/src/playbooks/translation/propose-translation-update.yaml>`__

  * Carries out the second Zuul job (Syncing into repos) by executing
    `propose_translation_update.sh <https://opendev.org/openstack/openstack-zuul-jobs/src/roles/prepare-zanata-client/files/propose_translation_update.sh>`__
  * This job renames Chinese locales in Zanata (``zh-cn`` and ``zh-tw``)
    to ``zh-hans`` and ``zh-hant`` for horizon related projects.
    For other projects and documentations (including docs in horizon related
    projects), ``zh-cn`` and ``zh-tw`` are used as-is.
    For more details, see :ref:`handling_horizon_projects`.

* `common_translation_update.sh <https://opendev.org/openstack/openstack-zuul-jobs/src/roles/prepare-zanata-client/files/common_translation_update.sh>`__

  * Common code used by **propose_translation_update.sh** and
    **upstream_translation_update.sh**

* `create-zanata-xml.py <https://opendev.org/openstack/openstack-zuul-jobs/src/roles/prepare-zanata-client/files/create-zanata-xml.py>`__

  * Python script to setup projects for Zanata

* `releasenotes/pre.yaml <https://opendev.org/openstack/project-config/src/playbooks/releasenotes/pre.yaml>`__
* `releasenotes/run.yaml <https://opendev.org/openstack/project-config/src/playbooks/releasenotes/run.yaml>`__

  * Builds release notes in both the original (English) version and translated
    versions (if any).

Note that the scripts in the tasks use `zanata-cli <http://docs.zanata.org/en/release/client/>`__
to pull and push translation content.

Debugging job scripts
---------------------

See :doc:`infra-debug`.
