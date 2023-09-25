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
   <https://docs.openstack.org/contributors/common/setup-gerrit.html#individual-contributor-license-agreement>`_.
   (You can preview the full text of the `OpenInfra Foundation Individual
   Contributor License Agreement
   <https://review.opendev.org/static/cla.html>`_ first if you want.)

   .. note::

      If you want to become a translator only, simply speaking,
      you need to `join The OpenInfra Foundation - Individual
      <https://openinfra.dev/join/>`_.
      You can see more details at `Contributor Guide - Account Setup <https://docs.openstack.org/contributors/common/accounts.html>`_.

2. Register a user ID in Zanata

   * Go to `Zanata server <https://translate.openstack.org/>`_
   * Click "Log in" button.
   * If you don't have OpenInfra ID (previously, OpenStack ID),
     `register one <https://id.openinfra.dev/auth/register>`_.
   * After you log in with OpenInfra ID, you will be requested to fill in
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
      , or to `I18n SIG Chair <https://governance.openstack.org/sigs/>`_
      directly.

5. Now you can start your translation.
   You can actually become an OpenStack official translator
   by contributing translations.
   You can find :doc:`various ways of contributions <contributing>`.

.. _i18n-ac:

Active Contributor status in I18n project
-----------------------------------------

The I18n team is one of official OpenStack SIGs (Special Interest Groups),
so official translators who have contributed translations to the strings in
code (e.g., Horizon) or documentations in official
`OpenStack projects <https://governance.openstack.org/tc/reference/projects/index.html>`_
or `OpenStack SIGs <https://governance.openstack.org/sigs/>`_ in a specific
period are regarded as "AC" (Active Contributor) of the I18n SIG. AC can vote
for OpenStack TC (Technical Committee). For more detail on AC and TC,
see `OpenStack Technical Committee Charter
<http://governance.openstack.org/reference/charter.html>`_.

As of now, AC of official translators are treated as extra ACs
as we have no way to collect statistics automatically now.
The list of extra ACs is maintained by the PTL or SIG Chair and usually updated
short before the deadline of extra ACs nomination in each release cycle.
The deadline of extra ACs nomination can be checked in the release
schedule page at http://releases.openstack.org/ (for example,
http://releases.openstack.org/bobcat/schedule.html).

Translators who translate and review at least 300 words combinedly
in the last six months until the deadline of extra ACs nomination are
nominated as ACs, and the AC status of translators is valid for one year.
Translation count and review count can be added up.
The detail period is determined by the PTL or SIG Chair in each cycle.
For Antelope cycle, the six month period was from 2022-10-05 to 2023-03-22,
and this AC status will expire on March 2024 if there will be no
additional translation contributions.

.. note::

   I18n SIG Chair updates the list using Zanata API and translator list.
   Detail statistics data is available :ref:`below <ac-stats>`.

If you have a question, feel free to ask it to the SIG Chair or the i18n list.

Note that code or documentation contributors to openstack/i18n repository
are acknowledged as AC automatically in the same way as for most OpenStack
projects and/or SIGs.

.. _ac-stats:

AC members of I18n project
--------------------------

A current list of all ACs is available at
https://github.com/openstack/governance/blob/master/reference/sigs-repos.yaml.

The statistics are calculated using
`a Python script <https://opendev.org/openstack/i18n/src/tools/zanata/zanata_stats.py>`__
powered by
`Zanata statistics API <http://zanata.org/zanata-platform/rest-api-docs/resource_StatisticsResource.html>`__
Translator list is maintained by
`translation_team.yaml <https://opendev.org/openstack/i18n/src/tools/zanata/translation_team.yaml>`__
stored in `openstack/i18n git repository <https://opendev.org/openstack/i18n>`__.

ATC members of I18n project
---------------------------

Before the transition to I18n SIG, I18n team was formed as one of official
OpenStack projects and the ATC list was maintained by proposing a patch to
`projects.yaml on governance repository
<https://github.com/openstack/governance/blob/master/reference/projects.yaml>`_.

.. note::

   On June 2021, ATC was renamed to AC.
   More information is available at `one TC resolution <https://governance.openstack.org/tc/resolutions/20210602-atc-renamed-to-ac.html>`_.

.. toctree::
   :maxdepth: 2

   atc-stats

.. _i18n-auc:

AUC status in I18n project
--------------------------

.. note::

   As User Committee no longer operated from August 1, 2020, I18n team now
   does not look up AUC status. See `OpenStack User Committee
   Charter <https://governance.openstack.org/tc/reference/user-committee-charter.html>`_
   for more information.

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
The list of AUCs was calculated by the PTL and is usually updated
by communication with UC.
