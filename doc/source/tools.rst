=====
Tools
=====

This page covers various operations around i18n activities.

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
