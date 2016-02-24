================
Translation tips
================

This page collects small tips and tricks around translations.

If you have any, don't hesitate to share it :)

Where a string is used in source code?
======================================

It is important to understand how an original string is used in the source code
with contextual knowledge for better quality of translations.
Unfortunately Zanata translation interface does not show where
a target string is used in a source code correspondingly.

You can find the location in a source code by checking the POT file
in a corresponding git repository.

Zanata project and git repository are one-to-one relationship.
If Zanata project name is ``<Zanata-project-name>``,
the corresponding git repository location is
``http://git.openstack.org/cgit/openstack/<Zanata-project-name>/``.
For example, if you are translating ``horizon``, the git repository is found at
http://git.openstack.org/cgit/openstack/horizon/.

POT file exists at ``<module-name>/locale/<Zanata-document-name>.pot``.
``<module-name>`` varies across projects. For example,

* horizon

  * http://git.openstack.org/cgit/openstack/horizon/tree/openstack_dashboard/locale/
  * http://git.openstack.org/cgit/openstack/horizon/tree/horizon/locale/

* trove-dashboard: http://git.openstack.org/cgit/openstack/trove-dashboard/tree/trove_dashboard/locale

POT file name depends on a project.

* For a dashboard related project, ``django.pot`` and ``djangojs.pot``
* For a normal python project, ``<module-name>.pot`` like ``nova.pot``
  and ``<module-name>-log-<level>.pot`` like ``nova-log-error.pot``.

  * Note that a normal python project, we also have separate POT files.

Open a POT file you find and search a string you are interested in.
Then you can find an entry like:

.. code-block:: none

   #: trove_dashboard/content/database_backups/views.py:100
   #, python-format
   msgid "Unable to retrieve details for parent backup: %s"
   msgstr ""

Where a string is used in Dashboard UI?
=======================================

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
