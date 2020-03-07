=============================
Reviewing translation imports
=============================

.. note:: This document explains to reviewers details about the
          automatic import of translations from Zanata.

          If you are unfamiliar with translations in OpenStack, read
          the `Project Team Guide on Internationalization and
          Translation
          <http://docs.openstack.org/project-team-guide/i18n.html>`_
          first.

          This document gives additional information.


How are translations handled?
-----------------------------

Translators translate repositories using the `translation server
<http://translate.openstack.org>`_ which runs the Zanata software.

Every day, new translations get imported into the repositories using a
proposal job. These need to have a review on whether the bot worked properly.
You can see all open reviews in `Gerrit
<https://review.opendev.org/#/q/status:open+topic:zanata/translations,n,z>`_.
The subject of these patches is always "Imported Translations from
Zanata".

Reviewing
---------

If you are reviewing these translations, keep the following in mind:

* The change is done by a bot. If anything looks wrong with it, you
  need to actively reach out to the :ref:`OpenStack I18n team
  <openstack_i18n_team>` and point the problem out.
* The goal of the review is that the structure of the change is fine,
  it's not that the strings are translated properly. The review of
  translated strings is done by teams using the translation server.
* If you notice bad translations in a language, file a bug (see
  :ref:`reporting_translation_bugs`). Then the translation team will
  update the translation. We recommend to still import this change as
  is and import later the fix to not block other valid translations to
  merge.
* Nobody should change translation files (the `.po` files in the
  `locale` directory) besides the bot. The next automatic import will
  override any change again. Therefore, leave a ``-1`` vote on any
  such changes and point developer to this document.
* The proposal bot also removes files, it removes files that have very
  few translations in them. Note that no translations will be lost,
  they are still in the translation server.

  Also, release notes translations are only needed on master since
  release notes are published only from master, the translations get
  removed on stable branches.
* Most teams have single approval for translation imports instead of
  two core reviewers.
