=========================
How to check translations
=========================

It is important to validate your translations by applying them in a real
situation where they are rendered and visualized. This page describes how to
check your translations.

.. note::

   ``translation check`` refers to build OpenStack artifacts with translated
   strings and check how the translated strings are shown on an actual screen
   as part of the translation process.

Documentation
-------------

Translated documents are available at the OpenStack Documentation site.
It is updated daily. Most contents are linked from:

* https://docs.openstack.org/<lang> contains released documents.
  Follow "Languages" in https://docs.openstack.org/.

The documents are maintained in the ``doc`` directory using `reStructuredText
<https://docutils.sourceforge.io/rst.html>`__ and built by `Sphinx
<https://www.sphinx-doc.org/>`__. Translated strings are stored as `Gettext PO
file format <https://www.gnu.org/server/standards/translations/po-how-to.html>`__
in ``locale/<lang>/LC_MESSAGES`` directory.

Documents on openstack-manuals
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For OpenStack documentation, `openstack-manuals git repository
<https://opendev.org/openstack/openstack-manuals>`_ hosts essential
OpenStack documents such as `Installation Guide
<https://docs.openstack.org/install-guide/>`_, and `Virtual Machine
Image Guide <https://docs.openstack.org/image-guide/>`_.

To build a translated document on this repository, you need to update the file
``doc-tools-check-languages.conf`` in each repository, and
add an entry to ``BOOKS`` like ``["ja"]="install-guide"``.

For a document in a stable branch, such as the installation guide for
Liberty, you need to update the file ``doc-tools-check-languages.conf``
in the target stable branch directly.

You can check a generated document for a specified branch on
``https://docs.openstack.org/<branch>/<language>/<document>``.
For example, the link of Japanese Ubuntu Installation Guide for Liberty is
https://docs.openstack.org/liberty/ja/install-guide-ubuntu/.

To add a link to a generated document, you need to update the file
``www/<lang>/index.html`` in the ``master`` branch of
the ``openstack-manuals`` repository.
Note that the web pages are published from ``master`` branch,
which contains the pages for all releases, such as Liberty.
Therefore, you don't need to update the file ``www/<lang>/index.html``
in the stable branch.

You can also check:

* `build status for publishing on Zuul <https://zuul.openstack.org/builds?job_name=build-tox-manuals-publishdocs>`__
* `checkbuild with drafts on Zuul <https://zuul.openstack.org/builds?job_name=build-tox-manuals-publishlang>`__


OpenStack project documentation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Currently, we support translations for small set of OpenStack project
documentations like Horizon, OpenStack-Ansible, and OpenStack-Helm upon
requests and available bandwidth. Top-level directory structure on
``doc/source/`` follows with `Documentation Contributor Guide - Project guide
setup <https://docs.openstack.org/doc-contrib-guide/project-guides.html>`_ and
the corresponding generated documents for ``master`` branch are available at
``https://docs.openstack.org/<project>/latest/<language>/<document>`` URL.
For project team documents in stable branch, you can check the documents with
``https://docs.openstack.org/<project>/<branch>/<language>/<document>`` URL.

Here are sample document links as examples:

* `Korean OpenStack-Helm Installation Guide (no branch) <https://docs.openstack.org/openstack-helm/latest/ko_KR/install/index.html>`_
* `German OpenStack-Ansible User Guide for 2023.1 <https://docs.openstack.org/openstack-ansible/2023.1/de/user/index.html>`_

OpenStack Dashboard
-------------------

Running OpenStack-Ansible
~~~~~~~~~~~~~~~~~~~~~~~~~

`OpenStack-Ansible (OSA) <https://docs.openstack.org/openstack-ansible/latest/>`__
provides Ansible playbooks and roles for the deployment and
configuration of an OpenStack environment. As part of the project a feature
named 'Translation Check Site' is developed. An OSA instance will fetch
translation strings from `translation platform <https://translate.openstack.org/>`__,
compile and serve these strings in Horizon. You need a machine with
two or four CPU cores, at least 8 GB memory and 70 GB disk to run OSA.


.. code-block:: console

   $ BRANCH=master
   $ git clone -b ${BRANCH} https://github.com/openstack/openstack-ansible /opt/openstack-ansible
   $ cd /opt/openstack-ansible
   $ ./scripts/gate-check-commit.sh translations

You can set the components of your AIO installation in
``tests/vars/bootstrap-aio-vars.yml``. Dependly on your environment
the installation takes 1-2 hours.
For more details on the AIO configuration, please see `OSA AIO documentation <https://docs.openstack.org/openstack-ansible/latest/user/aio/quickstart.html#building-an-aio>`_.

To fetch translated files regularly, execute this command manually or
as a cron:

.. code-block:: console

   $ cd /opt/openstack-ansible/playbooks; \
     openstack-ansible os-horizon-install.yml \
     -e horizon_translations_update=True \
     -e horizon_translations_project_version=master \
     --tags "horizon-config"

Running DevStack
~~~~~~~~~~~~~~~~

Another convenient way is to check dashboard translations is to run DevStack in
your local environment. To run DevStack, you need to prepare ``local.conf``
file, but no worries. Several ``local.conf`` files are shared on the Internet
and a minimum example is shown below. From our experience, you need a machine
with two or four CPU cores, 8 GB memory and 20 GB disk to run DevStack
comfortably. If you enable just major OpenStack projects, the machine
requirement would be much smaller like 2~4GB memory.

.. code-block:: console

   $ BRANCH=master
   $ git clone https://opendev.org/openstack/devstack.git
   $ cd devstack
   $ git checkout $BRANCH
   <prepare local.conf>
   $ ./stack.sh
   <wait and wait... it takes 20 or 30 minutes>

Replace ``$BRANCH`` with an appropriate branch such as ``master``,
``stable/newton`` or ``stable/mitaka``.

The following is an example of ``local.conf`` for Newton release which runs
core components (keystone, nova, glance, neutron, cinder), horizon, swift and
heat. The components which the main horizon code supports are chosen.

.. literalinclude:: ../../checksite/local.conf
   :language: ini

Import latest translations
++++++++++++++++++++++++++

Translations are being imported into a project repository daily,
so in most cases you do not need to pull translations from Zanata
manually. What you need is to pull the latest horizon code.

If you have a machine running DevStack, there are two ways.

One way is to update the horizon code only.
The following shell script fetches the latest horizon code,
compiles translation message catalogs and reloads the apache httpd server.
Replace ``$BRANCH`` with an appropriate branch such as ``master``,
``stable/newton`` or ``stable/mitaka``.

.. literalinclude:: ../../checksite/horizon-reload.sh
   :language: bash

The other way is to rerun DevStack. Ensure to include ``RECLONE=True`` in
your ``local.conf`` before running ``stack.sh`` again so that DevStack
retrieve the latest codes of horizon and other projects.

.. code-block:: console

   $ cd devstack
   $ ./unstack.sh
   <Ensure RECLONE=True in your local.conf>
   $ ./stack.sh
   <It takes 10 or 15 minutes>

CLI (command line interface)
----------------------------

TBD

Server projects
---------------

TBD
