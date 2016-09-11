=========================
Handling translation bugs
=========================

If you are a translator or a person involved in I18n effort,
you may be interested in triaging and fixing translation bugs :)

The bug triaging process are following the `general bug triaging
process <https://wiki.openstack.org/wiki/BugTriage>`_.
If you want to help bug triaging tasks, join the `OpenStack I18n
bug team <https://launchpad.net/~openstack-i18n-bugs>`_ first.

Bugs in translated documents or dashboard are mainly classified into
the following areas:

* translation bugs
* bugs in a source project
* bugs in tool chains

Translation bugs
----------------

If a bug reports translation errors of a certain language, it could be
called **translation bug**.
The translation bug should be fixed in the translation tool.

If you are a speaker of this language, you could help

* tag the bug with a language name
* confirm the bug or mark it as incomplete
* prioritize the bug

If you are a translator of this language, you could help

* assign the bug to you or a member of your language team, and then
  mark it as "In Progress"
* fix it by visiting a corresponding resource in Zanata and
  correcting translations.

.. note::

   As a translator, if reported bugs turns out beyond a translation bug,
   it is better to ask I18n team members via the mailing list or the IRC
   channel. They can handle such bugs.

Bugs in a source project
------------------------

The translatable strings are extracted from a source project.
So some i18n bugs might be caused by bugs in the original strings/source
codes of a source project which contains these translatable strings.
Those kind of bugs should be fixed in the source project.

In most cases, a source project would be one of:

* `OpenStack manuals <https://bugs.launchpad.net/openstack-manuals>`_
* `Horizon (OpenStack dashboard) <https://bugs.launchpad.net/horizon>`_

You must determine whether bugs are **translation bugs** or **bugs in a
source project**. Typical i18n bugs in the source project include:

* Original string or message is not correct.
* Missed translations. Missed translations might be caused by not extracting
  English strings from the source project, or be caused by real missed
  translations. If the translations are missed in two different languages,
  they are probably bugs in the source project. Or else, they are real missed
  translations.
* Bugs to report English strings are hard to translate in your language.
  For example, translators cannot control the order of words, or a plural
  form is not supported. Usually, this kind of bugs are in the original
  strings and cannot be fixed just by changing the strings and more work
  is needed.

If a reported bug turns out to be bugs in a source project,
You could help

* tag it with the project name, for example "horizon" or "docs".
* add the source project to "Also affects project" of this bug.
* confirm the bug
* prioritize the bug

Bugs in tool chains
-------------------

If you encounter more complicated things including translation tool chains or
something others, the most recommended way is to ask it in the I18n mailing
list ``openstack-i18n@lists.openstack.org``.
Of course, you can file a bug against a related project directly.
