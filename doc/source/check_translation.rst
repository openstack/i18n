=========================
How to check translations
=========================

It is important to check your translations by using a real situation where your
translation is used. This page describes how to check your translations.

Documentation
-------------

Using docs.openstack.org
~~~~~~~~~~~~~~~~~~~~~~~~

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
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We can translate the application developer documentations,
such as API Guide, as ``api-site`` resources in Zanata.

OpenStack developer documentation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Currently, we do not support translations for OpenStack developer
documents: http://docs.openstack.org/developer/<project>

OpenStack Dashboard
-------------------

Translation check site
~~~~~~~~~~~~~~~~~~~~~~

The infra and i18n teams are preparing the translation check site
to check dashboard translations. It is under preparation.

Running DevStack
~~~~~~~~~~~~~~~~

Another convenient way is to check dashboard translations is to run
DevStack in your local environment.  To run DevStack, you need to
prepare ``local.conf`` file, but no worries. Several ``local.conf``
files are shared, for example [#]_. From our experience, you need a
machine with two or four CPU core, 8 GB memory and 20 GB disk to run
DevStack comfortablely. If you enable just major OpenStack projects,
the machine requirement would be much smaller like 2~4GB memory.

.. code-block:: console

   $ git clone http://git.openstack.org/openstack-dev/devstack.git
   $ cd devstack
   <prepare local.conf>
   $ ./stack.sh
   <wait and wait... it takes 20 or 30 minutes>

Translations are being imported into a project repository daily,
so in most cases you do not need to pull translations from Zanata
manually.

.. [#] https://gist.github.com/amotoki/b5ca4affd768177ed911

CLI (command line interface)
----------------------------

TBD

Server projects
---------------

TBD
