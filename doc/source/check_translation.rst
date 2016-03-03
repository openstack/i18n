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

TBD: How to enable translated document generation for your language
and add links to the above index pages.
At the moment, ask it in the i18n mailing list.

OpenStack Dashboard
===================

Translation check site
----------------------

The infra and i18n teams are preparing the translation check site
to check dashboard translations. It is under preparation.

Running DevStack
----------------

Another convenient way is to check dashboard translations is to run
DevStack in your local environment.  To run DevStack, you need to
prepare ``local.conf`` file, but no worries. Several ``local.conf``
files are shared, for example [#]_. From my experience, you need a
machine with two or four CPU core, 8 GB memory and 20 GB disk to run
DevStack comfortablely.

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
============================

TBD

Server projects
===============

TBD
