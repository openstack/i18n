======================
Translation Statistics
======================

There are several ways to know your translation activity.

Zanata
======

Zanata provides ways to know your activity on Zanata.

* `Dashboard <https://translate.openstack.org/dashboard/>`__ page
  shows your recent activity statistics this month and detail activity.
* `Profile <https://translate.openstack.org/profile/>`__ page
  provides more nice statistics view.
  It shows your statistics in this month and last month.

Note that you need to log into Zanata to see your activity in the above pages.

Stackalytics
============

`Stackalytics <http://stackalytics.com/>`__ is a popular web site
which allows us to know various statistics related to OpenStack.
It supports translation statistics :)

Visit `Stackalytics <http://stackalytics.com/>`__ and
choose ``Translations`` as ``Metric`` dropdown menu at the upper-right.

FAQ: I cannot find my name in Stackalytics
------------------------------------------

There are cases where you cannot see your translation statistics
in Stackalytics even after you translate strings in Zanata.

Here is the check list for such case:

* Is your Zanata ID included in the `translator list
  <http://git.openstack.org/cgit/openstack/i18n/tree/tools/zanata/translation_team.yaml>`__?
* Is your Zanata ID different from your launchpad ID?

If your Zanata ID is not included in the translator list,
you need to add your Zanata ID to the list.
Contact your language coordinator, email the i18n mailling list,
or submit a patch to add your ID by yourself.

.. TODO (amotoki):
   We need a guide for language coordinators.
   A Coordinator is recommended to update the translator list
   when he/she adds a new member to his/her language team.
   I hope someone adds a content.

If your Zanata ID is different from your launchpad ID,
Stackalytics will not find your translation statistics.
You need to let Stackalytics know your ID mappings.
To do this, you need to add your user data into ``etc/detault_data.json``
in `the Stackalytics repository <http://git.openstack.org/cgit/openstack/stackalytics/>`__.
An example is https://review.openstack.org/#/c/284638/1/etc/default_data.json.

If you are lucky to use a same name for launchpad and Zanata IDs,
you do not need to do the above.
Stackalytics will find your statistics automatically.
