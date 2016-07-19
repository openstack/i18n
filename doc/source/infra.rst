==========================
Translation infrastructure
==========================

A series of scripts in OpenStack infrastructure is used to manage translation
changes in Zanata. Without running the scripts, translation changes will not
be reflected into OpenStack projects. This page explains how the infrastructure
scripts runs as Jenkins jobs and monitor the jobs status.

Translation jobs
================

We have two types of Jenkins jobs for translations: syncing Zanata with the
latest repositories and pushing translations into the repositories.
The first job is for Zanata-side updates. It enables Zanata to have up-to-date
texts to be translated by comparing OpenStack project repositories and Zanata.
On the other hand, the second job is aimed to reflect changes related to
translations. For example, if you contribute translations in Zanata, the
translation results need to be pushed to the corresponding repositories.

To find updates for both Zanata and OpenStack project repositories,
Jenkins starts to run scripts everyday at **6:00 UTC**.

Note that not all translation changes are the target for translation jobs.
Currently, we define that the jobs only download new files that are at least
**75 percent** translated and if files grow over time but do not get new
translations (or strings change too much), they will be removed again from the
project with a threshold of **20 percent**. For the glossary
(openstack-manuals/doc/glossary) and common (openstack-manuals/doc/common)
directories, the download limit is **8 percent** because these documents are
large and only a part is used. The purpose of thresholds is to reduce the
amount of patches that go into a project.

Monitoring translation jobs status
==================================

`OpenStack Health <http://status.openstack.org/openstack-health/#/>`__
dashboard provides us a convenient way to check the translation job status.

* `Post jobs - Syncing to Zanata <http://status.openstack.org/openstack-health/#/g/build_queue/post?groupKey=build_queue&searchJob=translation>`__
* `Periodic jobs: Syncing into repos <http://status.openstack.org/openstack-health/#/g/build_queue/periodic?groupKey=build_queue&searchJob=translation>`__

Translation infrastructure scripts
==================================

Translation infrastructure scripts are stored and managed in
`openstack-infra/project-config <http://git.openstack.org/cgit/openstack-infra/project-config>`__
repository.

* `upstream_translation_update.sh <http://git.openstack.org/cgit/openstack-infra/project-config/tree/jenkins/scripts/upstream_translation_update.sh>`__

  * Implements the first Jenkins job (Syncing to Zanata).

* `propose_translation_update.sh <http://git.openstack.org/cgit/openstack-infra/project-config/tree/jenkins/scripts/propose_translation_update.sh>`__

  * Carries out the second Jenkins job (Syncing into repos).

* `common_translation_update.sh <http://git.openstack.org/cgit/openstack-infra/project-config/tree/jenkins/scripts/common_translation_update.sh>`__

  * Common code used by **propose_translation_update.sh** and
    **upstream_translation_update.sh**

* `create-zanata-xml.py <http://git.openstack.org/cgit/openstack-infra/project-config/tree/jenkins/scripts/create-zanata-xml.py>`__

  * Python script to setup projects for Zanata

Note that the scripts use `zanata-cli <http://docs.zanata.org/projects/zanata-client/en/latest/>`__
to pull and push translation content.
