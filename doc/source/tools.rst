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

Handling documentation projects
-------------------------------

.. note::

   This is written about openstack-manuals project.
   As of the end of Pike development cycle,
   `the document migration community-wide effort
   <https://specs.openstack.org/openstack/docs-specs/specs/pike/os-manuals-migration.html>`__
   is being done. The process documented here might be changed in near future.

OpenStack documents are using RST format.
The steps to translate RST documents include:

* Slicing: generate PO templates from RST documents
* Uploading: Upload the translation resources to Zanata
* Translating: manage the translation in Zanata, including the translation
  memory and glossary management
* Downloading: Download the translated results by automation scripts.
* Building: Build HTML from RST documents and the translated results.

Sphinx is a tool to translate RST source files to various output formats,
including POT and HTML. You need to install Sphinx before you go to below
steps. Almost all projects have ``test-requirements.txt`` in their repositories
and you can check the required version of Sphinx by checking this file.

.. code-block:: console

   $ pip install Sphinx

Or, more convenient way would be:

.. code-block:: console

   $ pip install -r test-requirements.txt

Slicing
~~~~~~~

We use sphinx-build to translate RST files to POT files. Because we want to
have a single POT file per document, we use msgcat to merge those POTs after
sphinx-build.

.. code-block:: console

   $ sphinx-build -b gettext doc/[docname]/source/ doc/[docname]/source/locale/
   $ msgcat doc/[docname]/source/locale/*.pot > doc/[docname]/source/locale/[docname].pot

Uploading
~~~~~~~~~

We use :ref:`Zanata CLI <zanata-cli>` to upload the POT file to the translate
platform.

Downloading
~~~~~~~~~~~

We use :ref:`Zanata CLI <zanata-cli>` to download the translated PO files from
the translation platform.

Building
~~~~~~~~

Before use sphinx-build to build HTML file, we need to feed the translations
from the single PO file into those small PO files. For example:

.. code-block:: console

   $ msgmerge -o doc/[docname]/source/locale/zh_CN/LC_MESSAGES/A.po \
       doc/[docname]/source/locale/zh_CN/LC_MESSAGES/[docname].po \
       doc/[docname]/source/locale/A.pot

Then, for every PO file, we should execute the following command to build into
MO file:

.. code-block:: console

   $ msgfmt doc/[docname]/source/locale/zh_CN/LC_MESSAGES/A.po \
      -o doc/[docname]/source/locale/zh_CN/LC_MESSAGES/A.mo

Finally, we could generate HTML files by

.. code-block:: console

   $ sphinx-build -D "language='zh_CN' doc/[docname]/source/ \
       doc/[docname]/build/html

Handling python projects
------------------------

For most of the Python projects, the preferred tools for I18N are gettext and
babel. The gettext module provides internationalization (I18N) and localization
(L10N) services for your Python modules and applications. Babel are a
collection of tools for internationalizing Python applications.

Extracting
~~~~~~~~~~

You can extract the messages in code to PO template (POT) with pybabel,
where **PROJECT** is a project name like ``nova`` and **VERSION** is a version
number. Note that you can omit ``--project`` and ``--version`` options
if you just use them locally as they are just used in the POT file header.

.. code-block:: console

   $ pybabel extract \
       --add-comments Translators: \
       -k "_C:1c,2" -k "_P:1,2" \
       --project=${PROJECT} --version=${VERSION} \
       -o ${modulename}/locale/${modulename}.pot \
       ${modulename}

For example, in case of nova,

.. code-block:: console

   $ pybabel extract \
       --add-comments Translators: \
       -k "_C:1c,2" -k "_P:1,2" \
       --project=nova --version=${VERSION} \
       -o nova/locale/nova.pot nova/

Uploading
~~~~~~~~~

For each Python project in OpenStack, there is an automation job to extract the
messages , generate PO template and upload to Zanata, which is triggered by the
"commit" event. See :doc:`here <infra>`.

Downloading
~~~~~~~~~~~

For each Python project in OpenStack, there is an automation job daily to
download the translations in PO file to the "locale" folder under the source
folder of each project. See :doc:`here <infra>`. It will generate a review
request in Gerrit. After :doc:`review <reviewing-translation-import>`,
the translation in PO file will be merged.

Using translations
~~~~~~~~~~~~~~~~~~

To display translated messages in python server projects,
you need to compile message catalogs and also need to configure
your server services following instructions described at
`oslo.i18n documentation <https://docs.openstack.org/oslo.i18n/latest/user/usage.html#displaying-translated-messages>`__.

.. _handling_horizon_projects:

Handling horizon projects
-------------------------

For horizon related projects, Django, a framework which horizon is built on,
provides integrated translation support.

.. note::

   Unlike documentations and python projects, horizon and plugins use
   ``zh-hans`` and ``zh-hant`` for Chinese locales instead of ``zh-cn`` and
   ``zh-tw`` respectively since Wallaby release. This follows the Django
   recommendation which happened in `Django 1.7
   <https://www.djbook.ru/rel1.7/releases/1.7.html#language-codes-zh-cn-zh-tw-and-fy-nl>`__.
   The details are found in `the mailing list post
   <http://lists.openstack.org/pipermail/openstack-discuss/2021-February/020169.html>`__.

Extracting
~~~~~~~~~~

horizon provides a command to extract the messages in code to PO template
(POT). Run the following command in your repository.

.. code-block:: console

   $ python manage.py extract_messages -m ${MODULE_NAME}

where **MODULE_NAME** is a python module name of horizon or its plugin.

For example, in case of manila-ui,

.. code-block:: console

   $ python manage.py extract_messages -m manila_ui

The above command is a wrapper for pybabel and the translation job
uses pybabel directly.

Uploading
~~~~~~~~~

For each horizon related project in OpenStack, there is an automation job to
extract the messages , generate PO template and upload to Zanata, which is
triggered by the "commit" event. See :doc:`here <infra>`.

Downloading
~~~~~~~~~~~

For each horizon related project in OpenStack, there is an automation job daily
to download the translations in PO file to the "locale" folder under the source
folder of each project. See :doc:`here <infra>`. It will generate a review
request in Gerrit. After :doc:`review <reviewing-translation-import>`,
the translation in PO file will be merged.

.. note::

   As noted above, in Wallaby or later releases, ``zh-hans`` and ``zh-hant``
   are used for Chinese locales. On the other hand, ``zh-cn`` and ``zh-tw``
   continues to be used in Zanata. When the job downloads translations from
   Zanata, the job stores translations for ``zh-cn`` and ``zh-tw`` to
   ``zh-hans`` and ``zh-hant`` directories under ``locale``.

Using translations
~~~~~~~~~~~~~~~~~~

To display translated messages in OpenStack dashboard, you need to compile
message catalogs. Django picks up translated messages automatically once they
are compiled. The following command compiles messages in your project.

.. code-block:: console

   $ python manage.py compilemessages

.. _project-maintenance:

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
