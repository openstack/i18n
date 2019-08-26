===============================
ATC Statistics in past releases
===============================

.. only:: latex

   .. note::

      You can see detail member-level statistics data on
      `HTML version of the page <https://docs.openstack.org/i18n/latest/atc-stats.html>`_.

Train cycle
-----------

No detail data.

Stein cycle
-----------

* Period: 2018-07-10 to 2019-01-25
* Patch on governance repository: https://review.opendev.org/633398
* Foundation membership was validated by calling a REST API in
  https://openstackid-resources.openstack.org

.. only:: html

   .. csv-table::
      :header-rows: 1
      :widths: 2 1 1 1 1 1 1 1 1 1 1 2
      :file: data/stein.csv

Rocky cycle
-----------

* Period: 2018-01-11 to 2018-07-09
* Patch on governance repository: https://review.opendev.org/586751
* Foundation membership was validated by calling a REST API in
  https://openstackid-resources.openstack.org

.. only:: html

   .. csv-table::
      :header-rows: 1
      :widths: 2 1 1 1 1 1 1 1 1 1 1 2
      :file: data/rocky.csv

Queens cycle
------------

* Period: 2017-07-01 to 2018-01-10
* Patch on governance repository: https://review.opendev.org/532982
* Foundation membership was validated by calling a REST API in
  https://openstackid-resources.openstack.org

.. only:: html

   .. csv-table::
      :header-rows: 1
      :widths: 2 1 1 1 1 1 1 1 1 1 1 2
      :file: data/queens.csv

Pike cycle
----------

* Period: 2017-01-06 to 2017-06-30
* Patch on governance repository: https://review.opendev.org/483452
* Foundation membership was validated by calling a REST API in
  https://openstackid-resources.openstack.org

.. only:: html

   .. csv-table::
      :header-rows: 1
      :widths: 2 1 1 1 1 1 2
      :file: data/pike.csv

Ocata cycle
-----------

* Period: 2016-08-01 to 2017-01-05
* Patch on governance repository: https://review.opendev.org/#/c/417569/
  (`diff <https://opendev.org/openstack/governance/commit/bd71cefff1302ed04fc21faac5cf967365a7d7c7>`__)
* Note: the period is relative short because of release cycle change

  * More information: https://releases.openstack.org/ocata/schedule.html &
    https://ttx.re/splitting-out-design-summit.html

* [ianychoi] Note: only "translated" metric was considered to follow the
  description in I18n contributor guide. After more detail investigation on
  previous ATC criteria, review metrics were also considered.
  Fortunately, the three translators (jftalta - 117 translated & 2897 reviews,
  myamamot - 725 reviews, mucahit - 1241 reviews) are also regarded ATCs from
  Newton cycle :) - I keep it as record for the next ATC list changes.

.. only:: html

   .. csv-table::
      :header-rows: 1
      :widths: 2 1 1 1 1
      :file: data/ocata.csv

Newton cycle
------------

* Period: 2016-02-01 to 2016-07-31
* Patch on governance repository: https://review.opendev.org/#/c/351480/
  (`diff <https://opendev.org/openstack/governance/commit/3aa6cb3e52944f8bed250e0714c7373605b2ebc5>`__)

.. only:: html

   .. csv-table::
      :header-rows: 1
      :widths: 2 1 1 1 1
      :file: data/newton.csv

Mitaka cycle
------------

* Period: 2015-08-01 to 2016-01-30
* Patch on governance repository: https://review.opendev.org/#/c/281145/
  (`diff <https://opendev.org/openstack/governance/commit/8b3c83f28102c7b47688fbaca970a52a76eb6de5>`__)
* This following statistics data is calculated using up-to-date
  `translation_team.yaml <https://opendev.org/openstack/i18n/src/commit/a67e08d86cc78907da38d5f09b8be6f71d1979a0/tools/zanata/translation_team.yaml>`__
  (date: Jan 15, 2017).
* When proposing extra ATCs at that time, some translators were not included in
  `translation_team.yaml <https://opendev.org/openstack/i18n/src/commit/73a36041dbdc45212051c60cbeef3f7783200fd2/tools/zanata/translation_team.yaml>`__
  file. It seems that 1) new translators were joined and the statistics was
  calculated but the file was already created, or 2) there might be some lack
  of communication with language coordinators, since I18n encouraged each
  language coordinator to update this file.
* [ianychoi] Although one year was already passed (as of now: Jan 15, 2017),
  I really would like to say those translators also contributed translations
  with I18n team members. For acknowledgement purpose, I write their Zanata ID,
  name, and language team in here :

  * Zbyněk Schwarz (id: tsbook) - Czech
  * Rob Cresswell (id: robcresswell) - English (United Kingdom)
  * Heleno Jimenez de la Cruz (id: heleno_jimenez) - Spanish (Mexico)
  * Jori Kuusinen (id: nuyori) - Finnish (Finland)
  * Masaki Matsushita (id: mmasaki) - Japanese
  * Amandeep Singh Saini (jimidar) - Punjabi (India)
  * Łukasz Jernas (id: deejay1) - Polish (Poland)

.. only:: html

   .. csv-table::
      :header-rows: 1
      :widths: 2 1 1 1 1
      :file: data/mitaka.csv

Liberty cycle
--------------

* Period: from 2014-11-01 to 2015-07-16

* Patch on governance repository: https://review.opendev.org/#/c/213989/
  (`diff <https://opendev.org/openstack/governance/commit/a229d38469c5135af496d3c739695acbe1146a76>`__)
* exported the translators contribution statistics from Transifex since
  2014-11-01 to 2015-07-16
* ATC candidates are translators who has translated more than 200 words and
  reported their e-mail and name to language coordinators, and also signed
  ICLA.
* More information on mailing list:
  http://lists.openstack.org/pipermail/openstack-i18n/2015-July/001220.html
* Statistics are available through:
  https://docs.google.com/spreadsheets/d/1YpDJU_uNA4I5fzFG69T6L9gpFsy5yNtA9a-lSxnqeAY/edit#gid=1366189722
