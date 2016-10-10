==================
Release management
==================

This page documents what the i18n team and teams concerned needs to do around
OpenStack releases.

#. (Project) Release milestone-3. "Soft StringFreeze" is in effect.
#. (Translator) Start translations for the release.

   * Translate **master** version on Zanata.

#. (I18n PTL) Call for translation

#. (I18n PTL) Coordinate release and translation import schedule of individual
   projects with PTL or I18n liaison.

#. (Project) Release RC1 and create a stable branch.
   "Hard StringFreeze" is in effect.

#. (Zanata admin) Create a stable version such as ``stable-newton``

   * The stable version is created from the master version on Zanata once RC1
     is cut and a stable branch is created in a git repository.
   * Once a stable version corresponding to a project stable branch is created
     on Zanata, the infra script will push strings automatically.

#. (Translator) Translate **stable-XXXX** version instead of master version
   on Zanata.

   * At this stage, the master version on Zanata is still open for
     translations, but it is strongly suggested to work on a stable version.

#. (Infra) Setup translation jobs such as ``translation-jobs-newton``
   to import translations for stable branches.

   * This should be done after a stable version on Zanata is created.

#. (Translator) It is suggested to complete translation work by Monday or
   Tuesday of the Final RC week. For more detail schedule,
   check http://releases.openstack.org/ .

#. (Project) RC2 or RC3 release will be shipped with latest translations.
   Final RC release will happen one week before the official release week.

#. (Project) Official release!

#. (Zanata admin) Merge a stable version back into the master version.

   * This usually happens within a week after the release.
   * The stable version is well reviewed, so it makes sense to merge
     translations into the master version on Zanata to avoid translating the
     same strings again.

#. After the official release, translating master version is welcome
   for upstream translation contribution, but the original strings may be
   changed frequently due to upstream development on the projects.

#. On the other hand, translating stable version as upstream contribution
   is not encouraged after the translated strings are packaged with releases.
   The stable version will be closed earlier than or around EOL.

#. If there is a translation bug on a stable version in Zanata,
   it is highly recommended to fix the same translation bug on the
   corresponding string in the master version.
