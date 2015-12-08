=========================
Handling translation bugs
=========================

If you are a translator or a person involved in I18n effort,
you may be interested in fixing translation bugs :)

Bugs in translated documents or dashboard are mainly classified into
the following areas:

* translation bugs
* bugs in original strings
* bugs in tool chains

Translation bugs
----------------

Visit a corresponding resource in Zanata and correct translations.

.. note::

   As a translator, if reported bugs turns out beyond a translation bug, it is
   better to ask I18n team members via the mailing list or the IRC channel.
   They can handle such bugs.

Bugs in original strings
------------------------

If a reported bug turns out that an original string or message is not correct,
we suggest to file a bug to a corresponding OpenStack project.
In most cases, a related project would be one of:

* `OpenStack manuals <https://bugs.launchpad.net/openstack-manuals>`_
* `Horizon (OpenStack dashboard) <https://bugs.launchpad.net/horizon>`_

.. note::

   During translation you may sometimes encounter strings which are hard to
   translate in your language. For example, we cannot control the order of
   words, or a plural form is not supported.  Usually, this kind of bugs cannot
   be fixed just by changing the strings and more work is needed.  We would
   also suggest to file a bug to a corresponding project above.  In this case,
   ensure to add **i18n** tag when filing a bug.

Bugs in tool chains
-------------------

If you encounter more complicated things including translation tool chains or
something others, the most recommended way is to ask it in the I18n mailing
list ``openstack-i18n@lists.openstack.org``.
Of course you can file a bug against a related project directly.
