=====
Tools
=====

This page covers various operations around i18n activities.

.. _zanata-cli:

Zanata CLI
----------

OpenStack uses Zanata as a translation platform.
While most operations around the translation platform are automated,
if you want to communicate with the translation platform manually,
you can use `Zanata CLI <http://docs.zanata.org/en/release/client/>`__.

User configuration
~~~~~~~~~~~~~~~~~~

You need to create a configuration file in ``$HOME/.config/zanata.ini``
that contains user-specific configuration. For information on how to
create a configuration file, see `Zanata CLI configuration
<http://docs.zanata.org/en/release/client/configuration/#user-configuration>`__.

Project configuration
~~~~~~~~~~~~~~~~~~~~~

To communicate with the translation platform, you need to prepare
a project configuration file named ``zanata.xml`` in the top directory
of a project you are interested in.
OpenStack projects does not contain ``zanata.xml`` in their git repositories,
so you need to create it manually.

The following is an example of ``zanata.xml``.
In most cases, what you need to edit are **project** and **project-version**.

.. code-block:: xml

   <config xmlns="http://zanata.org/namespace/config/">
     <url>https://translate.openstack.org/</url>
     <project>horizon</project>
     <project-version>master</project-version>
     <project-type>gettext</project-type>
     <src-dir>.</src-dir>
     <trans-dir>.</trans-dir>
     <rules>
       <rule pattern="**/*.pot">{path}/{locale_with_underscore}/LC_MESSAGES/{filename}.po</rule>
     </rules>
     <excludes>.tox/**</excludes>
   </config>

Pull translations from Zanata
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To download translations from Zanata, run the following command
after going into a project directory.
You are usually interested in only a few of languages,
so ``--locales`` option would be useful.
For more options, see the output of ``zanata pull --help``.

.. code-block:: console

   $ zanata-cli pull --locales ja,ko-KR,zh-CN

Project maintenance
-------------------

.. note::

   The scripts below depend on several python modules.
   To install these dependencies, run ``pip install -e requirements.txt``.

   More convenient way is to use **tox** like
   ``tox -e venv -- python <script-name>``.

   **tox** is available on PyPI and also available in various Linux
   distribution. ``pip install tox`` or ``apt-get install python-tox``
   (in case of Ubuntu) installs **tox**.

.. _sync-translator-list:

Sync the translator list with Zanata
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The I18n project maintains a list of language teams and their members.
The list is used by Stackalytics to gather translation statistics
(See :ref:`stats-stackalytics` for detail). It is also used by the
scripts below.

The filename of the list is ``tools/translation_team.yaml``.

This list is a cache of information on Zanata, and we need to keep it
synced with Zanata.

To sync the translator list, run the following command:

.. code-block:: console

   tox -e zanata-users-sync

The above run the following internally:

.. code-block:: console

   python tools/zanata/zanata_users.py --output-file tools/zanata/translation_team.yaml

Retrieve translation statistics
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:ref:`ATC status in I18n project <i18n-atc>` is determined based on
translation statistics in a specific period.

The script ``tools/zanata/zanata_stats.py`` helps retrieving
translation statistics from Zanata.

To run the script:

.. code-block:: console

   tox -e venv -- python ./tools/zanata/zanata_stats.py <options>

``--help`` option shows the detail usage.

Extract Zanata user information
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

At the moment, the I18n PTL needs to maintain the ATC list of the I18n
project manually around the end of each release cycle.
This requires name and e-mail address of individual translators.

The script ``tools/zanata/zanata_userinfo.py`` helps this.
It generates a CSV file by reading a YAML file which contains the list
of translators (e.g., ``translation_team.yaml``) with user name and
e-mail addresses by interacting with Zanata API.

.. note::

   This script requires Zanata admin privilege.
