=============================
Official OpenStack translator
=============================

Steps to become a OpenStack translator
--------------------------------------

Translation is another kind of important contribution to OpenStack
community. If you want to become a official translator, you need to
finish following steps:

1. Before you start contribution, you'll have to `agree
   to the contributor license agreement
   <http://docs.openstack.org/infra/manual/developers.html#account-setup>`_.
   (You can preview the full text of `the OpenStack Individual
   Contributor License Agreement
   <https://review.opendev.org/static/cla.html>`_ first if you want.)

   .. note::

      If you want to become a translator only, simply speaking,
      you need to `join The OpenStack Foundation
      <https://www.openstack.org/join/>`_
      (select "Foundation Member") and
      `sign the appropriate Individual Contributor License Agreement
      <http://docs.openstack.org/infra/manual/developers.html#sign-the-appropriate-individual-contributor-license-agreement>`_.

2. Register a user ID in Zanata

   * Go to `Zanata server <https://translate.openstack.org/>`_
   * Click "Log in" button.
   * If you don't have OpenStack ID,
     `register one <https://www.openstack.org/join/register>`_.
   * After you log in with OpenStack ID, you will be requested to fill in
     your profile.

   .. note::

      You are encouraged to register with your business email,
      which will help your company to get the credit. If you don't
      want to, use your personal email will be OK too.

3. Request to join a translation team

   * Click "Languages" on the top, all languages will be listed.
   * Click the language you want to translate, the language page will
     be shown.
   * Click "..." on the right, and select "Request to join team".
   * Input a short introduction of yourself, including your name, as
     "Additional information", then click "Send message".

   .. note::

      Make sure to include a short introduction because it is the
      only information which language coordinators can use to
      determine your join request is valid or not.

4. When your request is approved, you will get an email notification.

   .. note::

      If your request is pending for long days, you can reach to your
      language coordinator through Zanata,
      to `I18n people <https://wiki.openstack.org/wiki/I18nTeam#People>`_
      through `IRC <https://docs.openstack.org/i18n/latest/#openstack-i18n-team>`_
      , or to `I18n PTL <https://governance.openstack.org/tc/reference/projects/i18n.html>`_
      directly.

5. Now you can start your translation.
   You can actually become an OpenStack official translator
   by contributing translations.
   You can find :doc:`various ways of contributions <contributing>`.

.. _i18n-atc:

ATC status in I18n project
--------------------------

The I18n project is an official OpenStack project, so official translators
who have contributed translations to
`official OpenStack projects <https://governance.openstack.org/tc/reference/projects/index.html>`_
in a specific period are regarded as "ATC" (Active Technical Contributor) and
"APC" (Active Project Contributor) of the I18n project.
APC can vote for the I18n PTL (Project Team Lead), and ATC
can vote for OpenStack TC (Technical Committee).
For more detail on ATC, APC and TC,
see `OpenStack Technical Committee Charter
<http://governance.openstack.org/reference/charter.html>`__.

As of now, ATC of official translators are treated as extra ATCs
as we have no way to collect statistics automatically now.
The list of extra ATCs is maintained by the PTL and is usually updated
short before the deadline of extra ATCs nomination in each release cycle.
The deadline of extra ATCs nomination can be checked in the release
schedule page at http://releases.openstack.org/ (for example,
http://releases.openstack.org/newton/schedule.html).

Translators who translate and review 300 and more words combinedly
in the last six months until the deadline of extra ATCs nomination are
nominated as ATCs, and the ATC status of translators is valid for one year.
Translation count and review count can be added up.
The detail period is determined by the PTL in each cycle.
For Newton cycle, the six month period was from 2016-02-01 to 2016-07-31,
and this ATC status will expire on July 2017 if there will be no
additional translation contributions.

.. note::

   I18n PTL updates the list using Zanata API and translator list.
   Detail statistics data is available :ref:`below <atc-stats>`.

If you have a question, feel free to ask it to the PTL or the i18n list.

Note that code or documentation contributors to openstack/i18n repository
are acknowledged as ATC automatically in the same way as for most OpenStack
projects.

.. _atc-stats:

ATC members of I18n project
---------------------------

A list of all ATCs is available at
http://governance.openstack.org/reference/projects/i18n.html#extra-atcs.

The statistics are calculated using
`a Python script <https://opendev.org/openstack/i18n/src/tools/zanata/zanata_stats.py>`__
powered by
`Zanata statistics API <http://zanata.org/zanata-platform/rest-api-docs/resource_StatisticsResource.html>`__
Translator list is maintained by
`translation_team.yaml <https://opendev.org/openstack/i18n/src/tools/zanata/translation_team.yaml>`__
stored in `openstack/i18n git repository <https://opendev.org/openstack/i18n>`__.

.. toctree::
   :maxdepth: 2

   atc-stats

.. _i18n-auc:

AUC status in I18n project
--------------------------

As OpenStack evolved, Active User Contributor (AUC) recognition process was
introduced by the `OpenStack User Committee (UC) <https://governance.openstack.org/uc/>`_.
AUCs are acknowledged to operators and users who contributed aligned with UC
governance.

In Zanata, some project translations such as
`OpenStack User Survey <https://translate.openstack.org/iteration/view/openstack-user-survey/openstack-user-survey/documents>`_
and `OpenStack whitepapers <https://translate.openstack.org/version-group/view/Whitepaper-dashboard-translation/projects>`_
are not in `official projects <https://governance.openstack.org/tc/reference/projects/index.html>`_
but strongly encouraged to translate for better OpenStack world,
and translators who translated those projects are recognized as AUCs.

As of now, similar as ATCs, there is no way to collect statistics automatically.
The list of AUCs is calculated by the PTL and is usually updated
by communication with UC.

Translators who translate and review 300 and more words combinedly
in the last six months until the deadline of AUC nomination are
nominated as AUCs, and translation count and review count can be added up.
The detail period is determined by the PTL in each cycle.
For Train cycle, the six month period was from 2019-01-26 to 2019-07-25.
