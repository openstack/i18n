================
Translation tips
================

This page collects small tips and tricks around translations.

If you have any, don't hesitate to share it :)

Where a string is used in source code?
======================================

It is important to know how a string you are translating is used in a
corresponding source code for better quality of translations.
Unfortunately Zanata translation interface shows no information about
a corresponding location in a source code now.

You can know the location in a source code by checking the POT file
in a corresponding git repository.

Zanata project and git repository are 1-to-1 mapping and
``http://git.openstack.org/cgit/openstack/<Zanata-project-name>/``.
If you are translating ``horizon``, the git repository is found at
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

Where a string is used in Dashboard?
====================================

During translating a dashboard related project, you may want to know
"where is this string used in the dashboard?".

You can estimate where a string is used from a location in a source code.
(see the previous entry on how to know a location.)

``dashboards/admin/aggregates/views.py:104``
    This means ``aggregate`` means "Aggregate" menu in "Admin" group
    in the left side menu.

``dashboards/project/loadbalancers/workflows.py:44``
    When a filename is ``workflows.py`` or ``forms.py``, it means
    it is used in a form for creating or editing something.

``dashboards/project/containers/templates/containers/_update.html:21``
    A template is a skeleton of static HTML files. In this case,
    the string is perhaps used in "Update" form in "Container" menu.
