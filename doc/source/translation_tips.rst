================
Translation tips
================

This page collects small tips and tricks around translations.

If you have any, don't hesitate to share it :)

Where a string is used in source code?
--------------------------------------

It is important to understand how an original string is used in the source code
with contextual knowledge for better quality of translations.
Unfortunately Zanata translation interface does not show where
a target string is used in a source code correspondingly.

You can find the location in a source code by checking the POT file.

The POT file is found under
``http://tarballs.openstack.org/translation-source/<Zanata-project-name>/<Zanata-project-version>/<path>/<resource>.pot``,
where:

* ``<Zanata-project-name>`` is Zanata project name,
* ``<Zanata-project-version>`` is Zanata project version such as ``master`` or
  ``stable-mitaka``,
* ``<path>`` is a path of a document such as ``nova/locale``,
  ``openstack_dashboard/locale`` or ``releasenotes/source/locale``,
* ``<resource>`` is a document name in Zanata.

The easiest way would be to open
http://tarballs.openstack.org/translation-source and then
follow ``<Zanata-project-name>``, ``<Zanata-version>`` and corresponding links.

Open a POT file you find and search a string you are interested in.
Then you can find an entry like:

.. code-block:: none

   #: trove_dashboard/content/database_backups/views.py:100
   #, python-format
   msgid "Unable to retrieve details for parent backup: %s"
   msgstr ""

Once you find location(s) of a string you would like to check,
you can check more detail context where the string is used
by looking at the code in the git repository.
Zanata project and git repository are one-to-one relationship.
If Zanata project name is ``<Zanata-project-name>``,
the corresponding git repository location is
``https://opendev.org/openstack/<Zanata-project-name>/``.
For example, if you are translating ``horizon``, the git repository is found at
https://opendev.org/openstack/horizon/.

.. note::

   POT files are no longer stored in git repositories.
   The change was made at the beginning of Newton development cycle [#]_.

   .. [#] http://lists.openstack.org/pipermail/openstack-dev/2016-May/094215.html

Where a string is used in Dashboard UI?
---------------------------------------

During translating a dashboard related project, you may want to know
"where is this string used in the dashboard?".

You can estimate where a string is used from a location in a source code.
(See the previous entry on how to find a location.)

``dashboards/admin/aggregates/views.py:104``
    This means "Aggregates" menu in "Admin" group in the left side menu.
    In Horizon code, the second level corresponds to a dashboard group
    like "Project" or "Admin" and the third level corresponds to
    a panel like "Aggregates" (in this example), "Instances" or "Networks".

``dashboards/project/loadbalancers/workflows.py:44``
    When a filename is ``workflows.py`` or ``forms.py``, it means
    it is used in a form for creating or editing something.

``dashboards/project/containers/templates/containers/_update.html:21``
    A template is a skeleton of static HTML files. In this case,
    the string is perhaps used in "Update" form in "Container" menu.
