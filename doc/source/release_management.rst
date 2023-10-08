============================
Team activities with release
============================

This page documents what I18n team concerns and which things are needed
to do with OpenStack releases. Each OpenStack release has around 6-month cycle
and the corresponding schedule is available on https://releases.openstack.org/
(e.g., https://releases.openstack.org/ocata/schedule.html describes Ocata
release schedule).

One of main goals in I18n team is to incorporate translated strings into a new
release so that more global users experience translated version of OpenStack.
To accomplish this goal, some of team activities need to be aligned
with a release schedule.

.. note::

    I18n team sets target projects to be translated and prioritizes
    during around the `PTG <https://openinfra.dev/ptg/>`_.
    Current translation plan and priority are available on
    `translation dashboard <https://translate.openstack.org/>`_.

.. note::

    The terms in this page follow release schedule pages.
    You can see how OpenStack project teams product artifacts with release
    management on `Release Management <https://docs.openstack.org/project-team-guide/release-management.html>`_
    document.

Projects affecting StringFreezes
--------------------------------

Horizon and Horizon plugins are the main targets which affect StringFreezes.
Note that StringFreezes are applied to I18n team target projects and with
``cycle-with-rc`` or ``cycle-with-intermediary`` release model.

#. [Project] Release milestone-3. ``Soft StringFreeze`` is in effect.
#. [Translator] Start translations for the release.

   * Translate **master** version on Zanata.

#. [I18n SIG Chair] Call for translation

#. [I18n SIG Chair] Coordinate release and translation import schedule of
   individual projects with SIG Chair or I18n liaison.

#. [Project] Release RC1 and create a stable branch.
   ``Hard StringFreeze`` is in effect.

#. [Translator] It is suggested to complete translation work by Monday or
   Tuesday of the Final RC week.

   * It is encouraged to share translation progress with I18n team and/or
     corresponding project team(s) to make sure shipping the translation.

#. [Project] RC2 or RC3 release will be shipped with latest translations.
   Final RC release will happen one week before the official release week.

#. [Project] Official release!

#. [Zanata admin] Create a stable version after release.

#. [Infra] Setup translation jobs such as ``translation-jobs-newton``
   to import translations for stable branches.

   * This should be done after a stable version on Zanata is created.

#. After the official release, translating master version is welcome
   for upstream translation contribution, but the original strings may be
   changed frequently due to upstream development on the projects.

#. On the other hand, translating stable version as upstream contribution
   is not encouraged after the translated strings are packaged with releases.
   The stable version will be closed earlier than or around EOL.

#. If there is a translation bug on a stable version in Zanata,
   it is highly recommended to fix the same translation bug on the
   corresponding string in the master version.

Documentation projects
----------------------

All upstream OpenStack documents in ``openstack-manuals`` and project
repositories use ``master`` branch and can have stable branches depending
on release models and maintaining documents in different project teams.
Cross-project liaisons are strongly encouraged to communicate with I18n
team so that I18n team can discuss and decide which stable documents are
the target in I18n team and when translators start to translate stable
documents.

#. Translations on master version in Zanata are normally recommended for
   upstream contribution.

#. After the documents are translated and reviewed well, updating
   existing ``www/<lang>/index.html`` or creating a new language landing
   page is needed.

Other projects supported with translation jobs
----------------------------------------------

I18n team helps release activities on other projects if the projects have
cross-project liaison on I18n team and upon request.
