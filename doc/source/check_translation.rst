=========================
How to check translations
=========================

It is important to check your translations by using a real situation where your
translation is used. This page describes how to check your translations.

Documentation
=============

Using docs.openstack.org
------------------------

Translated documents are available at the OpenStack Documentation site.
It is updated daily. Most contents are linked from either of:

* http://docs.openstack.org/<lang> contains released documents.
  Follow "More Releases and Languages" in http://docs.openstack.org/.
* http://docs.openstack.org/draft/draft-index.html contains
  draft (unreleased) documents.

To build a translated document, you need to update the file
``doc-tools-check-languages.conf`` in each repository, and
add an entry to ``BOOKS`` like ``["ja"]="install-guide"``.
Also, to build as a draft, you need to add an entry to ``DRAFTS``.

For a document in a stable branch, such as the installation guide for
Liberty, you need to update the file ``doc-tools-check-languages.conf``
in the target stable branch directly.
You must add an entry to ``DRAFTS``, which is used as a special flag
for a stable branch.

You can check a generated document for a specified branch on
http://docs.openstack.org/<branch>/<language>/<document>.
For example, the link of Ubuntu Installation Guide for Liberty is
http://docs.openstack.org/liberty/ja/install-guide-ubuntu/.

To add a link to a generated document, you need to update the file
``www/<lang>/index.html`` in the ``master`` branch of
the ``openstack-manuals`` repository.
Note that the web pages are published from ``master`` branch,
which contains the pages for all releases, such as Liberty.
Therefore, you don't need to update the file ``www/<lang>/index.html``
in the stable branch.

Application developer documentation
-----------------------------------

We can translate the application developer documentations,
such as API Guide, as ``api-site`` resources in Zanata.

OpenStack developer documentation
---------------------------------

Currently, we do not support translations for OpenStack developer
documents: http://docs.openstack.org/developer/<project>

OpenStack Dashboard
===================

Translation check site
----------------------

The infra and i18n teams are preparing the translation check site
to check dashboard translations. It is under preparation.

.. note::

   Currently there is no solid plan when the check site is provided.

Running DevStack
----------------

Another convenient way is to check dashboard translations is to run DevStack in
your local environment. To run DevStack, you need to prepare ``local.conf``
file, but no worries. Several ``local.conf`` files are shared on the Internet
and an minimum example is shown below. From our experience, you need a machine
with two or four CPU cores, 8 GB memory and 20 GB disk to run DevStack
comfortablely. If you enable just major OpenStack projects, the machine
requirement would be much smaller like 2~4GB memory.

.. code-block:: console

   $ BRANCH=master
   $ git clone http://git.openstack.org/openstack-dev/devstack.git
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

Another way is to rerun DevStack. Ensure to include ``RECLONE=True`` in
your ``local.conf`` before running ``stack.sh`` again so that DevStack
retrieve the latest codes of horizon and other projects.

.. code-block:: console

   $ cd devstack
   $ ./unstack.sh
   <Ensure RECLONE=True in your local.conf>
   $ ./stack.sh
   <It takes 10 or 15 minutes>

CLI (command line interface)
============================

TBD

Server projects
===============

TBD
